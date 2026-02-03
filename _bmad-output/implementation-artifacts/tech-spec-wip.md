---
title: 'Refactoring Clean Code & Nettoyage Documentation'
slug: 'refactoring-clean-code-docs'
created: '2026-02-03'
status: 'in-progress'
stepsCompleted: [1, 2, 3]
tech_stack: ['Python 3.10+', 'pandas', 'ortools', 'streamlit', 'pytest']
files_to_modify: ['core/models.py', 'core/parser.py', 'core/scheduler.py']
code_patterns: ['dataclasses with validation methods', 'SRP violations detected', 'formatting in models', 'business logic in parser']
test_patterns: ['pytest with fixtures', 'tests separated by module', 'parametrized tests']
---

# Tech-Spec: Refactoring Clean Code & Nettoyage Documentation

**Created:** 2026-02-03

## Overview

### Problem Statement

Après le développement rapide du MVP avec Streamlit et 6 test cases validés (01-simple à 05-extrême + demo-warnings), le code fonctionne mais présente des opportunités d'amélioration :

**Code :**
- Les responsabilités des modules `core/` (models, parser, scheduler, formatter) peuvent être mieux définies et clarifiées
- Potentiels chevauchements de responsabilités à identifier et résoudre

**Documentation :**
- Fichiers obsolètes : `docs/email-tony-presentation.*` (déjà envoyé)
- Logs temporaires : `docs/reorganization/` (9 fichiers de status/summary de sessions passées)
- Documentation Docker dispersée : 4 fichiers séparés (GUIDE, QUICKSTART, RECAP, SETUP)
- Doublons : Multiples QUICKSTART et README à différents niveaux

**Objectif :** Clarifier le code et la documentation avant de repasser l'app à Tony pour validation.

### Solution

**Phase 1 : Refactoring Code**
- Analyser les responsabilités actuelles de chaque module `core/`
- Identifier et éliminer les chevauchements
- Clarifier les frontières entre modules
- S'assurer du respect du principe de responsabilité unique (SRP)
- **Contrainte : Aucun changement de logique métier, seulement organisation**

**Phase 2 : Nettoyage Documentation**
- **Supprimer :**
  - `docs/email-tony-presentation.md` et `.txt`
  - Tout le dossier `docs/reorganization/` (9 fichiers)
- **Fusionner :**
  - Les 4 fichiers `docs/docker/*` en un seul `docs/DOCKER.md`
  - Les multiples QUICKSTART/README en un guide unifié
- **Résultat :** Documentation claire, concise, sans redondance

**Phase 3 : Validation**
- Re-tester les 6 test cases dans Streamlit pour garantir la non-régression
- Vérifier que tous les tests unitaires passent

### Scope

**In Scope:**
- Refactoring des responsabilités dans les modules `core/` sans changer la logique métier
- Suppression des fichiers obsolètes et logs temporaires
- Fusion de la documentation Docker
- Unification des guides QUICKSTART/README
- Validation que les 6 test cases fonctionnent toujours
- Validation que les tests unitaires passent

**Out of Scope:**
- Changement d'architecture majeur (pas de passage à Hexagonal/DDD/CQRS)
- Modification de la logique métier ou des features
- Ajout de nouvelles fonctionnalités
- Migration vers un autre framework/librairie
- Optimisation de performance (hors scope sauf si critique)

## Context for Development

### Codebase Patterns

**Structure actuelle du projet :**
```
saas-planz/
├── core/                      # Modules métier (5 fichiers Python)
│   ├── __init__.py
│   ├── models.py              # Dataclasses (Student, Slot, ScheduledClass, ScheduleResult)
│   ├── parser.py              # Parsing CSV → objets Python
│   ├── scheduler.py           # Algorithme OR-Tools (2 phases : Squelette + Variations)
│   ├── formatter.py           # Formatage output (JSON + Markdown)
│   └── README.md
├── apps/
│   └── mvp-streamlit/         # Interface Streamlit
│       ├── app.py
│       ├── Dockerfile
│       └── docker-compose.yml
├── tests/                     # Tests unitaires + intégration
│   ├── test_parser.py
│   ├── test_scheduler.py
│   ├── test_formatter.py
│   └── test_integration.py
├── scripts/                   # Utilitaires
│   ├── validate_test_csv.py
│   └── README.md
├── docs/                      # Documentation (À NETTOYER)
│   ├── email-tony-*           ← À SUPPRIMER
│   ├── reorganization/        ← À SUPPRIMER (9 fichiers)
│   ├── docker/                ← À FUSIONNER (4 → 1 fichier)
│   ├── examples/
│   │   └── test-cases/        ← 6 test cases (GARDER)
│   ├── QUICKSTART.md          ← À UNIFIER
│   └── README.md              ← À UNIFIER
└── README.md                  ← Root README
```

**Patterns identifiés (à préserver) :**
- **Dataclasses** pour les modèles (Python 3.10+)
- **Séparation des concerns** : models / parser / scheduler / formatter
- **OR-Tools CP-SAT** pour l'optimisation (2 phases)
- **Pandas** pour le parsing CSV
- **Pytest** pour les tests

**Problèmes d'architecture détectés (Investigation Step 2) :**

**🔴 Problème 1 : Formatting dans models.py**
- `UnplacedStudent.to_human_readable()` (lignes 152-163) génère du Markdown
- Violation SRP : logique de formatting dans un modèle de données
- **Solution :** Déplacer vers `formatter.py`

**🟡 Problème 2 : Logique métier dans parser.py**
- `_generate_suggestions_for_single_student_slot()` (lignes 325-376) trouve des étudiants compatibles
- Questionnable : logique de suggestion/optimisation, pas du parsing pur
- **Solution :** Déplacer vers `scheduler.py` (ou nouveau module `suggestions.py`)

**🟡 Problème 3 : Dataclasses dans scheduler.py**
- `ValidationResult` et `SchedulingConstraints` (lignes 20-35) sont des modèles
- Questionnable : modèles de données définis dans le scheduler
- **Solution :** Déplacer vers `models.py` pour centraliser tous les modèles

**✅ Points positifs :**
- `formatter.py` est pur (pas de logique métier)
- `app.py` est une UI propre (pas de logique métier)
- Tests bien structurés et séparés par module

### Files to Reference

| File | Lines | Purpose | Problèmes Détectés |
| ---- | ----- | ------- | ------------------ |
| `core/models.py` | 192 | Dataclasses : Student, Slot, ScheduledClass, ScheduleResult, UnplacedStudent, SlotStatus (enum) | 🔴 `UnplacedStudent.to_human_readable()` fait du formatting |
| `core/parser.py` | 553 | Parse CSV → List[Student], parse recurring slots, validation format | 🟡 `_generate_suggestions_for_single_student_slot()` est de la logique métier |
| `core/scheduler.py` | 762 | Algorithme 2 phases (Squelette + OR-Tools), contraintes hard/soft, validation | 🟡 Contient `ValidationResult` et `SchedulingConstraints` (dataclasses) |
| `core/formatter.py` | 221 | ScheduleResult → JSON + Markdown | ✅ Pur formatting, aucun problème |
| `apps/mvp-streamlit/app.py` | 401 | Interface utilisateur Streamlit | ✅ UI pure, aucun problème |
| `tests/test_parser.py` | ~439 | Tests unitaires du parser | ✅ Bien structurés |
| `tests/test_scheduler.py` | ~77+ | Tests unitaires du scheduler | ✅ Bien structurés |
| `tests/test_formatter.py` | ~165 | Tests unitaires du formatter | ✅ Bien structurés |
| `docs/examples/test-cases/` | - | 6 test cases validés (01 à 05 + demo-warnings) | ✅ Bien organisés |

### Technical Decisions

**Décision 1 : Refactoring sans changement de logique**
- **Pourquoi :** MVP fonctionnel validé avec 6 test cases
- **Approche :** Améliorer l'organisation sans risquer de casser la logique
- **Validation :** Tests de non-régression après chaque changement

**Décision 2 : Suppression vs Archivage**
- **Supprimer directement :** 
  - `docs/email-tony-*` (obsolète, déjà envoyé)
  - `docs/reorganization/` (logs temporaires sans valeur future)
- **Pourquoi :** Alléger la documentation, pas besoin d'archive Git (déjà dans l'historique si besoin)

**Décision 3 : Fusion Documentation Docker**
- **Avant :** 4 fichiers (GUIDE, QUICKSTART, RECAP, SETUP)
- **Après :** 1 fichier `docs/DOCKER.md` avec sections claires
- **Pourquoi :** Éviter la confusion, un seul point d'entrée

**Décision 4 : Tests de validation obligatoires**
- Après chaque modification majeure, re-tester :
  1. `pytest tests/` (tous les tests unitaires)
  2. Les 6 test cases dans Streamlit (validation manuelle)
- **Seuil de succès :** 100% des tests passent, 100% des test cases fonctionnent

## Implementation Plan

> **Plan détaillé généré après investigation approfondie (Step 2)**

### Phase 1 : Refactoring Clean Code (Architecture)

**Objectif :** Respecter les principes SOLID, séparer les responsabilités (SRP), améliorer maintenabilité.

---

#### Task 1.1 : Déplacer `ValidationResult` et `SchedulingConstraints` → models.py

**Fichiers :**
- Source : `core/scheduler.py` (lignes 20-35)
- Destination : `core/models.py` (après `SlotStatus`)

**Actions :**
1. Couper les dataclasses `ValidationResult` et `SchedulingConstraints` de `scheduler.py`
2. Coller dans `models.py` après la définition de `SlotStatus` (ligne ~60)
3. Ajouter docstrings si manquantes
4. Mettre à jour les imports dans `scheduler.py` (ajout `from core.models import ValidationResult, SchedulingConstraints`)

**Justification :** Centraliser tous les modèles de données dans un seul fichier (SRP).

**Risque :** 🟢 Très faible (pas de logique, juste des dataclasses)

**Validation :**
- [ ] `pytest tests/test_scheduler.py -v` → 100% pass
- [ ] Vérifier import `ValidationResult` dans `scheduler.py`

---

#### Task 1.2 : Déplacer `_generate_suggestions_for_single_student_slot()` → scheduler.py

**Fichiers :**
- Source : `core/parser.py` (lignes 325-376)
- Destination : `core/scheduler.py` (nouvelle fonction publique)

**Actions :**
1. Renommer fonction : `_generate_suggestions_for_single_student_slot()` → `generate_optimization_suggestions()`
2. Déplacer vers `scheduler.py` (après `validate_skeleton`)
3. Modifier signature : `generate_optimization_suggestions(slot: Slot, students_in_class: List[Student], all_students: List[Student]) -> List[str]`
4. Mettre à jour l'appel dans `parser.py` :
   ```python
   from core.scheduler import generate_optimization_suggestions
   # Dans parse_recurring_slots_csv_with_warnings():
   suggestions = generate_optimization_suggestions(slot, students_for_slot, all_students)
   ```
5. Ajouter docstring publique (fonction devient partie de l'API `scheduler`)

**Justification :** Séparer parsing (parser) de logique métier/optimisation (scheduler). Les suggestions d'optimisation relèvent du scheduling, pas du parsing CSV.

**Risque :** 🟡 Moyen (changement de signature, imports à vérifier, appels à mettre à jour)

**Validation :**
- [ ] `pytest tests/test_parser.py -v` → 100% pass
- [ ] `pytest tests/test_scheduler.py -v` → 100% pass
- [ ] Tester `demo-warnings` dans Streamlit → Suggestions affichées correctement

---

#### Task 1.3 : Déplacer `UnplacedStudent.to_human_readable()` → formatter.py

**Fichiers :**
- Source : `core/models.py` (lignes 152-163)
- Destination : `core/formatter.py` (nouvelle fonction)

**Actions :**
1. Supprimer méthode `to_human_readable()` de la dataclass `UnplacedStudent`
2. Créer fonction `format_unplaced_student(unplaced: UnplacedStudent) -> str` dans `formatter.py`
3. Chercher tous les appels `.to_human_readable()` :
   ```bash
   grep -r "to_human_readable" core/ apps/ tests/
   ```
4. Mettre à jour les appels :
   ```python
   # Avant:
   unplaced.to_human_readable()
   # Après:
   from core.formatter import format_unplaced_student
   format_unplaced_student(unplaced)
   ```
5. Ajouter docstring pour la nouvelle fonction

**Justification :** Retirer toute logique de formatting des modèles (violation SRP). Les modèles doivent être des structures de données pures.

**Risque :** 🟢 Faible (fonction simple de formatting, peu d'appels)

**Validation :**
- [ ] `pytest tests/test_formatter.py -v` → 100% pass
- [ ] `pytest tests/test_models.py -v` → 100% pass (si existe)
- [ ] Vérifier Markdown généré identique (avant/après)

---

#### Task 1.4 : Cleanup imports, docstrings, type hints

**Fichiers :** `core/models.py`, `core/parser.py`, `core/scheduler.py`, `core/formatter.py`

**Actions :**
1. Vérifier tous les imports dans chaque fichier :
   - Supprimer imports inutilisés
   - Organiser par ordre : stdlib → third-party → local
2. Ajouter docstrings manquantes pour fonctions publiques :
   - Format : Description + Args + Returns + Raises
3. Vérifier cohérence des type hints :
   - Utiliser `List[...]`, `Optional[...]`, `Dict[...]` (Python 3.10+)
4. Ajouter module-level docstring si manquante :
   ```python
   """Module description.
   
   This module is responsible for...
   """
   ```

**Justification :** Améliorer lisibilité, maintenabilité, IDE support.

**Risque :** 🟢 Très faible

**Validation :**
- [ ] `pytest tests/ -v` → 100% pass
- [ ] Linter doit passer sans warnings (si configuré)

---

### Phase 2 : Nettoyage Documentation

**Objectif :** Supprimer obsolète, fusionner guides, améliorer structure.

---

#### Task 2.1 : Supprimer fichiers obsolètes

**Fichiers à supprimer :**
- `docs/email-tony-presentation.md`
- `docs/email-tony-presentation-plaintext.txt` (ou similaire)
- `docs/reorganization/` (dossier complet avec 9 fichiers de logs)

**Actions :**
1. Vérifier existence des fichiers :
   ```bash
   ls -la docs/email-tony*
   ls -la docs/reorganization/
   ```
2. Supprimer via Delete tool ou `rm -rf`
3. Commit avec message : "docs: remove obsolete files (email-tony, reorganization logs)"

**Justification :** Alléger repo, supprimer fichiers temporaires sans valeur future.

**Risque :** 🟢 Très faible (fichiers obsolètes confirmés)

**Validation :**
- [ ] Vérifier `docs/` ne contient plus ces fichiers
- [ ] Vérifier Git status montre bien les suppressions

---

#### Task 2.2 : Fusionner guides Docker → DOCKER.md

**Fichiers :**
- Sources : `docs/docker/DOCKER_SETUP_COMPLETE.md`, `DOCKER_QUICKSTART.md`, `DOCKER_GUIDE.md`, `DOCKER_RECAP.txt`
- Destination : `docs/DOCKER.md` (nouveau fichier unifié)

**Actions :**
1. Lire les 4 fichiers Docker pour analyser le contenu
2. Créer `docs/DOCKER.md` avec structure :
   ```markdown
   # Docker Setup & Guide
   
   ## 1. Installation Docker
   [From DOCKER_SETUP_COMPLETE.md]
   
   ## 2. Quickstart
   [From DOCKER_QUICKSTART.md]
   
   ## 3. Guide Complet
   [From DOCKER_GUIDE.md]
   
   ## 4. Récap Commandes
   [From DOCKER_RECAP.txt]
   
   ## 5. Troubleshooting
   ```
3. Supprimer dossier `docs/docker/` après fusion
4. Mettre à jour liens dans `README.md` si nécessaire

**Justification :** Guide Docker centralisé, éviter confusion avec multiples fichiers.

**Risque :** 🟢 Faible

**Validation :**
- [ ] `docs/DOCKER.md` contient toutes les infos
- [ ] `docs/docker/` n'existe plus
- [ ] Liens docs fonctionnent

---

#### Task 2.3 : Fusionner QUICKSTART.md et README.md

**Fichiers :**
- Sources : `docs/QUICKSTART.md`, `docs/README.md`
- Destination : `docs/README.md` (unifié)

**Actions :**
1. Lire `docs/QUICKSTART.md` et `docs/README.md`
2. Identifier sections communes et contenus dupliqués
3. Fusionner dans `docs/README.md` avec structure :
   ```markdown
   # SaaS Planz - Documentation
   
   ## Quickstart (5 minutes)
   [Contenu de QUICKSTART.md]
   
   ## Architecture
   [Structure du projet]
   
   ## Exemples et Test Cases
   [Lien vers examples/]
   
   ## Tests
   [Comment tester]
   
   ## Docker
   [Lien vers DOCKER.md]
   ```
4. Supprimer `docs/QUICKSTART.md` après fusion
5. Garder `README.md` root pour overview projet (ne pas toucher)

**Justification :** Point d'entrée unique, éviter duplication.

**Risque :** 🟢 Faible

**Validation :**
- [ ] `docs/README.md` contient Quickstart + Guide
- [ ] `docs/QUICKSTART.md` n'existe plus
- [ ] Pas de contenu perdu

---

#### Task 2.4 : Créer TESTING.md

**Fichiers :**
- Nouveau : `docs/TESTING.md`

**Actions :**
1. Créer `docs/TESTING.md` avec structure :
   ```markdown
   # Testing Guide
   
   ## Unit Tests
   - How to run: `pytest tests/ -v`
   - Structure: test_parser, test_scheduler, test_formatter
   
   ## Integration Tests
   - Test cases: 01-simple to 05-extreme + demo-warnings
   - How to run in Streamlit
   
   ## CSV Validation
   - Script: `scripts/validate_test_csv.py`
   - Usage examples
   
   ## Adding New Tests
   - Pytest fixtures
   - Test case structure
   ```
2. Documenter commandes, exemples, best practices

**Justification :** Faciliter contribution, onboarding, tests.

**Risque :** 🟢 Très faible

**Validation :**
- [ ] `docs/TESTING.md` existe
- [ ] Commandes testées et fonctionnent

---

### Phase 3 : Tests de Non-Régression

**Objectif :** Garantir zéro régression après refactoring.

---

#### Task 3.1 : Tests unitaires (pytest)

**Commande :**
```bash
pytest tests/ -v --tb=short
```

**Actions :**
1. Exécuter tous les tests unitaires
2. Vérifier 100% succès (pas de FAILED, pas de ERROR)
3. Si échec :
   - Lire traceback
   - Identifier la cause (import, signature, logique)
   - Corriger immédiatement
   - Re-tester

**Validation :**
- [ ] Tous tests au vert (PASSED)
- [ ] Aucun warning critique

**Risque :** 🟡 Moyen (possible régression si refactoring mal fait)

---

#### Task 3.2 : Tests manuels Streamlit (6 test cases)

**Test cases :** 01-simple, 02-moyen, 03-complexe, 04-tres-complexe, 05-extreme, demo-warnings

**Actions :**
1. Lancer Streamlit :
   ```bash
   docker-compose -f apps/mvp-streamlit/docker-compose.yml up
   ```
2. Pour chaque test case :
   - Upload `disponibilites.csv`
   - Upload `recurring-slots.csv` (si existe)
   - Cliquer "Générer Planning"
   - Vérifier : ✅ Succès, nombre cours correct, warnings affichés (demo-warnings)
3. Si échec :
   - Noter l'erreur exacte
   - Vérifier logs Docker
   - Corriger et re-tester

**Validation :**
- [ ] Test 01-simple : ✅
- [ ] Test 02-moyen : ✅
- [ ] Test 03-complexe : ✅
- [ ] Test 04-tres-complexe : ✅
- [ ] Test 05-extreme : ✅
- [ ] Test demo-warnings : ✅ (avec suggestions affichées)

**Risque :** 🟡 Moyen (possible régression UI ou parsing)

---

#### Task 3.3 : Validation CSV (script)

**Commande :**
```bash
python scripts/validate_test_csv.py docs/examples/test-cases/*/disponibilites.csv
```

**Actions :**
1. Exécuter script de validation sur tous les CSV
2. Vérifier aucune erreur de format
3. Si erreur : corriger CSV et re-valider

**Validation :**
- [ ] Aucune erreur de validation

**Risque :** 🟢 Faible

---

### Ordre d'Exécution Recommandé

**Séquence optimale pour minimiser risques :**

1. **Phase 1 - Task 1.1** (dataclasses → models.py)  
   → **Phase 3 - Task 3.1** (pytest immédiatement après)

2. **Phase 1 - Task 1.3** (formatting → formatter.py)  
   → **Phase 3 - Task 3.1** (pytest immédiatement après)

3. **Phase 1 - Task 1.2** (suggestions → scheduler.py)  
   → **Phase 3 - Task 3.1** (pytest immédiatement après)

4. **Phase 1 - Task 1.4** (cleanup imports/docstrings)  
   → **Phase 3 - Task 3.1** (pytest immédiatement après)

5. **Phase 3 - Task 3.2 + 3.3** (tests Streamlit + validation CSV)

6. **Phase 2 - Task 2.1 → 2.2 → 2.3 → 2.4** (documentation)

**Pourquoi cet ordre ?**
- Refactoring code d'abord (avec tests après chaque task)
- Tests complets avant de toucher documentation
- Documentation en dernier (pas de risque de régression)

---

### Estimation de Complexité

| Phase | Tâches | Complexité | Tool Calls Estimés |
| ----- | ------ | ---------- | ------------------ |
| Phase 1 | Task 1.1 | Faible | ~10-15 |
| Phase 1 | Task 1.2 | Moyenne | ~20-30 |
| Phase 1 | Task 1.3 | Faible | ~15-20 |
| Phase 1 | Task 1.4 | Faible | ~10-15 |
| Phase 2 | Task 2.1-2.4 | Faible | ~20-30 |
| Phase 3 | Task 3.1-3.3 | Faible | ~15-25 |
| **Total** | **10 tasks** | **Moyenne** | **~90-135 tool calls** |

---

### Summary pour Barry (Agent d'Exécution)

**Ce qui doit être fait :**
1. Déplacer 2 dataclasses de `scheduler.py` vers `models.py`
2. Déplacer 1 fonction de suggestions de `parser.py` vers `scheduler.py`
3. Déplacer 1 méthode de formatting de `models.py` vers `formatter.py`
4. Cleanup imports/docstrings
5. Supprimer fichiers obsolètes (email-tony, reorganization)
6. Fusionner 4 guides Docker en 1
7. Fusionner QUICKSTART + README
8. Créer TESTING.md
9. Tester pytest après chaque refactoring
10. Tester 6 test cases Streamlit à la fin

**Seuil de succès :** 100% tests pass, 100% test cases fonctionnent, documentation clean.

### Acceptance Criteria

**Code :**
- **Given** les modules `core/` après refactoring  
  **When** on analyse les responsabilités  
  **Then** chaque module a une responsabilité unique et claire

- **Given** tous les tests unitaires  
  **When** on exécute `pytest tests/`  
  **Then** 100% des tests passent

**Documentation :**
- **Given** le dossier `docs/`  
  **When** on liste les fichiers  
  **Then** plus aucun fichier obsolète (email-tony, reorganization)

- **Given** la documentation Docker  
  **When** on cherche dans `docs/`  
  **Then** un seul fichier `DOCKER.md` existe

- **Given** les guides QUICKSTART/README  
  **When** on les lit  
  **Then** pas de contenu dupliqué, hiérarchie claire

**Tests de non-régression :**
- **Given** les 6 test cases Streamlit  
  **When** on les exécute un par un  
  **Then** 100% fonctionnent comme avant le refactoring

## Additional Context

### Dependencies

Aucune nouvelle dépendance requise. Stack actuelle :
- Python 3.10+
- pandas
- ortools
- streamlit
- pytest

### Testing Strategy

**Tests automatisés (pytest) :**
- Exécuter avant ET après chaque phase de refactoring
- Seuil de succès : 100% des tests passent
- Si échec : rollback immédiat et investigation

**Tests manuels (Streamlit) :**
- Exécuter à la fin du refactoring (Phase 3)
- Les 6 test cases doivent fonctionner identiquement
- Si échec : identifier la régression et corriger

**Commande de test :**
```bash
# Tests automatisés
pytest tests/ -v

# Tests manuels
./run-mvp.sh start
# Puis upload chaque test case dans l'interface
```

### Notes

**Priorités :**
1. **Ne rien casser** : Préserver la logique métier fonctionnelle
2. **Clarifier** : Améliorer l'organisation et la lisibilité
3. **Simplifier** : Réduire la documentation redondante

**Après ce refactoring :**
- Code prêt pour amélioration UI/UX Streamlit
- Documentation claire pour passage à Tony
- Base saine pour évolutions futures

**Contexte historique :**
- MVP développé rapidement avec approche Quick Dev
- 6 test cases créés et validés (01-simple à 05-extrême + demo-warnings)
- Système de warnings pour créneaux à 1 étudiant implémenté et testé
- Tous les tests fonctionnent, besoin de clarifier avant d'avancer
