"""Tests for scheduler module."""

import pytest
from datetime import time

from core.scheduler import (
    validate_skeleton,
    place_recurring_slots,
    get_placed_students_from_skeleton
)
from core.models import Student, Slot, ScheduledClass, SlotStatus


class TestSkeletonValidation:
    """Tests for skeleton validation."""
    
    def test_valid_skeleton(self):
        """Test validation passes for valid skeleton."""
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
        
        assert validation.is_valid
        assert len(validation.errors) == 0
    
    def test_overlapping_courses_detected(self):
        """Test detection of overlapping courses."""
        students = [
            Student(
                name="Alice",
                sessions_per_week=1,
                available_slots=[Slot("lundi", time(8, 0), time(9, 0))]
            ),
            Student(
                name="Bob",
                sessions_per_week=1,
                available_slots=[Slot("lundi", time(8, 30), time(9, 30))]
            )
        ]
        
        skeleton = [
            ScheduledClass(
                slot=Slot("lundi", time(8, 0), time(9, 0)),
                students=["Alice", "Charlie"],
                status=SlotStatus.LOCKED
            ),
            ScheduledClass(
                slot=Slot("lundi", time(8, 30), time(9, 30)),
                students=["Bob", "David"],
                status=SlotStatus.LOCKED
            )
        ]
        
        validation = validate_skeleton(skeleton, students, coach_reserved=[])
        
        assert not validation.is_valid
        assert len(validation.errors) > 0
