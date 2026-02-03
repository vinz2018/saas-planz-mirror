"""Tests for formatter module."""

import pytest
import json
import tempfile
from pathlib import Path
from datetime import time

from core.formatter import to_json, to_markdown, save_json, save_markdown, _get_status_emoji
from core.models import (
    ScheduleResult, ScheduledClass, UnplacedStudent, 
    Slot, SlotStatus
)


class TestToJson:
    """Tests for to_json function."""
    
    def test_empty_schedule(self):
        """Test JSON output for empty schedule."""
        result = ScheduleResult(schedule=[], unplaced=[])
        json_output = to_json(result)
        
        assert json_output["schedule"] == []
        assert json_output["unplaced"] == []
        assert json_output["summary"]["total_classes"] == 0
        assert json_output["summary"]["is_complete"] is True
    
    def test_schedule_with_classes(self):
        """Test JSON output with scheduled classes."""
        slot = Slot("lundi", time(8, 0), time(9, 0), is_recurring=True)
        scheduled_class = ScheduledClass(
            slot=slot,
            students=["Alice", "Bob"],
            status=SlotStatus.LOCKED
        )
        result = ScheduleResult(schedule=[scheduled_class], unplaced=[])
        
        json_output = to_json(result)
        
        assert len(json_output["schedule"]) == 1
        assert json_output["schedule"][0]["day"] == "lundi"
        assert json_output["schedule"][0]["start_time"] == "08:00"
        assert json_output["schedule"][0]["end_time"] == "09:00"
        assert json_output["schedule"][0]["students"] == ["Alice", "Bob"]
        assert json_output["schedule"][0]["status"] == "locked"
        assert json_output["schedule"][0]["is_recurring"] is True
        assert json_output["summary"]["total_classes"] == 1
    
    def test_schedule_with_unplaced(self):
        """Test JSON output with unplaced students."""
        unplaced = UnplacedStudent(
            student="Charlie",
            reason="No available slots",
            conflicts=["All slots full"],
            suggestions=["Expand availability"]
        )
        result = ScheduleResult(schedule=[], unplaced=[unplaced])
        
        json_output = to_json(result)
        
        assert len(json_output["unplaced"]) == 1
        assert json_output["unplaced"][0]["student"] == "Charlie"
        assert json_output["unplaced"][0]["reason"] == "No available slots"
        assert json_output["summary"]["is_complete"] is False


class TestToMarkdown:
    """Tests for to_markdown function."""
    
    def test_empty_schedule_markdown(self):
        """Test Markdown output for empty schedule."""
        result = ScheduleResult(schedule=[], unplaced=[])
        markdown = to_markdown(result)
        
        assert "# Planning Généré" in markdown
        assert "Cours planifiés :** 0" in markdown
        assert "Élèves non placés :** 0" in markdown
    
    def test_schedule_with_classes_markdown(self):
        """Test Markdown output with scheduled classes."""
        slot = Slot("mardi", time(17, 0), time(18, 0), is_recurring=False)
        scheduled_class = ScheduledClass(
            slot=slot,
            students=["Vincent", "Jerome"],
            status=SlotStatus.PROPOSED
        )
        result = ScheduleResult(schedule=[scheduled_class], unplaced=[])
        
        markdown = to_markdown(result)
        
        assert "### Mardi" in markdown
        assert "17:00-18:00" in markdown
        assert "Vincent" in markdown
        assert "Jerome" in markdown
        assert "✅" in markdown  # PROPOSED status emoji
    
    def test_schedule_with_warnings_markdown(self):
        """Test Markdown output with warnings."""
        result = ScheduleResult(
            schedule=[],
            unplaced=[],
            warnings=[{
                "type": "single_student_recurring",
                "slot": "lundi 08:00-09:00",
                "student": "Alice",
                "message": "Single student in recurring slot",
                "suggestions": ["Add Bob to this slot"]
            }]
        )
        
        markdown = to_markdown(result)
        
        assert "Avertissements" in markdown
        assert "lundi 08:00-09:00" in markdown
        assert "Alice" in markdown


class TestSaveFiles:
    """Tests for save_json and save_markdown functions."""
    
    def test_save_json(self, tmp_path):
        """Test saving schedule result as JSON file."""
        result = ScheduleResult(
            schedule=[],
            unplaced=[],
            metadata={"test": "value"}
        )
        
        output_path = tmp_path / "output.json"
        save_json(result, str(output_path))
        
        assert output_path.exists()
        with open(output_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        assert data["metadata"]["test"] == "value"
    
    def test_save_markdown(self, tmp_path):
        """Test saving schedule result as Markdown file."""
        result = ScheduleResult(schedule=[], unplaced=[])
        
        output_path = tmp_path / "output.md"
        save_markdown(result, str(output_path))
        
        assert output_path.exists()
        with open(output_path, 'r', encoding='utf-8') as f:
            content = f.read()
        assert "# Planning Généré" in content


class TestStatusEmoji:
    """Tests for _get_status_emoji function."""
    
    def test_locked_emoji(self):
        """Test emoji for LOCKED status."""
        assert _get_status_emoji(SlotStatus.LOCKED) == "🔒"
    
    def test_proposed_emoji(self):
        """Test emoji for PROPOSED status."""
        assert _get_status_emoji(SlotStatus.PROPOSED) == "✅"
    
    def test_needs_validation_emoji(self):
        """Test emoji for NEEDS_VALIDATION status."""
        assert _get_status_emoji(SlotStatus.NEEDS_VALIDATION) == "⚠️"
