#!/usr/bin/env python3
"""
Generate test case CSV files for Streamlit testing.
Creates 5 test cases with increasing complexity.
"""

import os
from pathlib import Path

# Base path
BASE_PATH = Path(__file__).parent.parent / "docs/examples/test-cases"

# Test cases data
test_cases = {
    "01-simple": {
        "disponibilites": """Nom,Lundi,Mardi,Mercredi,Jeudi,Vendredi,Samedi,Groupe_lié,Notes
Alice,08:00-12:00,,09:00-11:00,,,,,Débutante
Bob,,14:00-18:00,14:00-17:00,14:00-16:00,,,Charlie,Niveau intermédiaire
Charlie,,14:00-18:00,14:00-17:00,14:00-16:00,,,Bob,Niveau intermédiaire
David,,,,,08:00-12:00,09:00-13:00,,Expert
Emma,10:00-12:00,10:00-12:00,10:00-12:00,,,,,"Flexible, préfère le matin"
""",
        "recurring": """Jour,Heure_début,Heure_fin,Élèves,Notes
Lundi,08:00,09:00,"Alice, Emma",Cours habituel du lundi matin
Mardi,15:00,16:00,"Bob, Charlie",Groupe habituel mardi après-midi
"""
    }
}

def create_test_case(name, data):
    """Create CSV files for a test case."""
    case_dir = BASE_PATH / name
    case_dir.mkdir(parents=True, exist_ok=True)
    
    # Write disponibilites.csv
    (case_dir / "disponibilites.csv").write_text(data["disponibilites"])
    print(f"✅ {name}/disponibilites.csv")
    
    # Write recurring-slots.csv
    (case_dir / "recurring-slots.csv").write_text(data["recurring"])
    print(f"✅ {name}/recurring-slots.csv")

if __name__ == "__main__":
    print("Generating test case CSV files...")
    for name, data in test_cases.items():
        create_test_case(name, data)
    print("\n✅ Test cases generated successfully!")
    print(f"Location: {BASE_PATH}")
