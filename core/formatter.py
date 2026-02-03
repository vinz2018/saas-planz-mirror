"""
Output formatters for schedule results.

This module is responsible for:
- Converting ScheduleResult → JSON (machine-readable)
- Converting ScheduleResult → Markdown (human-readable)
- Formatting UnplacedStudent explanations
- Saving formatted output to files

Pure formatting module with no business logic.
"""

import json
from datetime import time, datetime
from typing import Dict, Any

from .models import ScheduleResult, ScheduledClass, UnplacedStudent, SlotStatus, Slot


# ============================================================================
# JSON FORMATTER
# ============================================================================

def to_json(schedule_result: ScheduleResult) -> Dict[str, Any]:
    """Convert ScheduleResult to JSON-serializable dictionary.
    
    Args:
        schedule_result: Schedule result to format
    
    Returns:
        Dictionary with structured schedule data
    """
    return {
        "metadata": schedule_result.metadata,
        "schedule": [
            {
                "day": cls.slot.day,
                "start_time": cls.slot.start_time.strftime("%H:%M"),
                "end_time": cls.slot.end_time.strftime("%H:%M"),
                "students": cls.students,
                "status": cls.status.value,
                "is_recurring": cls.slot.is_recurring
            }
            for cls in schedule_result.schedule
        ],
        "unplaced": [
            {
                "student": unp.student,
                "reason": unp.reason,
                "conflicts": unp.conflicts,
                "suggestions": unp.suggestions
            }
            for unp in schedule_result.unplaced
        ],
        "warnings": schedule_result.warnings,
        "explanations": schedule_result.explanations,
        "summary": {
            "total_classes": len(schedule_result.schedule),
            "total_unplaced": len(schedule_result.unplaced),
            "total_warnings": len(schedule_result.warnings),
            "placement_rate": schedule_result.placement_rate(),
            "is_complete": schedule_result.is_complete()
        }
    }


def save_json(schedule_result: ScheduleResult, file_path: str) -> None:
    """Save schedule result as JSON file.
    
    Args:
        schedule_result: Schedule result to save
        file_path: Output file path
    """
    data = to_json(schedule_result)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# ============================================================================
# MARKDOWN FORMATTER
# ============================================================================

def to_markdown(schedule_result: ScheduleResult) -> str:
    """Convert ScheduleResult to human-readable Markdown format.
    
    Visual table by day/time with emoji indicators:
    - 🔒 locked (recurring or manually locked)
    - ✅ proposed (algo suggestion)
    - ⚠️ needs_validation (conflicts detected)
    
    Args:
        schedule_result: Schedule result to format
    
    Returns:
        Markdown formatted string
    """
    lines = []
    
    # Header
    lines.append("# Planning Généré")
    lines.append("")
    lines.append(f"**Date de génération :** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append("")
    
    # Summary
    lines.append("## Résumé")
    lines.append("")
    lines.append(f"- **Cours planifiés :** {len(schedule_result.schedule)}")
    lines.append(f"- **Élèves non placés :** {len(schedule_result.unplaced)}")
    lines.append(f"- **Taux de placement :** {schedule_result.placement_rate():.1f}%")
    lines.append(f"- **Planning complet :** {'✅ Oui' if schedule_result.is_complete() else '⚠️ Non (solution partielle)'}")
    lines.append("")
    
    # Schedule by day
    lines.append("## Planning Hebdomadaire")
    lines.append("")
    
    # Group classes by day
    days_order = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi"]
    schedule_by_day = {day: [] for day in days_order}
    
    for cls in schedule_result.schedule:
        schedule_by_day[cls.slot.day].append(cls)
    
    # Sort classes by time within each day
    for day in days_order:
        schedule_by_day[day].sort(key=lambda cls: (cls.slot.start_time, cls.slot.end_time))
    
    # Render each day
    for day in days_order:
        classes = schedule_by_day[day]
        if not classes:
            continue
        
        lines.append(f"### {day.capitalize()}")
        lines.append("")
        
        for cls in classes:
            status_emoji = _get_status_emoji(cls.status)
            students_str = ", ".join(cls.students)
            time_str = f"{cls.slot.start_time.strftime('%H:%M')}-{cls.slot.end_time.strftime('%H:%M')}"
            
            lines.append(f"{status_emoji} **{time_str}** - {students_str} ({len(cls.students)} élèves)")
        
        lines.append("")
    
    # Warnings and Optimizations
    if schedule_result.warnings:
        lines.append("## ⚠️ Avertissements et Suggestions d'Optimisation")
        lines.append("")
        
        for warning in schedule_result.warnings:
            if warning["type"] == "single_student_recurring":
                lines.append(f"### Créneau à optimiser : {warning['slot']}")
                lines.append("")
                lines.append(f"**Étudiant actuel :** {warning['student']}")
                lines.append("")
                lines.append(f"⚠️ {warning['message']}")
                lines.append("")
                
                if warning.get("suggestions"):
                    lines.append("**Suggestions d'optimisation :**")
                    for suggestion in warning["suggestions"]:
                        lines.append(f"- {suggestion}")
                    lines.append("")
    
    # Unplaced students
    if schedule_result.unplaced:
        lines.append("## Élèves Non Placés")
        lines.append("")
        
        for unplaced in schedule_result.unplaced:
            lines.append(f"### {unplaced.student}")
            lines.append("")
            lines.append(f"**Raison :** {unplaced.reason}")
            lines.append("")
            
            if unplaced.conflicts:
                lines.append("**Conflits détectés :**")
                for conflict in unplaced.conflicts:
                    lines.append(f"- {conflict}")
                lines.append("")
            
            if unplaced.suggestions:
                lines.append("**Suggestions :**")
                for suggestion in unplaced.suggestions:
                    lines.append(f"- {suggestion}")
                lines.append("")
    
    # Metadata
    if schedule_result.metadata:
        lines.append("## Informations Techniques")
        lines.append("")
        for key, value in schedule_result.metadata.items():
            lines.append(f"- **{key}** : {value}")
        lines.append("")
    
    # Legend
    lines.append("## Légende")
    lines.append("")
    lines.append("- 🔒 **Verrouillé** : Créneau récurrent ou manuellement verrouillé")
    lines.append("- ✅ **Proposé** : Suggestion de l'algorithme")
    lines.append("- ⚠️ **À valider** : Conflits détectés, nécessite validation")
    lines.append("")
    
    return "\n".join(lines)


def save_markdown(schedule_result: ScheduleResult, file_path: str) -> None:
    """Save schedule result as Markdown file.
    
    Args:
        schedule_result: Schedule result to save
        file_path: Output file path
    """
    markdown = to_markdown(schedule_result)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(markdown)


# ============================================================================
# FORMATTING HELPERS
# ============================================================================

def format_unplaced_student(unplaced: UnplacedStudent) -> str:
    """Generate human-readable explanation for why student wasn't placed.
    
    Args:
        unplaced: UnplacedStudent instance with reason, conflicts, and suggestions
    
    Returns:
        Formatted string with explanation and suggestions
    """
    explanation = f"{unplaced.student} n'a pas pu être placé(e) car :\n"
    for conflict in unplaced.conflicts:
        explanation += f"- {conflict}\n"
    
    if unplaced.suggestions:
        explanation += "\nSuggestions :\n"
        for suggestion in unplaced.suggestions:
            explanation += f"- {suggestion}\n"
    
    return explanation


def _get_status_emoji(status: SlotStatus) -> str:
    """Get emoji for slot status."""
    emoji_map = {
        SlotStatus.LOCKED: "🔒",
        SlotStatus.PROPOSED: "✅",
        SlotStatus.NEEDS_VALIDATION: "⚠️"
    }
    return emoji_map.get(status, "❓")
