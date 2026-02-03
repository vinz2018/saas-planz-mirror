#!/usr/bin/env python3
"""
Manual test for scheduler skeleton functions (no OR-Tools required).
"""

import sys
from pathlib import Path
from datetime import time

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.scheduler import (
    validate_skeleton,
    place_recurring_slots,
    get_placed_students_from_skeleton
)
from core.models import Student, Slot, ScheduledClass, SlotStatus

print("=" * 70)
print("TESTING SCHEDULER SKELETON (NO OR-TOOLS)")
print("=" * 70)

# Test 1: Valid skeleton
print("\n[TEST 1] Valid skeleton validation")
print("-" * 70)

students = [
    Student(
        name="Alice",
        sessions_per_week=1,
        available_slots=[Slot("lundi", time(8, 0), time(9, 0))]
    ),
    Student(
        name="Bob",
        sessions_per_week=1,
        available_slots=[Slot("lundi", time(8, 0), time(9, 0))]
    )
]

skeleton = [
    ScheduledClass(
        slot=Slot("lundi", time(8, 0), time(9, 0)),
        students=["Alice", "Bob"],
        status=SlotStatus.LOCKED
    )
]

validation = validate_skeleton(skeleton, students, coach_reserved=[])

assert validation.is_valid, f"Validation should pass: {validation.errors}"
assert len(validation.errors) == 0
print("✅ Valid skeleton passes validation")

# Test 2: Overlapping courses detected
print("\n[TEST 2] Overlapping courses detection (UN SEUL COURS À LA FOIS)")
print("-" * 70)

students2 = [
    Student(
        name="Charlie",
        sessions_per_week=1,
        available_slots=[Slot("lundi", time(8, 0), time(9, 0)), Slot("lundi", time(8, 30), time(9, 30))]
    ),
    Student(
        name="David",
        sessions_per_week=1,
        available_slots=[Slot("lundi", time(8, 0), time(9, 0)), Slot("lundi", time(8, 30), time(9, 30))]
    ),
    Student(
        name="Eve",
        sessions_per_week=1,
        available_slots=[Slot("lundi", time(8, 0), time(9, 0)), Slot("lundi", time(8, 30), time(9, 30))]
    ),
    Student(
        name="Frank",
        sessions_per_week=1,
        available_slots=[Slot("lundi", time(8, 0), time(9, 0)), Slot("lundi", time(8, 30), time(9, 30))]
    )
]

skeleton_overlap = [
    ScheduledClass(
        slot=Slot("lundi", time(8, 0), time(9, 0)),
        students=["Charlie", "David"],
        status=SlotStatus.LOCKED
    ),
    ScheduledClass(
        slot=Slot("lundi", time(8, 30), time(9, 30)),
        students=["Eve", "Frank"],
        status=SlotStatus.LOCKED
    )
]

validation2 = validate_skeleton(skeleton_overlap, students2, coach_reserved=[])

assert not validation2.is_valid, "Overlapping courses should fail validation"
assert len(validation2.errors) > 0
assert any("overlap" in err.lower() for err in validation2.errors)
print(f"✅ Overlapping courses detected: {validation2.errors[0]}")

# Test 3: Back-to-back courses (should be valid)
print("\n[TEST 3] Back-to-back courses (no overlap with half-open intervals)")
print("-" * 70)

skeleton_backtoback = [
    ScheduledClass(
        slot=Slot("lundi", time(8, 0), time(9, 0)),
        students=["Charlie", "David"],
        status=SlotStatus.LOCKED
    ),
    ScheduledClass(
        slot=Slot("lundi", time(9, 0), time(10, 0)),
        students=["Eve", "Frank"],
        status=SlotStatus.LOCKED
    )
]

validation3 = validate_skeleton(skeleton_backtoback, students2, coach_reserved=[])

assert validation3.is_valid, f"Back-to-back should be valid: {validation3.errors}"
print("✅ Back-to-back courses (09:00-10:00, 09:00-10:00) are valid (no overlap)")

# Test 4: Capacity violations
print("\n[TEST 4] Capacity violations")
print("-" * 70)

skeleton_low_capacity = [
    ScheduledClass(
        slot=Slot("lundi", time(8, 0), time(9, 0)),
        students=["Alice"],
        status=SlotStatus.LOCKED
    )
]

validation4 = validate_skeleton(skeleton_low_capacity, students, coach_reserved=[])

assert not validation4.is_valid
assert any("minimum 2" in err.lower() for err in validation4.errors)
print(f"✅ Low capacity detected: {validation4.errors[0]}")

# Test 5: place_recurring_slots
print("\n[TEST 5] place_recurring_slots()")
print("-" * 70)

skeleton_dict = place_recurring_slots(skeleton)

assert isinstance(skeleton_dict, dict)
assert len(skeleton_dict) == 1
assert Slot("lundi", time(8, 0), time(9, 0)) in skeleton_dict
print(f"✅ Skeleton dictionary created with {len(skeleton_dict)} slot(s)")

# Test 6: get_placed_students_from_skeleton
print("\n[TEST 6] get_placed_students_from_skeleton()")
print("-" * 70)

placed_counts = get_placed_students_from_skeleton(skeleton_dict)

assert "Alice" in placed_counts
assert "Bob" in placed_counts
assert placed_counts["Alice"] == 1
assert placed_counts["Bob"] == 1
print(f"✅ Placed counts: {placed_counts}")

# Test 7: Coach reserved slots conflict
print("\n[TEST 7] Coach reserved slots conflict")
print("-" * 70)

coach_reserved = [Slot("lundi", time(8, 0), time(9, 0))]

validation5 = validate_skeleton(skeleton, students, coach_reserved=coach_reserved)

assert not validation5.is_valid
assert any("coach reserved" in err.lower() for err in validation5.errors)
print(f"✅ Coach reserved conflict detected: {validation5.errors[0]}")

# Test 8: Student not in availability
print("\n[TEST 8] Student not in CSV")
print("-" * 70)

skeleton_bad_student = [
    ScheduledClass(
        slot=Slot("lundi", time(8, 0), time(9, 0)),
        students=["Alice", "Nonexistent"],
        status=SlotStatus.LOCKED
    )
]

validation6 = validate_skeleton(skeleton_bad_student, students, coach_reserved=[])

assert not validation6.is_valid
assert any("not found" in err for err in validation6.errors)
print(f"✅ Missing student detected: {validation6.errors[0]}")

print("\n" + "=" * 70)
print("✅ ALL SCHEDULER SKELETON TESTS PASSED")
print("=" * 70)
print("\nSkeleton validation is working correctly!")
print("OR-Tools optimization can now be tested once ortools is installed.")
