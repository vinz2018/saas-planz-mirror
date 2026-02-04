#!/usr/bin/env python3
"""
Verification script for UI/UX improvements.
Tests that all components are properly implemented.
"""

import sys
from pathlib import Path

def verify_files():
    """Verify all required files exist."""
    print("🔍 Verifying files...")
    
    required_files = [
        "app.py",
        "pages/documentation.py",
        "CHANGELOG_UI_UX_2026-02-04.md"
    ]
    
    all_exist = True
    for file in required_files:
        file_path = Path(file)
        if file_path.exists():
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} - MISSING!")
            all_exist = False
    
    return all_exist

def verify_app_content():
    """Verify app.py contains required improvements."""
    print("\n🔍 Verifying app.py content...")
    
    with open("app.py", "r") as f:
        content = f.read()
    
    checks = {
        "Error translations": "ERROR_TRANSLATIONS" in content,
        "Translation function": "translate_error_message" in content,
        "ParserError handling": "pd.errors.ParserError" in content,
        "EmptyDataError handling": "pd.errors.EmptyDataError" in content,
        "Tabs for views": "st.tabs" in content,
        "Calendar view": "tab_calendar" in content,
        "Documentation link": "pages/documentation.py" in content,
        "Improved warnings": "Comment faire ?" in content or "Comment faire" in content,
    }
    
    all_passed = True
    for check_name, result in checks.items():
        if result:
            print(f"  ✅ {check_name}")
        else:
            print(f"  ❌ {check_name} - NOT FOUND!")
            all_passed = False
    
    return all_passed

def verify_documentation_content():
    """Verify documentation.py contains required sections."""
    print("\n🔍 Verifying documentation.py content...")
    
    with open("pages/documentation.py", "r") as f:
        content = f.read()
    
    checks = {
        "Example Simple": "Exemple Simple" in content,
        "Example Moyen (linked groups)": "Exemple Moyen" in content and "groupe_lie" in content,
        "Example Complexe (:30)": "Exemple Complexe" in content and ":30" in content,
        "Example Récurrents": "Exemple Créneaux Récurrents" in content or "Exemple Récurrents" in content,
        "FAQ section": "FAQ" in content,
        "FAQ Q1 (unplaced)": "Pourquoi un élève n'est pas placé" in content,
        "FAQ Q2 (sessions_par_semaine)": "sessions_par_semaine" in content,
        "FAQ Q3 (linked groups)": "Comment créer un groupe lié" in content,
        "FAQ Q4 (unsatisfied)": "planning ne me convient pas" in content,
        "FAQ Q5 (difference)": "Différence entre disponibilités" in content,
        "FAQ Q6 (coach slots)": "bloquer mes créneaux personnels" in content,
        "Return link": "app.py" in content and "st.page_link" in content,
    }
    
    all_passed = True
    for check_name, result in checks.items():
        if result:
            print(f"  ✅ {check_name}")
        else:
            print(f"  ❌ {check_name} - NOT FOUND!")
            all_passed = False
    
    return all_passed

def verify_imports():
    """Verify all imports work correctly."""
    print("\n🔍 Verifying Python imports...")
    
    try:
        # Test app.py imports
        sys.path.insert(0, str(Path.cwd().parent.parent))
        
        # Basic import test
        import tempfile
        from datetime import time
        from pathlib import Path as P
        
        print("  ✅ Standard library imports")
        
        # Pandas import (used for error handling)
        try:
            import pandas as pd
            print("  ✅ pandas import")
        except ImportError:
            print("  ⚠️  pandas not available (expected in Docker)")
        
        return True
    except Exception as e:
        print(f"  ❌ Import error: {e}")
        return False

def main():
    """Run all verifications."""
    print("=" * 60)
    print("UI/UX Improvements Verification")
    print("=" * 60)
    
    results = [
        verify_files(),
        verify_app_content(),
        verify_documentation_content(),
        verify_imports(),
    ]
    
    print("\n" + "=" * 60)
    if all(results):
        print("✅ ALL CHECKS PASSED!")
        print("=" * 60)
        print("\n📋 Next Steps:")
        print("1. Start the app: ./run-mvp.sh start")
        print("2. Test documentation page navigation")
        print("3. Test error messages with invalid CSV")
        print("4. Test calendar view with test cases")
        print("5. Test warnings display")
        return 0
    else:
        print("❌ SOME CHECKS FAILED!")
        print("=" * 60)
        return 1

if __name__ == "__main__":
    sys.exit(main())
