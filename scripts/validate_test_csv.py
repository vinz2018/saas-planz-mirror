#!/usr/bin/env python3
"""
Script de validation des fichiers CSV de test cases.
Valide le format, les types, et la cohérence des données.

Usage:
    python scripts/validate_test_csv.py docs/examples/test-cases/01-simple/
    python scripts/validate_test_csv.py docs/examples/test-cases/  # Tous les test cases
"""

import sys
import os
import re
from pathlib import Path
from typing import List, Tuple, Dict, Optional
import argparse


# Constantes de validation
DISPONIBILITES_COLUMNS = [
    "nom", "sessions_par_semaine", 
    "lundi_debut", "lundi_fin",
    "mardi_debut", "mardi_fin",
    "mercredi_debut", "mercredi_fin",
    "jeudi_debut", "jeudi_fin",
    "vendredi_debut", "vendredi_fin",
    "samedi_debut", "samedi_fin",
    "groupe_lie", "notes"
]

RECURRING_COLUMNS = ["nom", "jour", "heure_debut", "heure_fin"]

VALID_DAYS = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]

TIME_PATTERN = re.compile(r'^([0-1][0-9]|2[0-3]):[0-5][0-9]$')


class ValidationError:
    """Représente une erreur de validation."""
    def __init__(self, file: str, line: int, column: Optional[str], message: str, severity: str = "error"):
        self.file = file
        self.line = line
        self.column = column
        self.message = message
        self.severity = severity  # "error" or "warning"
    
    def __str__(self):
        emoji = "❌" if self.severity == "error" else "⚠️"
        col_info = f" (colonne: {self.column})" if self.column else ""
        return f"{emoji} {self.file}:{self.line}{col_info} - {self.message}"


class ValidationReport:
    """Rapport de validation avec erreurs et warnings."""
    def __init__(self, test_case_path: str):
        self.test_case_path = test_case_path
        self.errors: List[ValidationError] = []
        self.warnings: List[ValidationError] = []
    
    def add_error(self, file: str, line: int, column: Optional[str], message: str):
        self.errors.append(ValidationError(file, line, column, message, "error"))
    
    def add_warning(self, file: str, line: int, column: Optional[str], message: str):
        self.warnings.append(ValidationError(file, line, column, message, "warning"))
    
    def is_valid(self) -> bool:
        return len(self.errors) == 0
    
    def print_report(self):
        print(f"\n{'='*80}")
        print(f"📋 Validation : {self.test_case_path}")
        print(f"{'='*80}\n")
        
        if not self.errors and not self.warnings:
            print("✅ Aucune erreur détectée ! Le test case est valide.\n")
            return
        
        if self.errors:
            print(f"❌ {len(self.errors)} erreur(s) bloquante(s) :\n")
            for error in self.errors:
                print(f"  {error}")
            print()
        
        if self.warnings:
            print(f"⚠️  {len(self.warnings)} avertissement(s) :\n")
            for warning in self.warnings:
                print(f"  {warning}")
            print()
        
        if self.errors:
            print("❌ VALIDATION ÉCHOUÉE - Corrigez les erreurs avant de tester.\n")
        else:
            print("⚠️  VALIDATION RÉUSSIE AVEC WARNINGS - Testable mais à améliorer.\n")


def count_csv_fields(line: str) -> int:
    """Compte le nombre de champs dans une ligne CSV (gestion basique des guillemets)."""
    # Simplification : on compte les virgules hors guillemets
    in_quotes = False
    field_count = 1  # Au moins un champ
    
    for char in line:
        if char == '"':
            in_quotes = not in_quotes
        elif char == ',' and not in_quotes:
            field_count += 1
    
    return field_count


def validate_time_format(time_str: str) -> bool:
    """Valide le format HH:MM (avec H = 00-23, M = 00-59)."""
    if not time_str or time_str.strip() == "":
        return True  # Les champs vides sont OK
    return TIME_PATTERN.match(time_str.strip()) is not None


def validate_disponibilites(file_path: Path, report: ValidationReport) -> Optional[Dict[str, List[str]]]:
    """
    Valide le fichier disponibilites.csv.
    Retourne un dict {nom: [disponibilités]} pour validation croisée, ou None si erreur.
    """
    if not file_path.exists():
        report.add_error(file_path.name, 0, None, "Fichier manquant")
        return None
    
    students_availability = {}
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    if len(lines) < 2:
        report.add_error(file_path.name, 0, None, "Fichier vide ou sans données")
        return None
    
    # Validation du header (ligne 1)
    header = lines[0].strip()
    header_fields = [field.strip() for field in header.split(',')]
    
    if header_fields != DISPONIBILITES_COLUMNS:
        report.add_error(file_path.name, 1, None, 
            f"Header incorrect. Attendu: {','.join(DISPONIBILITES_COLUMNS)}")
        # Afficher la différence
        missing = set(DISPONIBILITES_COLUMNS) - set(header_fields)
        extra = set(header_fields) - set(DISPONIBILITES_COLUMNS)
        if missing:
            report.add_error(file_path.name, 1, None, f"Colonnes manquantes: {missing}")
        if extra:
            report.add_error(file_path.name, 1, None, f"Colonnes en trop: {extra}")
    
    # Validation des données (lignes 2+)
    for line_num, line in enumerate(lines[1:], start=2):
        line = line.strip()
        if not line:
            continue  # Ligne vide OK
        
        # Vérification du nombre de champs
        field_count = count_csv_fields(line)
        if field_count != len(DISPONIBILITES_COLUMNS):
            report.add_error(file_path.name, line_num, None,
                f"Nombre de champs incorrect: {field_count} au lieu de {len(DISPONIBILITES_COLUMNS)}. "
                f"Vérifiez les virgules manquantes ou en trop.")
            continue
        
        # Parse la ligne
        fields = line.split(',')
        
        # Validation du nom
        nom = fields[0].strip()
        if not nom:
            report.add_error(file_path.name, line_num, "nom", "Nom vide")
            continue
        
        # Validation sessions_par_semaine
        sessions_str = fields[1].strip()
        try:
            sessions = int(sessions_str)
            if not (1 <= sessions <= 7):
                report.add_error(file_path.name, line_num, "sessions_par_semaine",
                    f"Valeur invalide: {sessions}. Doit être entre 1 et 7.")
        except ValueError:
            report.add_error(file_path.name, line_num, "sessions_par_semaine",
                f"Type invalide: '{sessions_str}'. Doit être un entier.")
        
        # Validation des heures (colonnes 2-13)
        day_pairs = [
            ("lundi", 2, 3), ("mardi", 4, 5), ("mercredi", 6, 7),
            ("jeudi", 8, 9), ("vendredi", 10, 11), ("samedi", 12, 13)
        ]
        
        student_slots = []
        for day, debut_idx, fin_idx in day_pairs:
            debut = fields[debut_idx].strip() if debut_idx < len(fields) else ""
            fin = fields[fin_idx].strip() if fin_idx < len(fields) else ""
            
            # Les deux doivent être remplis ou vides
            if (debut and not fin) or (not debut and fin):
                report.add_error(file_path.name, line_num, f"{day}_debut/{day}_fin",
                    f"Plage horaire incomplète pour {day}. Les deux champs doivent être remplis ou vides.")
            
            # Validation du format
            if debut and not validate_time_format(debut):
                report.add_error(file_path.name, line_num, f"{day}_debut",
                    f"Format d'heure invalide: '{debut}'. Attendu: HH:MM (ex: 08:00)")
            
            if fin and not validate_time_format(fin):
                report.add_error(file_path.name, line_num, f"{day}_fin",
                    f"Format d'heure invalide: '{fin}'. Attendu: HH:MM (ex: 12:00)")
            
            # Vérifier que debut < fin
            if debut and fin and validate_time_format(debut) and validate_time_format(fin):
                debut_minutes = int(debut.split(':')[0]) * 60 + int(debut.split(':')[1])
                fin_minutes = int(fin.split(':')[0]) * 60 + int(fin.split(':')[1])
                if debut_minutes >= fin_minutes:
                    report.add_error(file_path.name, line_num, f"{day}_debut/{day}_fin",
                        f"Incohérence: {day} {debut} >= {fin}. L'heure de début doit être avant l'heure de fin.")
                else:
                    student_slots.append((day, debut, fin))
        
        students_availability[nom] = student_slots
    
    return students_availability


def validate_recurring_slots(file_path: Path, students_availability: Optional[Dict[str, List[str]]], 
                             report: ValidationReport):
    """Valide le fichier recurring-slots.csv et la cohérence avec disponibilites.csv."""
    if not file_path.exists():
        report.add_warning(file_path.name, 0, None, "Fichier manquant (optionnel)")
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    if len(lines) < 1:
        report.add_warning(file_path.name, 0, None, "Fichier vide")
        return
    
    # Validation du header
    header = lines[0].strip()
    header_fields = [field.strip() for field in header.split(',')]
    
    if header_fields != RECURRING_COLUMNS:
        report.add_error(file_path.name, 1, None,
            f"Header incorrect. Attendu: {','.join(RECURRING_COLUMNS)}")
    
    # Validation des données
    for line_num, line in enumerate(lines[1:], start=2):
        line = line.strip()
        if not line:
            continue
        
        # Vérification du nombre de champs
        field_count = count_csv_fields(line)
        if field_count != len(RECURRING_COLUMNS):
            report.add_error(file_path.name, line_num, None,
                f"Nombre de champs incorrect: {field_count} au lieu de {len(RECURRING_COLUMNS)}")
            continue
        
        fields = line.split(',')
        
        nom = fields[0].strip()
        jour = fields[1].strip().lower()
        heure_debut = fields[2].strip()
        heure_fin = fields[3].strip()
        
        # Validation du nom (doit exister dans disponibilites.csv)
        if students_availability and nom not in students_availability:
            report.add_error(file_path.name, line_num, "nom",
                f"Étudiant '{nom}' non trouvé dans disponibilites.csv")
        
        # Validation du jour
        if jour not in VALID_DAYS:
            report.add_error(file_path.name, line_num, "jour",
                f"Jour invalide: '{jour}'. Doit être: {', '.join(VALID_DAYS)}")
        
        # Validation des heures
        if not validate_time_format(heure_debut):
            report.add_error(file_path.name, line_num, "heure_debut",
                f"Format d'heure invalide: '{heure_debut}'. Attendu: HH:MM")
        
        if not validate_time_format(heure_fin):
            report.add_error(file_path.name, line_num, "heure_fin",
                f"Format d'heure invalide: '{heure_fin}'. Attendu: HH:MM")
        
        # Vérifier la cohérence avec les disponibilités (le créneau récurrent doit être DANS une plage de dispo)
        if students_availability and nom in students_availability and validate_time_format(heure_debut) and validate_time_format(heure_fin):
            student_slots = students_availability[nom]
            
            # Convertir les heures en minutes
            rec_debut_min = int(heure_debut.split(':')[0]) * 60 + int(heure_debut.split(':')[1])
            rec_fin_min = int(heure_fin.split(':')[0]) * 60 + int(heure_fin.split(':')[1])
            
            # Vérifier si le créneau récurrent est dans une des disponibilités
            slot_found = False
            for day, debut, fin in student_slots:
                if day == jour:
                    dispo_debut_min = int(debut.split(':')[0]) * 60 + int(debut.split(':')[1])
                    dispo_fin_min = int(fin.split(':')[0]) * 60 + int(fin.split(':')[1])
                    
                    # Le créneau récurrent doit être DANS la plage de disponibilité
                    if rec_debut_min >= dispo_debut_min and rec_fin_min <= dispo_fin_min:
                        slot_found = True
                        break
            
            if not slot_found:
                report.add_error(file_path.name, line_num, None,
                    f"Créneau récurrent {jour} {heure_debut}-{heure_fin} "
                    f"non trouvé dans les disponibilités de {nom}")


def validate_test_case(test_case_path: Path) -> ValidationReport:
    """Valide un test case complet (disponibilites + recurring-slots)."""
    report = ValidationReport(str(test_case_path))
    
    dispo_file = test_case_path / "disponibilites.csv"
    recurring_file = test_case_path / "recurring-slots.csv"
    
    # Validation disponibilités
    students_availability = validate_disponibilites(dispo_file, report)
    
    # Validation recurring slots (avec validation croisée)
    validate_recurring_slots(recurring_file, students_availability, report)
    
    return report


def main():
    parser = argparse.ArgumentParser(
        description="Valide les fichiers CSV de test cases pour le scheduler"
    )
    parser.add_argument(
        "path",
        type=str,
        help="Chemin vers un test case ou un dossier contenant plusieurs test cases"
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Échouer si des warnings sont détectés"
    )
    
    args = parser.parse_args()
    
    path = Path(args.path)
    
    if not path.exists():
        print(f"❌ Erreur : Le chemin '{path}' n'existe pas.")
        sys.exit(1)
    
    # Déterminer les test cases à valider
    if path.is_dir():
        # Si c'est un dossier contenant des test cases
        if (path / "disponibilites.csv").exists():
            # C'est un test case unique
            test_cases = [path]
        else:
            # C'est un dossier parent contenant plusieurs test cases
            test_cases = [d for d in path.iterdir() if d.is_dir() and (d / "disponibilites.csv").exists()]
            test_cases.sort()
    else:
        print(f"❌ Erreur : '{path}' n'est pas un dossier.")
        sys.exit(1)
    
    if not test_cases:
        print(f"❌ Aucun test case trouvé dans '{path}'.")
        sys.exit(1)
    
    # Validation de tous les test cases
    all_valid = True
    reports = []
    
    for test_case in test_cases:
        report = validate_test_case(test_case)
        reports.append(report)
        
        if not report.is_valid():
            all_valid = False
        elif args.strict and report.warnings:
            all_valid = False
    
    # Affichage des rapports
    for report in reports:
        report.print_report()
    
    # Résumé global
    print(f"{'='*80}")
    print(f"📊 Résumé : {len(reports)} test case(s) validé(s)")
    print(f"{'='*80}\n")
    
    valid_count = sum(1 for r in reports if r.is_valid() and not r.warnings)
    warning_count = sum(1 for r in reports if r.is_valid() and r.warnings)
    error_count = sum(1 for r in reports if not r.is_valid())
    
    if valid_count:
        print(f"✅ {valid_count} test case(s) valide(s)")
    if warning_count:
        print(f"⚠️  {warning_count} test case(s) avec warnings")
    if error_count:
        print(f"❌ {error_count} test case(s) avec erreurs")
    
    print()
    
    if all_valid:
        print("✅ VALIDATION GLOBALE RÉUSSIE\n")
        sys.exit(0)
    else:
        print("❌ VALIDATION GLOBALE ÉCHOUÉE\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
