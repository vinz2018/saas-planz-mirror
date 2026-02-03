"""Tests for CSV parser module."""

import pytest
from datetime import time
from pathlib import Path
import tempfile
import os

from core.parser import (
    parse_time,
    expand_time_range_to_slots,
    parse_csv,
    validate_linked_groups,
    parse_recurring_slots_csv,
    parse_recurring_slots_csv_with_warnings,
    ParseError
)
from core.models import Student, Slot, SlotStatus


class TestParseTime:
    """Tests for parse_time function."""
    
    def test_valid_hour(self):
        """Test parsing valid hour times."""
        assert parse_time("08:00") == time(8, 0)
        assert parse_time("17:00") == time(17, 0)
        assert parse_time("00:00") == time(0, 0)
        assert parse_time("23:00") == time(23, 0)
    
    def test_valid_half_hour(self):
        """Test parsing valid half-hour times."""
        assert parse_time("08:30") == time(8, 30)
        assert parse_time("17:30") == time(17, 30)
        assert parse_time("00:30") == time(0, 30)
    
    def test_invalid_minute_granularity(self):
        """Test rejection of invalid minute granularity."""
        with pytest.raises(ParseError, match="granularity"):
            parse_time("08:15")
        
        with pytest.raises(ParseError, match="granularity"):
            parse_time("10:45")
    
    def test_invalid_format(self):
        """Test rejection of invalid time format."""
        with pytest.raises(ParseError, match="Invalid time format"):
            parse_time("8h")
        
        with pytest.raises(ParseError, match="Invalid time format"):
            parse_time("8:00:00")


class TestExpandTimeRange:
    """Tests for expand_time_range_to_slots function."""
    
    def test_full_hour_range(self):
        """Test expansion of full-hour range."""
        slots = expand_time_range_to_slots("lundi", time(8, 0), time(19, 0))
        
        assert len(slots) == 11  # 08:00-09:00, 09:00-10:00, ..., 18:00-19:00
        assert slots[0].start_time == time(8, 0)
        assert slots[0].end_time == time(9, 0)
        assert slots[-1].start_time == time(18, 0)
        assert slots[-1].end_time == time(19, 0)
        assert all(s.day == "lundi" for s in slots)
    
    def test_half_hour_start(self):
        """Test expansion starting at :30."""
        slots = expand_time_range_to_slots("mardi", time(8, 30), time(19, 0))
        
        assert len(slots) == 11  # 08:30-09:30, 09:30-10:30, ..., 18:00-19:00
        assert slots[0].start_time == time(8, 30)
        assert slots[0].end_time == time(9, 30)
    
    def test_half_hour_end(self):
        """Test expansion ending at :30."""
        slots = expand_time_range_to_slots("mercredi", time(8, 0), time(19, 30))
        
        assert len(slots) == 12  # Includes 18:30-19:30
        assert slots[-1].start_time == time(18, 30)
        assert slots[-1].end_time == time(19, 30)
    
    def test_single_hour_slot(self):
        """Test single 1-hour slot."""
        slots = expand_time_range_to_slots("jeudi", time(17, 0), time(18, 0))
        
        assert len(slots) == 1
        assert slots[0].start_time == time(17, 0)
        assert slots[0].end_time == time(18, 0)
    
    def test_invalid_range(self):
        """Test rejection of invalid range (start >= end)."""
        with pytest.raises(ParseError, match="start .* must be before end"):
            expand_time_range_to_slots("vendredi", time(18, 0), time(17, 0))
        
        with pytest.raises(ParseError, match="start .* must be before end"):
            expand_time_range_to_slots("vendredi", time(18, 0), time(18, 0))


class TestParseCSV:
    """Tests for parse_csv function."""
    
    def test_valid_csv(self, tmp_path):
        """Test parsing valid CSV with multiple students."""
        csv_content = """nom,sessions_par_semaine,lundi_debut,lundi_fin,mardi_debut,mardi_fin,mercredi_debut,mercredi_fin,jeudi_debut,jeudi_fin,vendredi_debut,vendredi_fin,samedi_debut,samedi_fin,groupe_lie,notes
Vincent,2,,,17:00,18:30,,,,,12:00,13:30,,,jerome,
Jerome,1,,,17:00,18:30,,,,,,,,,vincent,Toujours avec Vincent
Hugo,2,08:00,09:00,,,,,08:00,09:00,,,,,,
"""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(csv_content)
        
        students = parse_csv(str(csv_file))
        
        assert len(students) == 3
        assert students[0].name == "Vincent"
        assert students[0].sessions_per_week == 2
        assert len(students[0].available_slots) >= 2  # mardi + vendredi slots
        assert students[0].linked_group == "jerome"
    
    def test_missing_required_column(self, tmp_path):
        """Test error on missing required column."""
        csv_content = """nom,sessions_par_semaine,lundi_debut,lundi_fin
Vincent,2,08:00,19:00
"""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(csv_content)
        
        with pytest.raises(ParseError, match="Missing required columns"):
            parse_csv(str(csv_file))
    
    def test_invalid_sessions_per_week(self, tmp_path):
        """Test error on invalid sessions_per_week."""
        csv_content = """nom,sessions_par_semaine,lundi_debut,lundi_fin,mardi_debut,mardi_fin,mercredi_debut,mercredi_fin,jeudi_debut,jeudi_fin,vendredi_debut,vendredi_fin,samedi_debut,samedi_fin,groupe_lie,notes
Vincent,0,08:00,19:00,,,,,,,,,,,,
"""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(csv_content)
        
        with pytest.raises(ParseError, match="sessions_par_semaine must be 1-7"):
            parse_csv(str(csv_file))
    
    def test_incomplete_time_range(self, tmp_path):
        """Test error when only debut or fin specified."""
        csv_content = """nom,sessions_par_semaine,lundi_debut,lundi_fin,mardi_debut,mardi_fin,mercredi_debut,mercredi_fin,jeudi_debut,jeudi_fin,vendredi_debut,vendredi_fin,samedi_debut,samedi_fin,groupe_lie,notes
Vincent,2,08:00,,,,,,,,,,,,,
"""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(csv_content)
        
        with pytest.raises(ParseError, match="incomplete time range"):
            parse_csv(str(csv_file))
    
    def test_no_availability_slots(self, tmp_path):
        """Test error when student has no availability."""
        csv_content = """nom,sessions_par_semaine,lundi_debut,lundi_fin,mardi_debut,mardi_fin,mercredi_debut,mercredi_fin,jeudi_debut,jeudi_fin,vendredi_debut,vendredi_fin,samedi_debut,samedi_fin,groupe_lie,notes
Vincent,2,,,,,,,,,,,,,
"""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(csv_content)
        
        with pytest.raises(ParseError, match="No availability slots"):
            parse_csv(str(csv_file))
    
    def test_insufficient_availability(self, tmp_path):
        """Test error when not enough slots for requested sessions."""
        csv_content = """nom,sessions_par_semaine,lundi_debut,lundi_fin,mardi_debut,mardi_fin,mercredi_debut,mercredi_fin,jeudi_debut,jeudi_fin,vendredi_debut,vendredi_fin,samedi_debut,samedi_fin,groupe_lie,notes
Vincent,5,08:00,09:00,,,,,,,,,,,,
"""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(csv_content)
        
        with pytest.raises(ParseError, match="Only 1 availability slots but requests 5"):
            parse_csv(str(csv_file))


class TestValidateLinkedGroups:
    """Tests for validate_linked_groups function."""
    
    def test_valid_reciprocal_link(self):
        """Test valid reciprocal linked group."""
        student1 = Student(
            name="Vincent",
            sessions_per_week=2,
            available_slots=[
                Slot("mardi", time(17, 0), time(18, 0)),
                Slot("vendredi", time(12, 0), time(13, 0))
            ],
            linked_group="Jerome"
        )
        student2 = Student(
            name="Jerome",
            sessions_per_week=1,
            available_slots=[
                Slot("mardi", time(17, 0), time(18, 0))
            ],
            linked_group="Vincent"
        )
        
        pairs = validate_linked_groups([student1, student2])
        
        assert len(pairs) == 1
        assert ("Vincent", "Jerome") in pairs or ("Jerome", "Vincent") in pairs
    
    def test_non_reciprocal_link(self):
        """Test error on non-reciprocal link."""
        student1 = Student(
            name="Vincent",
            sessions_per_week=2,
            available_slots=[Slot("mardi", time(17, 0), time(18, 0))],
            linked_group="Jerome"
        )
        student2 = Student(
            name="Jerome",
            sessions_per_week=1,
            available_slots=[Slot("mardi", time(17, 0), time(18, 0))],
            linked_group="Hugo"  # Not reciprocal!
        )
        student3 = Student(
            name="Hugo",
            sessions_per_week=1,
            available_slots=[Slot("lundi", time(8, 0), time(9, 0))],
            linked_group=None
        )
        
        with pytest.raises(ParseError, match="not reciprocal"):
            validate_linked_groups([student1, student2, student3])
    
    def test_no_overlapping_availability(self):
        """Test error when linked students have no overlapping availability."""
        student1 = Student(
            name="Vincent",
            sessions_per_week=2,
            available_slots=[
                Slot("lundi", time(8, 0), time(9, 0)),
                Slot("mardi", time(8, 0), time(9, 0))
            ],
            linked_group="Jerome"
        )
        student2 = Student(
            name="Jerome",
            sessions_per_week=1,
            available_slots=[
                Slot("jeudi", time(17, 0), time(18, 0)),
                Slot("vendredi", time(17, 0), time(18, 0))
            ],
            linked_group="Vincent"
        )
        
        with pytest.raises(ParseError, match="NO overlapping availability"):
            validate_linked_groups([student1, student2])
    
    def test_nonexistent_linked_student(self):
        """Test error when linked student doesn't exist."""
        student1 = Student(
            name="Vincent",
            sessions_per_week=2,
            available_slots=[Slot("mardi", time(17, 0), time(18, 0))],
            linked_group="Nonexistent"
        )
        
        with pytest.raises(ParseError, match="doesn't exist"):
            validate_linked_groups([student1])


class TestParseRecurringSlots:
    """Tests for parse_recurring_slots_csv function."""
    
    def test_valid_recurring_csv(self, tmp_path):
        """Test parsing valid recurring slots CSV."""
        # First create students
        students = [
            Student(
                name="Vincent",
                sessions_per_week=2,
                available_slots=[
                    Slot("mardi", time(17, 0), time(18, 0)),
                    Slot("vendredi", time(12, 0), time(13, 0))
                ]
            ),
            Student(
                name="Jerome",
                sessions_per_week=1,
                available_slots=[
                    Slot("mardi", time(17, 0), time(18, 0))
                ]
            )
        ]
        
        # Create recurring slots CSV
        csv_content = """nom,jour,heure_debut,heure_fin
Vincent,mardi,17:00,18:00
Jerome,mardi,17:00,18:00
"""
        csv_file = tmp_path / "recurring.csv"
        csv_file.write_text(csv_content)
        
        classes = parse_recurring_slots_csv(str(csv_file), students)
        
        assert len(classes) == 1  # One class with both students
        assert len(classes[0].students) == 2
        assert "Vincent" in classes[0].students
        assert "Jerome" in classes[0].students
        assert classes[0].slot.day == "mardi"
        assert classes[0].slot.is_recurring is True
    
    def test_student_not_in_main_csv(self, tmp_path):
        """Test error when recurring student not in main CSV."""
        students = [
            Student(
                name="Vincent",
                sessions_per_week=2,
                available_slots=[Slot("mardi", time(17, 0), time(18, 0))]
            )
        ]
        
        csv_content = """nom,jour,heure_debut,heure_fin
Nonexistent,mardi,17:00,18:00
"""
        csv_file = tmp_path / "recurring.csv"
        csv_file.write_text(csv_content)
        
        with pytest.raises(ParseError, match="not found in availability CSV"):
            parse_recurring_slots_csv(str(csv_file), students)
    
    def test_slot_not_in_availability(self, tmp_path):
        """Test error when recurring slot not in student's availability."""
        students = [
            Student(
                name="Vincent",
                sessions_per_week=2,
                available_slots=[Slot("mardi", time(17, 0), time(18, 0))]
            )
        ]
        
        # Try to place Vincent at a time he's not available
        csv_content = """nom,jour,heure_debut,heure_fin
Vincent,lundi,08:00,09:00
"""
        csv_file = tmp_path / "recurring.csv"
        csv_file.write_text(csv_content)
        
        with pytest.raises(ParseError, match="not in student's availability"):
            parse_recurring_slots_csv(str(csv_file), students)
    
    def test_capacity_violation(self, tmp_path):
        """Test error on capacity violation (> 3 students only, 1 student now accepted)."""
        students = [
            Student(
                name="Vincent",
                sessions_per_week=1,
                available_slots=[Slot("mardi", time(17, 0), time(18, 0))]
            )
        ]
        
        # 1 student is now accepted with NEEDS_VALIDATION status
        csv_content = """nom,jour,heure_debut,heure_fin
Vincent,mardi,17:00,18:00
"""
        csv_file = tmp_path / "recurring.csv"
        csv_file.write_text(csv_content)
        
        # Should NOT raise an error anymore
        classes = parse_recurring_slots_csv(str(csv_file), students)
        assert len(classes) == 1
        assert classes[0].status == SlotStatus.NEEDS_VALIDATION
    
    def test_recurring_single_student_generates_warnings(self, tmp_path):
        """Test that warnings are generated for single-student recurring slots."""
        students = [
            Student(
                name="Vincent",
                sessions_per_week=1,
                available_slots=[Slot("mardi", time(17, 0), time(18, 0))]
            ),
            Student(
                name="Jerome",
                sessions_per_week=1,
                available_slots=[Slot("mardi", time(17, 0), time(18, 0))]  # Same slot
            ),
            Student(
                name="Alice",
                sessions_per_week=1,
                available_slots=[Slot("lundi", time(10, 0), time(11, 0))]  # Different slot
            )
        ]
        
        # Vincent alone on mardi 17:00
        csv_content = """nom,jour,heure_debut,heure_fin
Vincent,mardi,17:00,18:00
"""
        csv_file = tmp_path / "recurring.csv"
        csv_file.write_text(csv_content)
        
        classes, warnings = parse_recurring_slots_csv_with_warnings(str(csv_file), students)
        
        # Should have 1 class with NEEDS_VALIDATION
        assert len(classes) == 1
        assert classes[0].status == SlotStatus.NEEDS_VALIDATION
        
        # Should have 1 warning
        assert len(warnings) == 1
        assert warnings[0]["type"] == "single_student_recurring"
        assert warnings[0]["student"] == "Vincent"
        assert "mardi" in warnings[0]["slot"]
        
        # Should suggest Jerome (available on same slot)
        assert len(warnings[0]["suggestions"]) > 0
        suggestions_text = " ".join(warnings[0]["suggestions"])
        assert "Jerome" in suggestions_text
    
    def test_recurring_single_student_no_compatible_students(self, tmp_path):
        """Test suggestions when no other students are available on the same slot."""
        students = [
            Student(
                name="Vincent",
                sessions_per_week=1,
                available_slots=[Slot("mardi", time(17, 0), time(18, 0))]
            ),
            Student(
                name="Alice",
                sessions_per_week=1,
                available_slots=[Slot("lundi", time(10, 0), time(11, 0))]  # Different slot
            )
        ]
        
        csv_content = """nom,jour,heure_debut,heure_fin
Vincent,mardi,17:00,18:00
"""
        csv_file = tmp_path / "recurring.csv"
        csv_file.write_text(csv_content)
        
        classes, warnings = parse_recurring_slots_csv_with_warnings(str(csv_file), students)
        
        assert len(warnings) == 1
        suggestions_text = " ".join(warnings[0]["suggestions"])
        assert "Aucun autre étudiant disponible" in suggestions_text
