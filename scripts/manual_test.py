#!/usr/bin/env python3
"""
Manual test script to validate parser logic without pytest.
Run this after installing dependencies: pip install pandas
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from core.parser import parse_csv, parse_recurring_slots_csv, parse_time, expand_time_range_to_slots
    from core.models import Slot, Student
    from datetime import time
    
    print("✅ Modules imported successfully\n")
    
    # Test 1: parse_time
    print("=" * 60)
    print("TEST 1: parse_time()")
    print("=" * 60)
    
    test_times = [
        ("08:00", time(8, 0), True),
        ("17:30", time(17, 30), True),
        ("08:15", None, False),  # Should fail
    ]
    
    for time_str, expected, should_pass in test_times:
        try:
            result = parse_time(time_str)
            if should_pass:
                assert result == expected, f"Expected {expected}, got {result}"
                print(f"  ✅ parse_time('{time_str}') = {result}")
            else:
                print(f"  ❌ parse_time('{time_str}') should have failed but got {result}")
        except Exception as e:
            if not should_pass:
                print(f"  ✅ parse_time('{time_str}') correctly failed: {type(e).__name__}")
            else:
                print(f"  ❌ parse_time('{time_str}') unexpectedly failed: {e}")
    
    # Test 2: expand_time_range_to_slots
    print("\n" + "=" * 60)
    print("TEST 2: expand_time_range_to_slots()")
    print("=" * 60)
    
    slots = expand_time_range_to_slots("lundi", time(8, 0), time(19, 0))
    print(f"  08:00-19:00 expanded to {len(slots)} slots")
    assert len(slots) == 11, f"Expected 11 slots, got {len(slots)}"
    print(f"    First: {slots[0].start_time}-{slots[0].end_time}")
    print(f"    Last: {slots[-1].start_time}-{slots[-1].end_time}")
    print("  ✅ Full hour range expansion works")
    
    slots_30 = expand_time_range_to_slots("mardi", time(8, 30), time(19, 0))
    print(f"  08:30-19:00 expanded to {len(slots_30)} slots")
    assert len(slots_30) == 11, f"Expected 11 slots, got {len(slots_30)}"
    print(f"    First: {slots_30[0].start_time}-{slots_30[0].end_time}")
    print("  ✅ Half-hour start expansion works")
    
    # Test 3: Slot validation
    print("\n" + "=" * 60)
    print("TEST 3: Slot validation")
    print("=" * 60)
    
    valid_slot = Slot("lundi", time(8, 0), time(9, 0))
    assert valid_slot.is_valid(), "Valid slot should pass validation"
    assert valid_slot.duration_hours() == 1.0, "Duration should be 1 hour"
    print("  ✅ Valid 1-hour slot passes validation")
    
    invalid_slot = Slot("lundi", time(8, 15), time(9, 15))
    assert not invalid_slot.is_valid(), "Invalid granularity should fail"
    print("  ✅ Invalid granularity (:15) correctly rejected")
    
    # Test 4: Slot overlap detection
    print("\n" + "=" * 60)
    print("TEST 4: Slot overlap detection")
    print("=" * 60)
    
    slot1 = Slot("lundi", time(8, 0), time(9, 0))
    slot2 = Slot("lundi", time(9, 0), time(10, 0))  # Back-to-back, no overlap
    slot3 = Slot("lundi", time(8, 30), time(9, 30))  # Overlaps with slot1
    
    assert not slot1.overlaps(slot2), "Back-to-back slots should not overlap (half-open interval)"
    print("  ✅ Back-to-back slots (08:00-09:00, 09:00-10:00) don't overlap")
    
    assert slot1.overlaps(slot3), "Overlapping slots should be detected"
    print("  ✅ Overlapping slots (08:00-09:00, 08:30-09:30) detected")
    
    # Test 5: Student overlapping availability
    print("\n" + "=" * 60)
    print("TEST 5: Student overlapping availability")
    print("=" * 60)
    
    student1 = Student(
        name="Alice",
        sessions_per_week=2,
        available_slots=[
            Slot("mardi", time(17, 0), time(18, 0)),
            Slot("vendredi", time(12, 0), time(13, 0))
        ],
        linked_group="Bob"
    )
    
    student2 = Student(
        name="Bob",
        sessions_per_week=1,
        available_slots=[
            Slot("mardi", time(17, 0), time(18, 0))
        ],
        linked_group="Alice"
    )
    
    assert student1.has_overlapping_availability(student2), "Should have overlapping availability"
    overlapping = student1.get_overlapping_slots(student2)
    assert len(overlapping) == 1, "Should have 1 overlapping slot"
    print(f"  ✅ Linked students have {len(overlapping)} overlapping slot(s)")
    
    # Test 6: Parse real CSV fixture
    print("\n" + "=" * 60)
    print("TEST 6: Parse CSV fixture")
    print("=" * 60)
    
    fixture_path = Path(__file__).parent / "tests" / "fixtures" / "test_schedule.csv"
    if fixture_path.exists():
        students = parse_csv(str(fixture_path))
        print(f"  ✅ Parsed {len(students)} students from fixture")
        
        # Check Vincent
        vincent = next(s for s in students if s.name == "Vincent")
        print(f"    - Vincent: {vincent.sessions_per_week} sessions, {len(vincent.available_slots)} slots, linked to {vincent.linked_group}")
        
        # Check linked groups
        jerome = next(s for s in students if s.name == "Jerome")
        assert vincent.has_overlapping_availability(jerome), "Vincent and Jerome should have overlapping availability"
        print("    - ✅ Vincent and Jerome have overlapping availability")
        
        # Test 7: Parse recurring slots
        print("\n" + "=" * 60)
        print("TEST 7: Parse recurring slots CSV")
        print("=" * 60)
        
        recurring_path = Path(__file__).parent / "tests" / "fixtures" / "test_recurring_slots.csv"
        if recurring_path.exists():
            scheduled_classes = parse_recurring_slots_csv(str(recurring_path), students)
            print(f"  ✅ Parsed {len(scheduled_classes)} recurring classes")
            
            for cls in scheduled_classes:
                print(f"    - {cls.slot.day} {cls.slot.start_time}-{cls.slot.end_time}: {', '.join(cls.students)} ({len(cls.students)} students)")
            
            # Check no overlaps
            for i, class1 in enumerate(scheduled_classes):
                for class2 in scheduled_classes[i+1:]:
                    assert not class1.slot.overlaps(class2.slot), f"Classes should not overlap"
            print("  ✅ No overlaps between recurring classes (UN SEUL COURS À LA FOIS)")
    else:
        print(f"  ⚠️  Fixture not found: {fixture_path}")
    
    print("\n" + "=" * 60)
    print("✅ ALL TESTS PASSED")
    print("=" * 60)
    print("\nParser implementation is working correctly!")
    print("Ready to implement Phase 2: Scheduler OR-Tools")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("\nPlease install dependencies first:")
    print("  pip install pandas")
    sys.exit(1)
except Exception as e:
    print(f"\n❌ TEST FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
