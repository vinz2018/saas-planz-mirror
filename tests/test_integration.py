"""Integration tests for end-to-end CSV parsing workflow."""

import pytest
from pathlib import Path

from core.parser import parse_csv, parse_recurring_slots_csv, ParseError
from core.models import Slot, SlotStatus


class TestEndToEndParsing:
    """Test complete parsing workflow with realistic fixtures."""
    
    def test_parse_full_schedule_fixture(self, fixtures_dir):
        """Test parsing complete schedule fixture with 10 students."""
        csv_path = fixtures_dir / "test_schedule.csv"
        
        students = parse_csv(str(csv_path))
        
        # Verify basic parsing
        assert len(students) == 10
        
        # Verify specific students
        vincent = next(s for s in students if s.name == "Vincent")
        assert vincent.sessions_per_week == 2
        assert vincent.linked_group == "jerome"
        assert len(vincent.available_slots) > 0
        
        jerome = next(s for s in students if s.name == "Jerome")
        assert jerome.linked_group == "vincent"
        
        # Verify linked groups are reciprocal
        assert vincent.linked_group.lower() == jerome.name.lower()
        
        # Verify overlapping availability for linked group
        assert vincent.has_overlapping_availability(jerome)
        overlapping = vincent.get_overlapping_slots(jerome)
        assert len(overlapping) > 0
    
    def test_parse_recurring_slots_fixture(self, fixtures_dir):
        """Test parsing recurring slots with real fixture."""
        # First parse students
        schedule_path = fixtures_dir / "test_schedule.csv"
        students = parse_csv(str(schedule_path))
        
        # Parse recurring slots
        recurring_path = fixtures_dir / "test_recurring_slots.csv"
        scheduled_classes = parse_recurring_slots_csv(str(recurring_path), students)
        
        # Verify scheduled classes
        assert len(scheduled_classes) == 2  # 2 unique slots (Vincent+Jerome on mardi, Hugo+Juliette on lundi)
        
        # Check first class (Vincent + Jerome on mardi 17:00)
        mardi_class = next(c for c in scheduled_classes if c.slot.day == "mardi")
        assert len(mardi_class.students) == 2
        assert "Vincent" in mardi_class.students
        assert "Jerome" in mardi_class.students
        assert mardi_class.status == SlotStatus.LOCKED
        assert mardi_class.slot.is_recurring is True
        
        # Check second class (Hugo + Juliette on lundi 08:00)
        lundi_class = next(c for c in scheduled_classes if c.slot.day == "lundi")
        assert len(lundi_class.students) == 2
        assert "Hugo" in lundi_class.students
        assert "Juliette" in lundi_class.students
    
    def test_linked_groups_validation(self, fixtures_dir):
        """Test that linked groups are properly validated."""
        csv_path = fixtures_dir / "test_schedule.csv"
        students = parse_csv(str(csv_path))
        
        # Check Vincent and Jerome
        vincent = next(s for s in students if s.name == "Vincent")
        jerome = next(s for s in students if s.name == "Jerome")
        
        assert vincent.has_overlapping_availability(jerome)
        
        # Check Caroline and Franck
        caroline = next(s for s in students if s.name == "Caroline")
        franck = next(s for s in students if s.name == "Franck")
        
        assert caroline.has_overlapping_availability(franck)
    
    def test_slot_expansion(self, fixtures_dir):
        """Test that time ranges are properly expanded to 1-hour slots."""
        csv_path = fixtures_dir / "test_schedule.csv"
        students = parse_csv(str(csv_path))
        
        # Sarah has lundi 08:00-19:00 (should be 11 slots)
        sarah = next(s for s in students if s.name == "Sarah")
        lundi_slots = [s for s in sarah.available_slots if s.day == "lundi"]
        
        # 08:00-09:00, 09:00-10:00, ..., 18:00-19:00 = 11 slots
        assert len(lundi_slots) == 11
        
        # Verify first and last slot
        assert lundi_slots[0].start_time.hour == 8
        assert lundi_slots[0].end_time.hour == 9
        assert lundi_slots[-1].start_time.hour == 18
        assert lundi_slots[-1].end_time.hour == 19
        
        # Verify all slots are 1 hour
        for slot in lundi_slots:
            assert slot.duration_hours() == 1.0
            assert slot.is_valid()
    
    def test_no_overlapping_recurring_slots(self, fixtures_dir):
        """Test that recurring slots don't overlap (UN SEUL COURS À LA FOIS)."""
        schedule_path = fixtures_dir / "test_schedule.csv"
        students = parse_csv(str(schedule_path))
        
        recurring_path = fixtures_dir / "test_recurring_slots.csv"
        scheduled_classes = parse_recurring_slots_csv(str(recurring_path), students)
        
        # Check no overlaps between any pair of classes
        for i, class1 in enumerate(scheduled_classes):
            for class2 in scheduled_classes[i+1:]:
                # Classes should not overlap
                assert not class1.slot.overlaps(class2.slot), (
                    f"Classes overlap: {class1.slot.day} {class1.slot.start_time}-{class1.slot.end_time} "
                    f"and {class2.slot.day} {class2.slot.start_time}-{class2.slot.end_time}"
                )


class TestEdgeCases:
    """Test edge cases and error handling."""
    
    def test_half_hour_boundaries(self, tmp_path):
        """Test slots with :30 start times."""
        csv_content = """nom,sessions_par_semaine,lundi_debut,lundi_fin,mardi_debut,mardi_fin,mercredi_debut,mercredi_fin,jeudi_debut,jeudi_fin,vendredi_debut,vendredi_fin,samedi_debut,samedi_fin,groupe_lie,notes
Alice,2,08:30,10:30,,,,,,,,,,,,
"""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(csv_content)
        
        students = parse_csv(str(csv_file))
        
        assert len(students) == 1
        alice = students[0]
        
        # Should have 2 slots: 08:30-09:30, 09:30-10:30
        lundi_slots = [s for s in alice.available_slots if s.day == "lundi"]
        assert len(lundi_slots) == 2
        assert lundi_slots[0].start_time.minute == 30
        assert lundi_slots[1].start_time.minute == 30
    
    def test_partial_linking_different_sessions(self, tmp_path):
        """Test partial linking when students have different sessions_per_week."""
        csv_content = """nom,sessions_par_semaine,lundi_debut,lundi_fin,mardi_debut,mardi_fin,mercredi_debut,mercredi_fin,jeudi_debut,jeudi_fin,vendredi_debut,vendredi_fin,samedi_debut,samedi_fin,groupe_lie,notes
Alice,3,08:00,19:00,,,,,,,,,,,,bob,
Bob,1,08:00,19:00,,,,,,,,,,,,alice,
"""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(csv_content)
        
        # Should succeed with warning (partial linking)
        students = parse_csv(str(csv_file))
        
        assert len(students) == 2
        alice = next(s for s in students if s.name == "Alice")
        bob = next(s for s in students if s.name == "Bob")
        
        # Should have overlapping availability
        assert alice.has_overlapping_availability(bob)
        
        # But different session counts (partial linking will be handled by scheduler)
        assert alice.sessions_per_week == 3
        assert bob.sessions_per_week == 1
