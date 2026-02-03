"""
CSV parser for student availabilities and recurring slots.

This module is responsible for:
- Parsing availability CSV → List[Student]
- Parsing recurring slots CSV → List[ScheduledClass]
- Time range expansion (e.g., "08:00-19:00" → list of 1h slots)
- CSV format validation (field counts, time formats, etc.)
- Linked group validation (partial linking allowed)

Note: Contains one business logic function (parse_recurring_slots_csv_with_warnings)
that calls scheduler.generate_optimization_suggestions via local import to avoid
circular dependency.
"""

import logging
import pandas as pd
from datetime import time
from typing import List, Tuple, Optional, Dict, Any
from pathlib import Path

from .models import Student, Slot, ScheduledClass, SlotStatus

logger = logging.getLogger(__name__)


# French day names (lowercase) - dimanche excluded as coach doesn't work Sundays
VALID_DAYS = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi"]

# Required columns for availability CSV
AVAILABILITY_REQUIRED_COLUMNS = [
    "nom", "sessions_par_semaine",
    "lundi_debut", "lundi_fin",
    "mardi_debut", "mardi_fin",
    "mercredi_debut", "mercredi_fin",
    "jeudi_debut", "jeudi_fin",
    "vendredi_debut", "vendredi_fin",
    "samedi_debut", "samedi_fin",
    "groupe_lie", "notes"
]

# Required columns for recurring slots CSV
RECURRING_REQUIRED_COLUMNS = ["nom", "jour", "heure_debut", "heure_fin"]


class ParseError(Exception):
    """Custom exception for parsing errors with clear messages."""
    pass


def parse_time(time_str: str) -> time:
    """Parse time string in HH:MM format.
    
    Args:
        time_str: Time string like "08:00" or "17:30"
    
    Returns:
        datetime.time object
    
    Raises:
        ParseError: If format invalid or not :00 or :30
    """
    if pd.isna(time_str) or time_str == "":
        return None
    
    try:
        hour, minute = map(int, time_str.split(":"))
    except (ValueError, AttributeError):
        raise ParseError(f"Invalid time format: '{time_str}'. Expected HH:MM (e.g., '08:00', '17:30')")
    
    # Validate granularity (:00 or :30 only)
    if minute not in [0, 30]:
        raise ParseError(
            f"Invalid time granularity: '{time_str}'. "
            f"Times must end in :00 or :30 (not :{minute:02d})"
        )
    
    # Validate hour range
    if not (0 <= hour < 24):
        raise ParseError(f"Invalid hour: {hour}. Must be 0-23")
    
    return time(hour=hour, minute=minute)


def expand_time_range_to_slots(day: str, start_time: time, end_time: time) -> List[Slot]:
    """Expand a time range to list of 1-hour slots.
    
    Examples:
        08:00-19:00 → [08:00-09:00, 09:00-10:00, ..., 18:00-19:00] (11 slots)
        08:30-19:00 → [08:30-09:30, 09:30-10:30, ..., 18:00-19:00] (11 slots)
        08:00-19:30 → [08:00-09:00, 09:00-10:00, ..., 18:30-19:30] (12 slots)
    
    Args:
        day: Day name (lowercase French)
        start_time: Start of availability range
        end_time: End of availability range
    
    Returns:
        List of 1-hour Slot objects
    
    Raises:
        ParseError: If range invalid
    """
    if start_time >= end_time:
        raise ParseError(
            f"Invalid time range for {day}: start ({start_time}) must be before end ({end_time})"
        )
    
    slots = []
    current_start = start_time
    
    while True:
        # Calculate end time for 1-hour slot
        # 08:00 → 09:00, 08:30 → 09:30
        next_hour = current_start.hour + 1
        
        # Handle hour overflow (23:00 + 1h would be invalid)
        if next_hour > 23:
            break
        
        current_end = time(hour=next_hour, minute=current_start.minute)
        
        # Stop if we exceed the end time
        if current_end > end_time:
            break
        
        slot = Slot(
            day=day,
            start_time=current_start,
            end_time=current_end,
            is_recurring=False
        )
        slots.append(slot)
        
        # Move to next slot
        current_start = current_end
    
    return slots


def parse_csv(file_path: str) -> List[Student]:
    """Parse student availability CSV.
    
    Args:
        file_path: Path to CSV file with student availabilities
    
    Returns:
        List of Student objects
    
    Raises:
        ParseError: If CSV format invalid or validation fails
    """
    # Read CSV
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        raise ParseError(f"File not found: {file_path}")
    except pd.errors.ParserError as e:
        raise ParseError(f"Failed to parse CSV: {e}")
    
    # Validate required columns exist (case-sensitive)
    missing_cols = set(AVAILABILITY_REQUIRED_COLUMNS) - set(df.columns)
    if missing_cols:
        raise ParseError(
            f"Missing required columns: {', '.join(sorted(missing_cols))}. "
            f"Expected columns: {', '.join(AVAILABILITY_REQUIRED_COLUMNS)}"
        )
    
    students = []
    
    for idx, row in df.iterrows():
        try:
            # Parse basic info
            name = str(row["nom"]).strip()
            if not name or pd.isna(row["nom"]):
                raise ParseError(f"Row {idx+2}: Student name is required")
            
            sessions_per_week = int(row["sessions_par_semaine"])
            if sessions_per_week <= 0 or sessions_per_week > 7:
                raise ParseError(
                    f"Row {idx+2} ({name}): sessions_par_semaine must be 1-7, got {sessions_per_week}"
                )
            
            # Parse availability slots
            available_slots = []
            for day in ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi"]:
                debut_col = f"{day}_debut"
                fin_col = f"{day}_fin"
                
                debut_str = row[debut_col]
                fin_str = row[fin_col]
                
                # Skip if both empty
                if pd.isna(debut_str) and pd.isna(fin_str):
                    continue
                
                # Both must be filled if one is filled
                if pd.isna(debut_str) or pd.isna(fin_str):
                    raise ParseError(
                        f"Row {idx+2} ({name}): {day} has incomplete time range. "
                        f"Both {debut_col} and {fin_col} must be filled or both empty."
                    )
                
                # Parse times
                try:
                    debut_time = parse_time(debut_str)
                    fin_time = parse_time(fin_str)
                except ParseError as e:
                    raise ParseError(f"Row {idx+2} ({name}): {e}")
                
                # Expand range to hourly slots
                try:
                    day_slots = expand_time_range_to_slots(day, debut_time, fin_time)
                    available_slots.extend(day_slots)
                except ParseError as e:
                    raise ParseError(f"Row {idx+2} ({name}): {e}")
            
            # Check student has at least one availability slot
            if not available_slots:
                raise ParseError(
                    f"Row {idx+2} ({name}): No availability slots defined. "
                    f"Student must have at least one time range."
                )
            
            # Check enough availability for requested sessions
            if len(available_slots) < sessions_per_week:
                raise ParseError(
                    f"Row {idx+2} ({name}): Only {len(available_slots)} availability slots "
                    f"but requests {sessions_per_week} sessions/week. Need at least {sessions_per_week} slots."
                )
            
            # Parse linked group
            linked_group = row.get("groupe_lie")
            if pd.isna(linked_group) or linked_group == "":
                linked_group = None
            else:
                linked_group = str(linked_group).strip()
            
            # Parse notes
            notes = row.get("notes", "")
            if pd.isna(notes):
                notes = ""
            else:
                notes = str(notes).strip()
            
            # Create student
            student = Student(
                name=name,
                sessions_per_week=sessions_per_week,
                available_slots=available_slots,
                linked_group=linked_group,
                notes=notes
            )
            students.append(student)
            
        except ParseError:
            raise
        except Exception as e:
            raise ParseError(f"Row {idx+2}: Unexpected error: {e}")
    
    # Validate linked groups after all students parsed
    try:
        validate_linked_groups(students)
    except ParseError as e:
        raise ParseError(f"Linked group validation failed: {e}")
    
    return students


def validate_linked_groups(students: List[Student]) -> List[Tuple[str, str]]:
    """Validate linked groups have reciprocal links and overlapping availability.
    
    Args:
        students: List of all students
    
    Returns:
        List of validated linked pairs (student1, student2)
    
    Raises:
        ParseError: If linked groups invalid
    """
    # Build student lookup
    student_map = {s.name: s for s in students}
    validated_pairs = []
    processed = set()
    
    for student in students:
        if not student.linked_group:
            continue
        
        # Skip if already processed this pair
        pair_key = tuple(sorted([student.name, student.linked_group]))
        if pair_key in processed:
            continue
        processed.add(pair_key)
        
        # Check linked student exists
        if student.linked_group not in student_map:
            raise ParseError(
                f"{student.name} links to '{student.linked_group}' but that student doesn't exist in CSV"
            )
        
        linked_student = student_map[student.linked_group]
        
        # Check reciprocity
        if linked_student.linked_group != student.name:
            raise ParseError(
                f"{student.name} links to {student.linked_group}, "
                f"but {student.linked_group} links to '{linked_student.linked_group}' (not reciprocal). "
                f"Both students must link to each other."
            )
        
        # Check overlapping availability (REQUIRED for partial linking)
        if not student.has_overlapping_availability(linked_student):
            raise ParseError(
                f"{student.name} and {student.linked_group} have NO overlapping availability. "
                f"Linked groups must have at least one common time slot."
            )
        
        # Warn if sessions_per_week differ (partial linking will apply)
        if student.sessions_per_week != linked_student.sessions_per_week:
            # Log warning, not an error (partial linking supported)
            logger.warning(
                f"Partial linking: {student.name} ({student.sessions_per_week} sessions) "
                f"and {student.linked_group} ({linked_student.sessions_per_week} sessions) "
                f"have different session counts. "
                f"min({student.sessions_per_week}, {linked_student.sessions_per_week}) sessions together, rest solo."
            )
        
        validated_pairs.append((student.name, student.linked_group))
    
    return validated_pairs


def parse_recurring_slots_csv_with_warnings(
    file_path: str,
    all_students: List[Student]
) -> Tuple[List[ScheduledClass], List[Dict[str, Any]]]:
    """Parse recurring slots CSV and generate warnings for single-student slots.
    
    Args:
        file_path: Path to recurring slots CSV
        all_students: List of all students (for validation)
    
    Returns:
        Tuple of (scheduled_classes, warnings)
        - scheduled_classes: List of ScheduledClass objects
        - warnings: List of warning dictionaries for optimization
    
    Raises:
        ParseError: If CSV format invalid or validation fails
    """
    # Import here to avoid circular dependency
    from typing import Any, Dict
    
    # Parse recurring slots (now accepts 1 student with NEEDS_VALIDATION)
    scheduled_classes = parse_recurring_slots_csv(file_path, all_students)
    
    # Generate warnings for single-student slots
    # Import locally to avoid circular dependency (parser -> scheduler -> parser)
    from .scheduler import generate_optimization_suggestions
    
    warnings = []
    for scheduled_class in scheduled_classes:
        if scheduled_class.needs_optimization():
            suggestions = generate_optimization_suggestions(
                scheduled_class.slot,
                scheduled_class.students[0],
                all_students
            )
            
            warnings.append({
                "type": "single_student_recurring",
                "slot": f"{scheduled_class.slot.day} {scheduled_class.slot.start_time.strftime('%H:%M')}-{scheduled_class.slot.end_time.strftime('%H:%M')}",
                "student": scheduled_class.students[0],
                "message": f"Créneau récurrent avec 1 seul étudiant ({scheduled_class.students[0]})",
                "suggestions": suggestions
            })
    
    return scheduled_classes, warnings


def parse_recurring_slots_csv(file_path: str, all_students: List[Student]) -> List[ScheduledClass]:
    """Parse recurring slots CSV.
    
    Args:
        file_path: Path to recurring slots CSV
        all_students: List of all students (for validation)
    
    Returns:
        List of ScheduledClass objects with status=LOCKED or NEEDS_VALIDATION
    
    Raises:
        ParseError: If CSV format invalid or validation fails
    """
    # Read CSV
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        raise ParseError(f"File not found: {file_path}")
    except pd.errors.ParserError as e:
        raise ParseError(f"Failed to parse recurring slots CSV: {e}")
    
    # Validate required columns
    missing_cols = set(RECURRING_REQUIRED_COLUMNS) - set(df.columns)
    if missing_cols:
        raise ParseError(
            f"Recurring slots CSV missing columns: {', '.join(sorted(missing_cols))}. "
            f"Expected: nom, jour, heure_debut, heure_fin"
        )
    
    # Build student lookup
    student_map = {s.name: s for s in all_students}
    
    # Group by slot (same slot can have multiple students)
    slot_students = {}
    
    for idx, row in df.iterrows():
        try:
            # Parse student name
            name = str(row["nom"]).strip()
            if name not in student_map:
                raise ParseError(
                    f"Row {idx+2}: Student '{name}' not found in availability CSV"
                )
            
            # Parse day
            jour = str(row["jour"]).strip().lower()
            if jour not in VALID_DAYS:
                raise ParseError(
                    f"Row {idx+2} ({name}): Invalid day '{jour}'. "
                    f"Must be one of: {', '.join(VALID_DAYS)}"
                )
            
            # Parse times
            try:
                heure_debut = parse_time(row["heure_debut"])
                heure_fin = parse_time(row["heure_fin"])
            except ParseError as e:
                raise ParseError(f"Row {idx+2} ({name}): {e}")
            
            # Create slot
            slot = Slot(
                day=jour,
                start_time=heure_debut,
                end_time=heure_fin,
                is_recurring=True
            )
            
            # Validate slot
            if not slot.is_valid():
                raise ParseError(
                    f"Row {idx+2} ({name}): Invalid slot. "
                    f"Duration must be 1h and times must be :00 or :30"
                )
            
            # Check slot is within student's availability
            # Accept if the recurring slot is INCLUDED in any availability range
            student = student_map[name]
            
            # Get all availability slots for this day
            day_slots = [s for s in student.available_slots if s.day == jour]
            
            if not day_slots:
                raise ParseError(
                    f"Row {idx+2} ({name}): No availability on {jour}"
                )
            
            # Find min/max time for this day to determine availability range
            # This handles cases like 08:00-13:00 availability containing 08:30-09:30 recurring slot
            min_start = min(s.start_time for s in day_slots)
            max_end = max(s.end_time for s in day_slots)
            
            # Check if recurring slot is within this range
            if not (heure_debut >= min_start and heure_fin <= max_end):
                raise ParseError(
                    f"Row {idx+2} ({name}): Recurring slot {jour} {heure_debut}-{heure_fin} "
                    f"not within student's availability range ({min_start}-{max_end})"
                )
            
            # Group students by slot
            slot_key = (slot.day, slot.start_time, slot.end_time)
            if slot_key not in slot_students:
                slot_students[slot_key] = (slot, [])
            slot_students[slot_key][1].append(name)
            
        except ParseError:
            raise
        except Exception as e:
            raise ParseError(f"Row {idx+2}: Unexpected error: {e}")
    
    # Create ScheduledClass objects
    scheduled_classes = []
    for (day, start, end), (slot, students_names) in slot_students.items():
        # Validate capacity (max 3 students per class)
        if len(students_names) > 3:
            raise ParseError(
                f"Recurring slot {day} {start}-{end} has {len(students_names)} students. "
                f"Maximum 3 students per class."
            )
        
        # Status: LOCKED if 2-3 students, NEEDS_VALIDATION if 1 student
        status = SlotStatus.LOCKED if len(students_names) >= 2 else SlotStatus.NEEDS_VALIDATION
        
        scheduled_class = ScheduledClass(
            slot=slot,
            students=students_names,
            status=status
        )
        scheduled_classes.append(scheduled_class)
    
    return scheduled_classes
