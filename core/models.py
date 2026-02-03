"""
Data models for the scheduling system.

This module contains all data structures (dataclasses) used across the system:
- Slot: Time slot representation
- Student: Student information with availability
- ScheduledClass: A scheduled class with assigned students
- ScheduleResult: Complete scheduling output with metadata
- UnplacedStudent: Student that couldn't be placed
- SlotStatus: Enum for class status
- ValidationResult: Skeleton validation output
- SchedulingConstraints: Algorithm constraints

Uses dataclasses for Python 3.10+ with type hints.
"""

from dataclasses import dataclass, field
from datetime import time
from typing import List, Optional, Dict, Any
from enum import Enum


class SlotStatus(Enum):
    """Status of a scheduled class."""
    LOCKED = "locked"  # Recurring or manually locked
    PROPOSED = "proposed"  # Algorithm suggestion
    NEEDS_VALIDATION = "needs_validation"  # Has conflicts


@dataclass
class ValidationResult:
    """Result of skeleton validation."""
    is_valid: bool
    errors: List[str]
    warnings: List[str]


@dataclass
class SchedulingConstraints:
    """Constraints for the scheduling algorithm."""
    coach_reserved_slots: List['Slot']  # Slots reserved by coach (never used)
    skeleton_classes: List['ScheduledClass']  # Recurring/locked classes
    min_students_per_class: int = 2
    max_students_per_class: int = 3
    max_timeout_sec: float = 15.0  # Progressive timeout strategy


@dataclass
class Slot:
    """Represents a time slot for a class.
    
    Time interval semantics: Half-open intervals [start, end)
    Example: 09:00-10:00 means starts at 09:00:00, ends at 09:59:59
    """
    day: str  # lowercase French day name: lundi, mardi, mercredi, jeudi, vendredi, samedi (no dimanche)
    start_time: time
    end_time: time
    is_recurring: bool = False
    
    def duration_hours(self) -> float:
        """Calculate duration in hours. Must be exactly 1h for valid courses."""
        start_minutes = self.start_time.hour * 60 + self.start_time.minute
        end_minutes = self.end_time.hour * 60 + self.end_time.minute
        return (end_minutes - start_minutes) / 60.0
    
    def is_valid(self) -> bool:
        """Validate slot: duration must be 1h, times must be :00 or :30."""
        # Check duration
        if abs(self.duration_hours() - 1.0) > 0.01:  # Allow small float errors
            return False
        
        # Check granularity (:00 or :30 only)
        if self.start_time.minute not in [0, 30]:
            return False
        if self.end_time.minute not in [0, 30]:
            return False
        
        # Check start < end
        if self.start_time >= self.end_time:
            return False
        
        return True
    
    def overlaps(self, other: 'Slot') -> bool:
        """Check if this slot overlaps with another slot on the same day.
        
        Uses half-open interval logic: [start, end)
        Overlap check: start1 < end2 AND start2 < end1
        """
        if self.day != other.day:
            return False
        
        # Convert to minutes for comparison
        self_start_min = self.start_time.hour * 60 + self.start_time.minute
        self_end_min = self.end_time.hour * 60 + self.end_time.minute
        other_start_min = other.start_time.hour * 60 + other.start_time.minute
        other_end_min = other.end_time.hour * 60 + other.end_time.minute
        
        return self_start_min < other_end_min and other_start_min < self_end_min
    
    def __hash__(self):
        """Make Slot hashable for use in dicts/sets."""
        return hash((self.day, self.start_time, self.end_time))
    
    def __eq__(self, other):
        """Equality check for Slot."""
        if not isinstance(other, Slot):
            return False
        return (self.day == other.day and 
                self.start_time == other.start_time and 
                self.end_time == other.end_time)


@dataclass
class Student:
    """Represents a student with their availability and constraints."""
    name: str
    sessions_per_week: int
    available_slots: List[Slot] = field(default_factory=list)
    linked_group: Optional[str] = None  # Name of linked student (partial linking supported)
    notes: str = ""
    
    def has_overlapping_availability(self, other: 'Student') -> bool:
        """Check if this student has overlapping availability with another student.
        Required for linked groups (partial linking).
        """
        for slot1 in self.available_slots:
            for slot2 in other.available_slots:
                # Check if slots are on same day and same time
                if (slot1.day == slot2.day and 
                    slot1.start_time == slot2.start_time and 
                    slot1.end_time == slot2.end_time):
                    return True
        return False
    
    def get_overlapping_slots(self, other: 'Student') -> List[Slot]:
        """Get list of slots where both students are available."""
        overlapping = []
        for slot1 in self.available_slots:
            for slot2 in other.available_slots:
                if (slot1.day == slot2.day and 
                    slot1.start_time == slot2.start_time and 
                    slot1.end_time == slot2.end_time):
                    overlapping.append(slot1)
                    break
        return overlapping


@dataclass
class ScheduledClass:
    """Represents a scheduled class with students assigned."""
    slot: Slot
    students: List[str]  # Student names
    status: SlotStatus = SlotStatus.PROPOSED
    
    def is_full(self) -> bool:
        """Check if class has max capacity (3 students)."""
        return len(self.students) >= 3
    
    def is_valid(self) -> bool:
        """Check if class meets capacity constraints (2-3 students)."""
        return 2 <= len(self.students) <= 3
    
    def needs_optimization(self) -> bool:
        """Check if class needs optimization (< 2 students).
        
        Returns True if the class has less than 2 students and should be
        flagged for optimization (adding more students).
        """
        return len(self.students) < 2


@dataclass
class UnplacedStudent:
    """Represents a student that couldn't be placed in the schedule."""
    student: str
    reason: str
    conflicts: List[str] = field(default_factory=list)  # List of conflicting constraints
    suggestions: List[str] = field(default_factory=list)  # Alternative slots or actions


@dataclass
class ScheduleResult:
    """Complete result of scheduling algorithm including metadata and explanations."""
    schedule: List[ScheduledClass]
    unplaced: List[UnplacedStudent] = field(default_factory=list)
    warnings: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    explanations: Dict[str, Any] = field(default_factory=dict)
    
    def placement_rate(self) -> float:
        """Calculate percentage of students successfully placed.
        
        Returns percentage of individual student placements vs total needed.
        """
        # Count actual students placed (may appear in multiple classes)
        placed_count = sum(len(c.students) for c in self.schedule)
        unplaced_count = len(self.unplaced)
        total = placed_count + unplaced_count
        
        if total == 0:
            return 0.0
        
        return (placed_count / total) * 100.0
    
    def is_complete(self) -> bool:
        """Check if all students were successfully placed."""
        return len(self.unplaced) == 0
