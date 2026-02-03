"""
Core scheduling algorithm using Google OR-Tools CP-SAT solver.

This module is responsible for:
- Validating recurring slots (skeleton validation)
- Generating optimization suggestions for sub-optimal slots
- Running the CP-SAT solver to place remaining students
- Producing the final schedule with all constraints satisfied

Two-phase algorithm:
1. Skeleton: Lock recurring slots (from CSV)
2. Variations: Optimize placement of remaining students
"""

from typing import List, Dict, Tuple, Optional, Set
from datetime import time
import time as time_module

try:
    from ortools.sat.python import cp_model
except ImportError:
    cp_model = None  # Will be installed later

from .models import (
    Student, Slot, ScheduledClass, SlotStatus, UnplacedStudent, ScheduleResult,
    ValidationResult, SchedulingConstraints
)
from .parser import parse_recurring_slots_csv, parse_recurring_slots_csv_with_warnings


# ============================================================================
# PHASE 1: SKELETON (Recurring Slots)
# ============================================================================

def load_recurring_slots_csv(csv_path: str, all_students: List[Student]) -> List[ScheduledClass]:
    """Load recurring slots from CSV and create ScheduledClass objects.
    
    This is a wrapper around parse_recurring_slots_csv from parser.py
    for consistency with the scheduler interface.
    
    Args:
        csv_path: Path to recurring slots CSV
        all_students: List of all students for validation
    
    Returns:
        List of ScheduledClass with status=LOCKED
    
    Raises:
        ParseError: If CSV format invalid or validation fails
    """
    return parse_recurring_slots_csv(csv_path, all_students)


def validate_skeleton(
    skeleton: List[ScheduledClass],
    all_students: List[Student],
    coach_reserved: List[Slot]
) -> ValidationResult:
    """Validate skeleton (recurring slots) before optimization.
    
    Checks:
    - No overlap between ANY courses (UN SEUL COURS À LA FOIS)
    - Capacity per class (2-3 students)
    - All student names exist in main CSV
    - Slots within student availabilities
    - No overlap with coach reserved slots
    
    Args:
        skeleton: List of recurring scheduled classes
        all_students: List of all students from main CSV
        coach_reserved: List of slots reserved by coach
    
    Returns:
        ValidationResult with errors and warnings
    """
    errors = []
    warnings = []
    
    # Build student lookup
    student_map = {s.name: s for s in all_students}
    
    # Check 1: No overlap between ANY courses (UN SEUL COURS À LA FOIS)
    for i, class1 in enumerate(skeleton):
        for class2 in skeleton[i+1:]:
            if class1.slot.overlaps(class2.slot):
                errors.append(
                    f"Courses overlap (UN SEUL COURS À LA FOIS violated): "
                    f"{class1.slot.day} {class1.slot.start_time}-{class1.slot.end_time} "
                    f"({', '.join(class1.students)}) overlaps with "
                    f"{class2.slot.day} {class2.slot.start_time}-{class2.slot.end_time} "
                    f"({', '.join(class2.students)})"
                )
    
    # Check 2: Capacity per class (2-3 students)
    for scheduled_class in skeleton:
        if not scheduled_class.is_valid():
            if len(scheduled_class.students) < 2:
                # Allow single-student classes with NEEDS_VALIDATION status (generate warning, not error)
                if scheduled_class.status == SlotStatus.NEEDS_VALIDATION:
                    warnings.append(
                        f"Class {scheduled_class.slot.day} {scheduled_class.slot.start_time} "
                        f"has only {len(scheduled_class.students)} student(s). "
                        f"Consider adding another student to optimize this slot."
                    )
                else:
                    errors.append(
                        f"Class {scheduled_class.slot.day} {scheduled_class.slot.start_time} "
                        f"has only {len(scheduled_class.students)} student(s). Minimum 2 required."
                    )
            elif len(scheduled_class.students) > 3:
                errors.append(
                    f"Class {scheduled_class.slot.day} {scheduled_class.slot.start_time} "
                    f"has {len(scheduled_class.students)} students. Maximum 3 allowed."
                )
    
    # Check 3: All student names exist in main CSV
    for scheduled_class in skeleton:
        for student_name in scheduled_class.students:
            if student_name not in student_map:
                errors.append(
                    f"Student '{student_name}' in recurring slot "
                    f"{scheduled_class.slot.day} {scheduled_class.slot.start_time} "
                    f"not found in main availability CSV"
                )
    
    # Check 4: Slots within student availabilities
    for scheduled_class in skeleton:
        for student_name in scheduled_class.students:
            if student_name not in student_map:
                continue  # Already reported in Check 3
            
            student = student_map[student_name]
            slot = scheduled_class.slot
            
            # Get all availability slots for this day
            day_slots = [s for s in student.available_slots if s.day == slot.day]
            
            if not day_slots:
                errors.append(
                    f"Recurring slot {slot.day} {slot.start_time} "
                    f"for {student_name} has no availability on that day"
                )
                continue
            
            # Find min/max time for this day to determine availability range
            # This allows recurring slots at :30 to be valid within a :00 availability range
            min_start = min(s.start_time for s in day_slots)
            max_end = max(s.end_time for s in day_slots)
            
            # Check if recurring slot is within this range (not exact match)
            if not (slot.start_time >= min_start and slot.end_time <= max_end):
                errors.append(
                    f"Recurring slot {slot.day} {slot.start_time} "
                    f"for {student_name} not in their availability"
                )
    
    # Check 5: No overlap with coach reserved slots
    for scheduled_class in skeleton:
        for reserved_slot in coach_reserved:
            if scheduled_class.slot.overlaps(reserved_slot):
                errors.append(
                    f"Recurring class {scheduled_class.slot.day} {scheduled_class.slot.start_time} "
                    f"overlaps with coach reserved slot "
                    f"{reserved_slot.day} {reserved_slot.start_time}-{reserved_slot.end_time}"
                )
    
    is_valid = len(errors) == 0
    return ValidationResult(is_valid=is_valid, errors=errors, warnings=warnings)


def generate_optimization_suggestions(
    slot: Slot,
    current_student: str,
    all_students: List[Student]
) -> List[str]:
    """Generate suggestions for optimizing a single-student recurring slot.
    
    Finds compatible students who are available on the same time slot
    and suggests them for optimization. This is business logic for
    optimization, not parsing, so it belongs in the scheduler module.
    
    Args:
        slot: The recurring slot with only 1 student
        current_student: Name of the current student in the slot
        all_students: List of all students
    
    Returns:
        List of suggestion strings for optimization
    """
    suggestions = []
    compatible_students = []
    
    # Find students available on this slot
    for student in all_students:
        if student.name == current_student:
            continue
        
        # Check if student is available on this slot
        is_available = any(
            avail_slot.day == slot.day and
            avail_slot.start_time == slot.start_time and
            avail_slot.end_time == slot.end_time
            for avail_slot in student.available_slots
        )
        
        if is_available:
            compatible_students.append(student.name)
    
    if compatible_students:
        # Show top 3 compatible students
        top_students = compatible_students[:3]
        suggestions.append(
            f"Étudiants disponibles sur ce créneau : {', '.join(top_students)}"
        )
        if len(compatible_students) > 3:
            suggestions.append(f"... et {len(compatible_students) - 3} autre(s)")
    else:
        suggestions.append(
            "Aucun autre étudiant disponible sur ce créneau. "
            "Envisager de modifier les disponibilités ou de proposer un autre créneau."
        )
    
    return suggestions


def place_recurring_slots(recurring_slots: List[ScheduledClass]) -> Dict[Slot, ScheduledClass]:
    """Build initial schedule dictionary from recurring slots.
    
    Args:
        recurring_slots: List of validated recurring classes
    
    Returns:
        Dictionary mapping Slot → ScheduledClass
    """
    skeleton_schedule = {}
    
    for scheduled_class in recurring_slots:
        skeleton_schedule[scheduled_class.slot] = scheduled_class
    
    return skeleton_schedule


def get_placed_students_from_skeleton(skeleton: Dict[Slot, ScheduledClass]) -> Dict[str, int]:
    """Get count of how many times each student is placed in skeleton.
    
    Args:
        skeleton: Dictionary of skeleton schedule
    
    Returns:
        Dictionary mapping student_name → placement_count
    """
    placed_counts = {}
    
    for scheduled_class in skeleton.values():
        for student_name in scheduled_class.students:
            placed_counts[student_name] = placed_counts.get(student_name, 0) + 1
    
    return placed_counts


# ============================================================================
# PHASE 2: OR-TOOLS OPTIMIZATION
# ============================================================================

def optimize_variations(
    all_students: List[Student],
    skeleton: Dict[Slot, ScheduledClass],
    constraints: SchedulingConstraints
) -> ScheduleResult:
    """Optimize variable student placements using OR-Tools CP-SAT.
    
    Progressive timeout strategy:
    - Phase 2a (0-5 sec): All constraints (hard + soft with weights)
    - Phase 2b (5-10 sec): Relax soft constraints (hard only)
    - Phase 2c (10-15 sec): Maximize placements with early termination
    
    Args:
        all_students: List of all students
        skeleton: Dictionary of locked recurring classes
        constraints: Scheduling constraints
    
    Returns:
        ScheduleResult with complete or partial solution
    """
    if cp_model is None:
        raise ImportError(
            "OR-Tools not installed. Please install: pip install ortools"
        )
    
    start_time = time_module.time()
    
    # Get students already placed in skeleton
    skeleton_placements = get_placed_students_from_skeleton(skeleton)
    
    # Filter students who still need placement
    remaining_students = []
    for student in all_students:
        already_placed = skeleton_placements.get(student.name, 0)
        remaining_sessions = student.sessions_per_week - already_placed
        
        if remaining_sessions > 0:
            # Create a modified student with remaining sessions
            remaining_student = Student(
                name=student.name,
                sessions_per_week=remaining_sessions,
                available_slots=student.available_slots,
                linked_group=student.linked_group,
                notes=student.notes
            )
            remaining_students.append(remaining_student)
    
    # If no students need placement, return skeleton as final schedule
    if not remaining_students:
        return ScheduleResult(
            schedule=list(skeleton.values()),
            unplaced=[],
            metadata={
                "algorithm": "skeleton_only",
                "total_students": len(all_students),
                "placed_students": len(all_students),
                "execution_time_sec": time_module.time() - start_time
            }
        )
    
    # Collect all available slots (excluding skeleton and reserved)
    all_available_slots = _collect_available_slots(
        all_students,
        skeleton,
        constraints.coach_reserved_slots
    )
    
    # Try progressive timeout phases
    result = None
    
    # Phase 2a: All constraints (0-5 sec)
    result = _run_cp_sat_solver(
        remaining_students,
        all_available_slots,
        skeleton,
        constraints,
        timeout_sec=5.0,
        include_soft_constraints=True
    )
    
    if result.is_complete():
        result.metadata["phase"] = "2a_all_constraints"
        result.metadata["execution_time_sec"] = time_module.time() - start_time
        return result
    
    # Phase 2b: Hard constraints only (5-10 sec)
    elapsed = time_module.time() - start_time
    if elapsed < 10.0:
        result = _run_cp_sat_solver(
            remaining_students,
            all_available_slots,
            skeleton,
            constraints,
            timeout_sec=10.0 - elapsed,
            include_soft_constraints=False
        )
        
        if result.is_complete():
            result.metadata["phase"] = "2b_hard_only"
            result.metadata["execution_time_sec"] = time_module.time() - start_time
            return result
    
    # Phase 2c: Maximize placements (10-15 sec)
    elapsed = time_module.time() - start_time
    if elapsed < 15.0:
        result = _run_cp_sat_solver(
            remaining_students,
            all_available_slots,
            skeleton,
            constraints,
            timeout_sec=15.0 - elapsed,
            include_soft_constraints=False,
            maximize_placements=True
        )
    
    # Return best partial solution found
    result.metadata["phase"] = "2c_partial"
    result.metadata["execution_time_sec"] = time_module.time() - start_time
    return result


def _collect_available_slots(
    all_students: List[Student],
    skeleton: Dict[Slot, ScheduledClass],
    coach_reserved: List[Slot]
) -> List[Slot]:
    """Collect all unique available slots from students, excluding used ones.
    
    Args:
        all_students: List of all students
        skeleton: Skeleton schedule (slots already used)
        coach_reserved: Coach reserved slots (never used)
    
    Returns:
        List of available Slot objects
    """
    # Collect all unique slots from all students
    all_slots_set = set()
    for student in all_students:
        for slot in student.available_slots:
            all_slots_set.add(slot)
    
    # Remove skeleton slots
    skeleton_slots = set(skeleton.keys())
    all_slots_set -= skeleton_slots
    
    # Remove coach reserved slots
    reserved_set = set(coach_reserved)
    all_slots_set -= reserved_set
    
    return list(all_slots_set)


def _run_cp_sat_solver(
    students: List[Student],
    available_slots: List[Slot],
    skeleton: Dict[Slot, ScheduledClass],
    constraints: SchedulingConstraints,
    timeout_sec: float,
    include_soft_constraints: bool = True,
    maximize_placements: bool = False
) -> ScheduleResult:
    """Run OR-Tools CP-SAT solver with given parameters.
    
    Args:
        students: Students to place
        available_slots: Available slots for placement
        skeleton: Locked skeleton schedule
        constraints: Scheduling constraints
        timeout_sec: Timeout in seconds
        include_soft_constraints: Whether to include soft constraints
        maximize_placements: If True, maximize number of placements (partial solution)
    
    Returns:
        ScheduleResult with solution or partial solution
    """
    model = cp_model.CpModel()
    
    # Create variables: assignment[student_idx][slot_idx] = BoolVar
    num_students = len(students)
    num_slots = len(available_slots)
    
    assignments = {}
    for i in range(num_students):
        for j in range(num_slots):
            # Only create variable if student available for this slot
            student = students[i]
            slot = available_slots[j]
            
            if _is_student_available_for_slot(student, slot):
                assignments[(i, j)] = model.NewBoolVar(f"assign_s{i}_slot{j}")
    
    # HARD CONSTRAINTS
    
    # Constraint 1: Each student placed exactly sessions_per_week times
    for i, student in enumerate(students):
        student_vars = [assignments[(i, j)] for j in range(num_slots) if (i, j) in assignments]
        model.Add(sum(student_vars) == student.sessions_per_week)
    
    # Constraint 2: Slot capacity (2-3 students per class)
    slot_students = {}  # slot_idx → list of student vars assigned to this slot
    for (i, j), var in assignments.items():
        if j not in slot_students:
            slot_students[j] = []
        slot_students[j].append(var)
    
    for j, vars_list in slot_students.items():
        total_students = sum(vars_list)
        # Only enforce capacity if slot is used (at least 1 student)
        # We'll use: if any student assigned, then 2-3 students
        slot_used = model.NewBoolVar(f"slot{j}_used")
        model.Add(total_students >= 1).OnlyEnforceIf(slot_used)
        model.Add(total_students == 0).OnlyEnforceIf(slot_used.Not())
        
        # If slot used, enforce 2-3 students
        model.Add(total_students >= 2).OnlyEnforceIf(slot_used)
        model.Add(total_students <= 3).OnlyEnforceIf(slot_used)
    
    # Constraint 3: UN SEUL COURS À LA FOIS (no overlap between classes)
    # For each pair of slots that overlap, at most one can be used
    for j1 in range(num_slots):
        for j2 in range(j1 + 1, num_slots):
            slot1 = available_slots[j1]
            slot2 = available_slots[j2]
            
            if slot1.overlaps(slot2):
                # At most one of these slots can be used
                if j1 in slot_students and j2 in slot_students:
                    slot1_used = model.NewBoolVar(f"overlap_s{j1}_used")
                    slot2_used = model.NewBoolVar(f"overlap_s{j2}_used")
                    
                    # slot1_used iff any student in slot1
                    model.Add(sum(slot_students[j1]) >= 1).OnlyEnforceIf(slot1_used)
                    model.Add(sum(slot_students[j1]) == 0).OnlyEnforceIf(slot1_used.Not())
                    
                    # slot2_used iff any student in slot2
                    model.Add(sum(slot_students[j2]) >= 1).OnlyEnforceIf(slot2_used)
                    model.Add(sum(slot_students[j2]) == 0).OnlyEnforceIf(slot2_used.Not())
                    
                    # At most one can be used
                    model.Add(slot1_used + slot2_used <= 1)
    
    # Check overlap with skeleton slots
    for j in range(num_slots):
        slot = available_slots[j]
        for skeleton_slot in skeleton.keys():
            if slot.overlaps(skeleton_slot):
                # This available slot cannot be used
                if j in slot_students:
                    model.Add(sum(slot_students[j]) == 0)
    
    # Constraint 4: Linked groups (partial linking)
    student_name_to_idx = {s.name: i for i, s in enumerate(students)}
    
    for i, student in enumerate(students):
        if student.linked_group and student.linked_group in student_name_to_idx:
            linked_idx = student_name_to_idx[student.linked_group]
            linked_student = students[linked_idx]
            
            # Min sessions together = min(student.sessions, linked.sessions)
            min_together = min(student.sessions_per_week, linked_student.sessions_per_week)
            
            # For each slot where both are assigned, count as "together"
            together_vars = []
            for j in range(num_slots):
                if (i, j) in assignments and (linked_idx, j) in assignments:
                    both_assigned = model.NewBoolVar(f"together_s{i}_s{linked_idx}_slot{j}")
                    model.AddMultiplicationEquality(
                        both_assigned,
                        [assignments[(i, j)], assignments[(linked_idx, j)]]
                    )
                    together_vars.append(both_assigned)
            
            # At least min_together sessions together
            if together_vars:
                model.Add(sum(together_vars) >= min_together)
    
    # SOFT CONSTRAINTS (if enabled)
    objective_terms = []
    
    if include_soft_constraints:
        # Soft 1: Respect recurring habits (weight 10)
        # TODO: Implement if we have recurring habit data
        
        # Soft 2: Balance load per day (weight 5)
        # TODO: Implement day balance penalty
        
        # Soft 3: Fill existing classes 2→3 before new slot (weight 3)
        # Favor slots that already have 1-2 students from skeleton
        for j in slot_students:
            # Penalty for creating new slot vs filling existing
            objective_terms.append(-3 * sum(slot_students[j]))
    
    # OBJECTIVE
    if maximize_placements:
        # Maximize total placements (for partial solution)
        total_placements = sum(assignments.values())
        model.Maximize(total_placements)
    elif objective_terms:
        model.Maximize(sum(objective_terms))
    
    # SOLVE
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = timeout_sec
    
    status = solver.Solve(model)
    
    # EXTRACT SOLUTION
    return _extract_solution(
        solver,
        status,
        students,
        available_slots,
        assignments,
        skeleton,
        constraints
    )


def _is_student_available_for_slot(student: Student, slot: Slot) -> bool:
    """Check if student is available for a given slot."""
    return any(
        avail_slot.day == slot.day and
        avail_slot.start_time == slot.start_time and
        avail_slot.end_time == slot.end_time
        for avail_slot in student.available_slots
    )


def _extract_solution(
    solver: 'cp_model.CpSolver',
    status: int,
    students: List[Student],
    available_slots: List[Slot],
    assignments: Dict[Tuple[int, int], 'cp_model.IntVar'],
    skeleton: Dict[Slot, ScheduledClass],
    constraints: SchedulingConstraints
) -> ScheduleResult:
    """Extract solution from CP-SAT solver.
    
    Args:
        solver: CP-SAT solver
        status: Solve status
        students: List of students
        available_slots: List of available slots
        assignments: Assignment variables
        skeleton: Skeleton schedule
        constraints: Constraints
    
    Returns:
        ScheduleResult with schedule and unplaced students
    """
    # Start with skeleton
    final_schedule = list(skeleton.values())
    slot_to_students = {slot: list(cls.students) for slot, cls in skeleton.items()}
    
    placed_students = set()
    for cls in skeleton.values():
        placed_students.update(cls.students)
    
    unplaced = []
    
    if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
        # Extract assignments from solution
        for (i, j), var in assignments.items():
            if solver.Value(var) == 1:
                student = students[i]
                slot = available_slots[j]
                
                if slot not in slot_to_students:
                    slot_to_students[slot] = []
                slot_to_students[slot].append(student.name)
                placed_students.add(student.name)
        
        # Build ScheduledClass objects for new slots
        for slot, student_names in slot_to_students.items():
            if slot not in skeleton:  # Don't duplicate skeleton
                scheduled_class = ScheduledClass(
                    slot=slot,
                    students=student_names,
                    status=SlotStatus.PROPOSED
                )
                final_schedule.append(scheduled_class)
        
        # Find unplaced students
        for student in students:
            if student.name not in placed_students:
                unplaced_student = _generate_unplaced_explanation(
                    student,
                    available_slots,
                    slot_to_students,
                    constraints
                )
                unplaced.append(unplaced_student)
    
    else:  # INFEASIBLE or UNKNOWN
        # Return skeleton + generate explanations for all students
        for student in students:
            if student.name not in placed_students:
                unplaced_student = _generate_unplaced_explanation(
                    student,
                    available_slots,
                    slot_to_students,
                    constraints,
                    infeasible=True
                )
                unplaced.append(unplaced_student)
    
    return ScheduleResult(
        schedule=final_schedule,
        unplaced=unplaced,
        metadata={
            "solver_status": _status_to_string(status),
            "total_students": len(students),
            "placed_students": len(placed_students),
            "unplaced_students": len(unplaced)
        }
    )


def _generate_unplaced_explanation(
    student: Student,
    available_slots: List[Slot],
    slot_to_students: Dict[Slot, List[str]],
    constraints: SchedulingConstraints,
    infeasible: bool = False
) -> UnplacedStudent:
    """Generate human-readable explanation for unplaced student.
    
    Template-based (no LLM cost).
    """
    conflicts = []
    suggestions = []
    
    if infeasible:
        reason = "Aucune solution valide trouvée avec les contraintes actuelles"
        conflicts.append("Les contraintes sont trop strictes (groupes liés, disponibilités limitées)")
    else:
        reason = "Pas de créneau disponible respectant toutes les contraintes"
        
        # Check why student couldn't be placed
        # 1. Check if slots are full
        for slot in student.available_slots:
            if slot in slot_to_students:
                students_in_slot = slot_to_students[slot]
                if len(students_in_slot) >= 3:
                    conflicts.append(
                        f"{slot.day.capitalize()} {slot.start_time.strftime('%H:%M')} : "
                        f"déjà {len(students_in_slot)} élèves ({', '.join(students_in_slot[:3])})"
                    )
        
        # 2. Generate suggestions from available slots
        for slot in student.available_slots[:3]:  # Top 3 suggestions
            if slot not in slot_to_students or len(slot_to_students[slot]) < 3:
                suggestions.append(
                    f"Proposer {slot.day.capitalize()} {slot.start_time.strftime('%H:%M')} "
                    f"(disponible dans ses dispos)"
                )
    
    if not conflicts:
        conflicts.append("Contraintes incompatibles (vérifier groupes liés et disponibilités)")
    
    if not suggestions:
        suggestions.append("Contacter l'élève pour élargir ses disponibilités")
    
    return UnplacedStudent(
        student=student.name,
        reason=reason,
        conflicts=conflicts,
        suggestions=suggestions
    )


def _status_to_string(status: int) -> str:
    """Convert CP-SAT status to string."""
    if cp_model is None:
        return "UNKNOWN"
    
    status_map = {
        cp_model.OPTIMAL: "OPTIMAL",
        cp_model.FEASIBLE: "FEASIBLE",
        cp_model.INFEASIBLE: "INFEASIBLE",
        cp_model.MODEL_INVALID: "MODEL_INVALID",
        cp_model.UNKNOWN: "UNKNOWN"
    }
    return status_map.get(status, "UNKNOWN")


# ============================================================================
# PUBLIC API
# ============================================================================

def generate_schedule(
    students: List[Student],
    recurring_slots_path: Optional[str] = None,
    coach_reserved_slots: Optional[List[Slot]] = None
) -> ScheduleResult:
    """Main entry point for schedule generation.
    
    Args:
        students: List of all students with availabilities
        recurring_slots_path: Optional path to recurring slots CSV
        coach_reserved_slots: Optional list of coach reserved slots
    
    Returns:
        ScheduleResult with complete or partial schedule
    
    Raises:
        ValueError: If validation fails
    """
    if coach_reserved_slots is None:
        coach_reserved_slots = []
    
    # Phase 1: Load and validate skeleton
    skeleton_classes = []
    recurring_warnings = []
    
    if recurring_slots_path:
        # Parse recurring slots with warnings for single-student slots
        skeleton_classes, recurring_warnings = parse_recurring_slots_csv_with_warnings(
            recurring_slots_path,
            students
        )
        
        # Validate skeleton
        validation = validate_skeleton(skeleton_classes, students, coach_reserved_slots)
        if not validation.is_valid:
            raise ValueError(
                f"Skeleton validation failed:\n" + "\n".join(validation.errors)
            )
    
    # Build skeleton dictionary
    skeleton = place_recurring_slots(skeleton_classes)
    
    # Phase 2: OR-Tools optimization
    constraints = SchedulingConstraints(
        coach_reserved_slots=coach_reserved_slots,
        skeleton_classes=skeleton_classes
    )
    
    result = optimize_variations(students, skeleton, constraints)
    
    # Propagate warnings from recurring slots parsing
    result.warnings.extend(recurring_warnings)
    
    return result
