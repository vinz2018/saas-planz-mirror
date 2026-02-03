---
title: 'Algorithme de Génération de Planning Intelligent'
slug: 'algo-generation-planning'
created: '2026-02-01'
status: 'ready-for-dev'
stepsCompleted: [1, 2, 3, 4]
tech_stack: ['Python 3.10+', 'Google OR-Tools CP-SAT', 'pandas', 'Streamlit', 'pytest']
files_to_modify: []
files_to_create: ['src/__init__.py', 'src/models.py', 'src/parser.py', 'src/scheduler.py', 'src/formatter.py', 'app.py', 'tests/__init__.py', 'tests/conftest.py', 'tests/test_parser.py', 'tests/test_scheduler.py', 'tests/test_formatter.py', 'tests/test_integration.py', 'tests/fixtures/test_schedule.csv', 'tests/fixtures/test_overbooking.csv', 'tests/fixtures/test_linked_group_conflict.csv', 'tests/fixtures/test_recurring_slots.csv', 'requirements.txt', 'README.md', '.gitignore']
code_patterns: ['dataclasses for models', 'OR-Tools CP-SAT for constraints', 'soft/hard constraints with penalties', 'two-phase optimization']
test_patterns: ['pytest with fixtures', 'parametrized tests', 'integration tests with CSV fixtures']
estimated_effort: '3-5 days for MVP implementation'
---

# Tech-Spec: Algorithme de Génération de Planning Intelligent

**Created:** 2026-02-01

## Overview

### Problem Statement

Le coach Tony passe 3-4h chaque samedi à créer manuellement un planning pour 50 élèves avec des contraintes multiples interdépendantes (niveaux, disponibilités changeantes, groupes liés, habitudes récurrentes). Le cerveau humain ne peut pas optimiser efficacement autant de variables simultanément.

**Causes racines identifiées (brainstorming) :**
- Surcharge cognitive : 50 élèves × niveaux × disponibilités × contraintes de groupe × habitudes
- Cascade de communication : aller-retours WhatsApp pour valider/négocier
- Absence de visualisation décisionnelle : Excel ne montre pas les options et impacts

### Solution

Algorithme d'optimisation en 2 phases basé sur Google OR-Tools :

**Phase 1 - Squelette (< 1 sec) :** Place les créneaux récurrents pré-définis (élèves avec habitudes fixes). Réduit drastiquement l'espace de recherche.

**Phase 2 - Variations (< 10 sec) :** OR-Tools optimise uniquement les créneaux variables. Génère solution complète ou partielle si contraintes incompatibles.

**Mode dégradation gracieuse :** Si solution complète impossible, retourne solution partielle (ex: 45/50 élèves placés) avec explications détaillées des élèves non placés (conflits, raisons, suggestions d'ajustement).

**Mode itératif :** Tony peut ajuster manuellement, verrouiller des créneaux, puis relancer l'optimisation qui respecte les verrous comme contraintes hard.

**Innovation clé :** Optimisation "Squelette + Variations" - respecte les créneaux récurrents habituels tout en optimisant les variations hebdomadaires.

**Contrainte économique :** Solution doit rester peu coûteuse en ressources (CPU/mémoire) pour permettre pricing abordable en multi-tenant. Pas de ML complexe, optimisations simples et efficaces.

### Scope

**In Scope:**
- **Parser CSV structuré** (format template standardisé avec plages horaires)
  - Colonnes : `nom, sessions_par_semaine, lundi_debut, lundi_fin, mardi_debut, mardi_fin, ..., samedi_debut, samedi_fin, groupe_lie, notes`
  - **Format heures : HH:00 ou HH:30** (granularité demi-heure)
    - Valide : `08:00`, `08:30`, `17:00`, `17:30`
    - Invalide : `08:15`, `10:45` (pas de granularité minute)
    - **Flexibilité totale :** Peut mixer :00 et :30 librement (pas de pattern forcé)
    - Tony peut enchaîner : 08:00-09:00 → 09:00-10:00 → 10:30-11:30 (mix direct + pause)
  - Plages horaires par jour (debut + fin)
  - **Templates fournis :**
    - `docs/examples/template-disponibilites.csv` - Disponibilités élèves
    - `docs/examples/template-recurring-slots.csv` - Créneaux récurrents (nouveau)
  - Tony remplit dans Excel/Numbers, upload dans Streamlit
  - **Avantages format plages :**
    - Dispo large : `lundi_debut=08:00, lundi_fin=19:00` → algo choisit meilleur créneau 1h
    - Créneau précis : `mardi_debut=17:00, mardi_fin=18:00` → créneau fixe
    - Intuitivité : matche mental model ("Sarah dispo toute la journée mercredi")
- Contraintes physiques :
  - Cours de 1h exactement
  - **2-3 élèves par cours + Tony** (min 2, max 3 élèves)
  - **UN SEUL COURS À LA FOIS** (jamais de chevauchement entre cours)
    - À tout moment, maximum 1 cours actif dans le garage
    - Exemple valide : 08:00-09:00 puis 09:00-10:00 (enchaînement direct) ✅
    - Exemple valide : 08:00-09:00 puis 09:30-10:30 (pause 30 min) ✅
    - Exemple invalide : 08:00-09:00 ET 08:30-09:30 simultanés ❌
  - Pas de chevauchement pour un même élève (évident si 1 seul cours à la fois)
- Contraintes métier :
  - **Groupes liés (couples/amis) - Partial Linking :**
    - **Règle 1 :** Si sessions_par_semaine identiques → tous les cours ensemble
    - **Règle 2 :** Si sessions_par_semaine différentes → **Partial linking**
      - Cours ensemble pour min(sessions_per_week)
      - Reste solo pour l'élève avec plus de sessions
      - **Prérequis :** Overlapping availability required (sinon infeasible)
      - **Choix des slots :** OR-Tools optimise quels slots spécifiques (soft constraints)
    - **Exemple :** Vincent (2 sessions, dispo lundi/mercredi/vendredi) + Jerome (1 session, dispo mercredi/vendredi)
      - Overlap : mercredi, vendredi
      - Résultat : 1 cours ensemble (mercredi OU vendredi, algo choisit), 1 solo Vincent (autre jour)
    - **Cas infeasible :** Vincent (2 sessions, dispo lundi/mardi) + Jerome (1 session, dispo jeudi/vendredi)
      - Pas d'overlap → impossible de respecter groupe_lie → les deux unplaced avec explication
  - Respect des habitudes récurrentes (poids élevé)
  - **Slots réservés coach :** Tony peut bloquer des créneaux via UI Streamlit (pas de config file au départ)
  - Distribution équilibrée des cours dans la semaine
- Optimisation multi-critères :
  - Minimiser le nombre d'élèves à contacter
  - Maximiser le respect des habitudes
  - Équilibrer la charge par jour (pas 8 cours lundi, 0 vendredi)
  - Privilégier le remplissage de cours existants (2→3 élèves) vs créer nouveau créneau
- Output enrichi :
  - JSON structuré (planning + metadata + élèves non placés + explications)
  - Markdown formaté (visualisation humaine avec explications des décisions)
  - Explications type LLM : pourquoi chaque décision, conflits détectés, suggestions d'ajustement
- Mode verrouillage/ajustement manuel :
  - Tony peut marquer des créneaux comme "verrouillés" (deviennent contraintes hard)
  - Re-calcul possible en gardant les ajustements manuels

**Out of Scope (Phase 2 ou séparé) :**
- Interface utilisateur web hébergée (Streamlit local pour MVP)
- Gestion base de données
- Authentification/autorisation
- Priorisation des créneaux (Préféré/Acceptable/Dernier recours)
- LLM/NLP avancé pour parsing texte libre
- Gestion abonnements/facturation
- Export Google Calendar (sera dans l'app)
- **Continuité semaine-à-semaine automatique** (MVP = fresh start chaque semaine)
- **Détection automatique des patterns récurrents** depuis historique (MVP = saisie manuelle)

## Context for Development

### Codebase Patterns

**Projet État :** Greenfield - pas de code existant

**Structure du projet :**
```
saas-planz/
├── src/
│   ├── __init__.py
│   ├── models.py           # Dataclasses: Student, Slot, Schedule, ScheduleResult
│   ├── parser.py           # CSV → Student objects (pandas)
│   ├── scheduler.py        # Core algo OR-Tools (2 phases)
│   └── formatter.py        # Schedule → JSON + Markdown
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Fixtures partagées pytest
│   ├── test_parser.py       # Tests parsing CSV
│   ├── test_scheduler.py    # Tests constraints + optimization
│   ├── test_formatter.py    # Tests output formats
│   ├── test_integration.py  # Tests end-to-end
│   └── fixtures/
│       ├── test_schedule.csv              # 10 students, valid
│       ├── test_overbooking.csv          # Conflicting availabilities
│       ├── test_linked_group_conflict.csv # Partial linking edge case
│       └── test_recurring_slots.csv       # Recurring skeleton test
├── app.py                  # Streamlit UI
├── requirements.txt        # Dependencies
└── README.md              # Setup + Usage

docs/                       # Documentation (déjà existant)
└── examples/
    ├── template-disponibilites.csv    # Template disponibilités élèves
    ├── template-recurring-slots.csv    # Template créneaux récurrents
    ├── README-template.md              # Instructions disponibilités
    └── README-recurring-slots.md       # Instructions récurrents
```

**Patterns de code identifiés :**

**1. Dataclasses pour modèles (Python 3.10+)**
```python
from dataclasses import dataclass
from typing import List, Optional
from datetime import time

@dataclass
class Student:
    name: str
    sessions_per_week: int
    available_slots: List['Slot']  # Plages horaires disponibles
    linked_group: Optional[str] = None
    notes: str = ""

@dataclass
class Slot:
    day: str  # "lundi", "mardi", ...
    start_time: time  # datetime.time(8, 0)
    end_time: time    # datetime.time(9, 0)
    is_recurring: bool = False  # Squelette vs variation

@dataclass
class ScheduledClass:
    slot: Slot
    students: List[str]  # Noms des élèves
    status: str  # "locked" | "proposed" | "needs_validation"

@dataclass
class ScheduleResult:
    schedule: List[ScheduledClass]
    unplaced: List['UnplacedStudent']
    metadata: dict
    explanations: dict
```

**2. OR-Tools CP-SAT patterns** (inspiré de `shift_scheduling_sat.py`)
```python
from ortools.sat.python import cp_model

model = cp_model.CpModel()

# Variables booléennes: assignment[student_idx, slot_idx]
assignment = {}
for s_idx, student in enumerate(students):
    for sl_idx, slot in enumerate(available_slots):
        assignment[s_idx, sl_idx] = model.new_bool_var(f"assign_{s_idx}_{sl_idx}")

# Hard constraints avec AddBoolOr, AddExactlyOne
# Soft constraints avec pénalités dans l'objectif
obj_vars = []
obj_coeffs = []

# Exemple: Pénalité si pas de respect des habitudes récurrentes
penalty_var = model.new_bool_var("penalty_no_recurring")
model.add_implication(assignment[s_idx, sl_idx], penalty_var)
obj_vars.append(penalty_var)
obj_coeffs.append(10)  # Poids de la pénalité

# Minimize
model.minimize(sum(obj_vars[i] * obj_coeffs[i] for i in range(len(obj_vars))))

# Solve
solver = cp_model.CpSolver()
solver.parameters.max_time_in_seconds = 10.0
status = solver.solve(model)
```

**3. Deux phases d'optimisation**
```python
def generate_schedule(students, recurring_slots):
    # Phase 1: Squelette (déterministe)
    skeleton = place_recurring_slots(recurring_slots)
    
    # Phase 2: Variations (OR-Tools)
    remaining_students = [s for s in students if not s.is_recurring]
    optimized = optimize_with_ortools(remaining_students, skeleton)
    
    # Merge
    final_schedule = merge_skeleton_and_variations(skeleton, optimized)
    return final_schedule
```

**Références disponibles :**
- Document de brainstorming complet : `_bmad-output/brainstorming/brainstorming-session-2026-02-01.md`
- CSV exemple ancien format (texte libre) : `docs/examples/disponibilites-exemple.csv`
- **Templates CSV MVP :**
  - Disponibilités élèves : `docs/examples/template-disponibilites.csv`
  - Créneaux récurrents : `docs/examples/template-recurring-slots.csv`
- **README templates :**
  - Instructions disponibilités : `docs/examples/README-template.md`
  - Instructions créneaux récurrents : `docs/examples/README-recurring-slots.md`
- OR-Tools exemple shift scheduling : https://github.com/google/or-tools/blob/stable/examples/python/shift_scheduling_sat.py
- Adversarial review findings : 24 issues identifiées (2 Critical, 7 High, 10 Medium, 5 Low)
- 13 vérités fondamentales identifiées (contraintes du domaine)

**Environnement cible :**
- Python 3.10+
- Interface Streamlit (UI web locale)
- Doit être testable avec le CSV exemple

### Files to Reference (Existing)

| File | Purpose |
| ---- | ------- |
| `docs/examples/disponibilites-exemple.csv` | CSV réel de Tony avec 50 élèves, ancien format texte libre |
| `docs/examples/template-disponibilites.csv` | **Template CSV MVP** avec format plages horaires structuré |
| `docs/examples/README-template.md` | Instructions pour Tony sur remplissage CSV |
| `_bmad-output/brainstorming/brainstorming-session-2026-02-01.md` | Analyse complète des contraintes et vérités fondamentales |

### Files to Create

| File | Purpose | Lines Est. |
| ---- | ------- | ---------- |
| `src/models.py` | Dataclasses: `Student`, `Slot`, `ScheduledClass`, `ScheduleResult`, `UnplacedStudent` | ~100 |
| `src/parser.py` | Parse CSV → List[Student], validation format, expansion plages → slots 1h | ~150 |
| `src/scheduler.py` | **Core algo**: Phase 1 (squelette) + Phase 2 (OR-Tools), contraintes hard/soft | ~400 |
| `src/formatter.py` | ScheduleResult → JSON + Markdown avec explications templates | ~200 |
| `app.py` | Streamlit UI: upload CSV, bouton generate, affichage résultats, download | ~150 |
| `requirements.txt` | Dependencies: ortools, pandas, streamlit, pytest | ~10 |
| `README.md` | Setup instructions, usage, architecture overview | ~100 |
| `tests/test_parser.py` | Unit tests parsing, validation, edge cases | ~150 |
| `tests/test_scheduler.py` | Tests contraintes, optimisation, solutions partielles | ~200 |
| `tests/test_formatter.py` | Tests output JSON/Markdown | ~80 |
| `tests/fixtures/test_schedule.csv` | CSV test avec 10 élèves | ~12 |
| `tests/fixtures/test_overbooking.csv` | CSV test overbooking (conflits) | ~12 |
| `tests/fixtures/test_linked_group_conflict.csv` | CSV test partial linking | ~8 |
| `tests/fixtures/test_recurring_slots.csv` | CSV créneaux récurrents test | ~10 |
| `docs/examples/template-recurring-slots.csv` | Template CSV pour créneaux récurrents Tony | ~5 |

**Total estimé : ~1,600 lignes de code + tests**

### Technical Decisions

**1. Librairie d'optimisation : Google OR-Tools**
- **Pourquoi :** CSP solver mature, performant, bien documenté, utilisé en production
- **Alternative écartée :** python-constraint (moins performant), algo génétique custom (trop de tuning)
- **Conséquence :** Nécessite apprentissage de l'API OR-Tools CP-SAT

**2. Parsing CSV : pandas direct (format plages horaires structurées)**
- **Pourquoi :** Template CSV standardisé fourni à Tony = données propres dès le départ
- **Approche :** `pandas.read_csv()` + validation basique + expansion des plages en créneaux 1h
- **Logique parsing :**
  ```python
  # Exemple : lundi_debut=08:00, lundi_fin=19:00
  # → Génère slots disponibles : [08:00, 09:00, 10:00, ..., 18:00] (11 créneaux)
  # L'algo CSP choisira parmi ces créneaux
  ```
- **Avantages :**
  - Pas de regex complexe, pas d'ambiguïtés
  - Validation immédiate (format heure, plage cohérente)
  - Flexibilité : larges plages OU créneaux précis
  - Migration UI future triviale (formulaire web → CSV backend)
- **Trade-off :** Tony doit remplir template (mais plus simple et intuitif qu'Excel actuel)

**3. Architecture modulaire**
- **Modules séparés :**
  - `parser.py` : CSV → structure Python
  - `scheduler.py` : Algo OR-Tools
  - `formatter.py` : Planning → JSON + Markdown
  - `main.py` : CLI entry point
- **Pourquoi :** Testabilité, réutilisabilité, clarté

**4. Interface MVP : Streamlit (UI web locale)**
- **Pourquoi Streamlit :**
  - Tony est sur Mac, pas de lignes de commande à taper
  - UI web simple lancée en local : `streamlit run app.py`
  - 1 fichier Python (~50-100 lignes) = dev rapide
  - Upload CSV drag & drop, bouton "Générer", download résultats
  - Coût : 0€ (tourne en local), complexité minimale
- **Alternative CLI écartée :** Trop technique pour utilisateur non-dev

**5. Output dual (JSON + Markdown)**
- **JSON :** Machine-readable, pour intégration API future
- **Markdown :** Human-readable, pour debug et validation avec Tony
- **Structure JSON :**
  ```json
  {
    "metadata": {
      "generated_at": "ISO-8601",
      "week_start": "2026-02-03",
      "students_to_contact": []
    },
    "schedule": [
      {
        "day": "lundi",
        "start_time": "08:00",
        "end_time": "09:00",
        "students": ["Hugo", "Juliette"],
        "status": "locked|proposed|needs_validation"
      }
    ],
    "unplaced": [
      {
        "student": "Sarah",
        "reason": "slot_overbooked",
        "conflicts": [...],
        "suggestions": [...]
      }
    ],
    "explanations": {
      "decisions": [...],
      "constraint_scores": {...}
    }
  }
  ```

**5. Algorithme 2 phases pour performance optimale**
- **Phase 1 : Squelette** (déterministe, < 1 sec)
  - **Input : CSV créneaux récurrents** (`template-recurring-slots.csv`)
    - Tony remplit ce template avec les élèves ayant des habitudes fixes
    - Format : `nom, jour, heure_debut, heure_fin` (une ligne par créneau récurrent)
    - Exemple : `Vincent, mardi, 17:00, 18:00` + `Vincent, vendredi, 12:00, 13:00`
  - Place tous les créneaux récurrents fixes
  - **Validation complète du squelette :**
    - **UN SEUL COURS À LA FOIS : Aucun chevauchement entre cours** (contrainte globale)
    - Respect capacité par cours (2-3 élèves)
    - Tous les élèves existent dans le CSV principal
    - Créneaux dans les disponibilités des élèves
    - Pas de conflits individuels (élève placé 2× au même moment - évident si 1 cours à la fois)
  - Output : planning partiel avec ~70-80% des élèves placés
  
- **Phase 2 : Variations** (OR-Tools CSP, < 10 sec max)
  - Input : squelette + élèves restants + contraintes
  - Optimise uniquement les créneaux variables
  - Espace de recherche réduit de ~90%
  - **Stratégie timeout progressive :**
    - 0-5 sec : Optimisation complète (toutes contraintes hard + soft)
    - 5-10 sec : Relaxation soft constraints (garde uniquement hard)
    - 10-15 sec : Relaxation supplémentaire (objectif = placer maximum d'élèves)
    - Si toujours pas de solution : retourne meilleure tentative partielle
  
**6. Contraintes encodées avec poids**
- **Hard constraints** (doivent être respectées) :
  - **Cours exactement 1h, sur :00 ou :30**
    - Time interval semantics: **Half-open intervals [start, end)**
    - 09:00-10:00 means starts at 09:00:00, ends at 09:59:59
    - Back-to-back courses valid: [08:00, 09:00) then [09:00, 10:00) → no overlap ✅
  - 2-3 élèves par cours (min 2, max 3)
  - **UN SEUL COURS À LA FOIS** (aucun chevauchement entre cours)
    - Contrainte globale : à tout moment T, max 1 cours actif
    - Overlap check: `start1 < end2 AND start2 < end1` means overlap
    - Plus simple que capacité garage : pas de gestion simultanéité
  - **Groupes liés : Partial linking avec prérequis overlap**
    - Si même `sessions_per_week` : toujours ensemble
    - Si différent : ensemble pour min(sessions), reste solo
    - **Prérequis :** Overlapping availability required (sinon infeasible → both unplaced)
  - Slots réservés coach jamais utilisés (bloqués via UI)
  - Créneaux verrouillés manuellement (si re-calcul)
  - Créneaux dans les disponibilités élèves (plages horaires CSV)
- **Soft constraints** (à maximiser) :
  - Respect habitudes récurrentes (poids 10)
  - Distribution équilibrée jours (poids 5)
  - Remplir cours existants vs nouveau (poids 3)
  
**7. Solution partielle avec explications**
- Si impossible de placer tous les élèves, retourner :
  - Planning avec maximum d'élèves placés (best-effort)
  - Liste élèves non placés avec raisons détaillées
  - Suggestions d'ajustement (ex: "Contacter Sarah pour proposer mercredi 10h")
  - Pas d'alternatives multiples (trop coûteux) - MVP single solution

**8. Explications claires (template-based, pas de LLM)**
- **Pas de vrai LLM** (coût 0€) : templates Python simples
- **Format humain :**
  ```
  Sarah n'a pas pu être placée car :
  - Lundi 8h : déjà 3 élèves (Hugo, Juliette, Isabelle)
  - Vendredi 12h : déjà 3 élèves (Victor, Vincent, Marion)
  
  Suggestions :
  - Proposer Mercredi 10h (disponible dans ses dispos)
  - Ou déplacer Isabelle → Jeudi 9h pour libérer Lundi 8h
  ```
- **Objectif :** Réduire coût support en rendant l'algo transparent

## Implementation Plan

### Phase 1: Foundation (Models + Parser)

**Task 1.1: Create data models** (`src/models.py`)
- [ ] Define `Student` dataclass with fields: name, sessions_per_week, available_slots, linked_group, notes
- [ ] Define `Slot` dataclass with fields: day, start_time, end_time, is_recurring
- [ ] Define `ScheduledClass` dataclass with fields: slot, students, status
- [ ] Define `UnplacedStudent` dataclass with fields: student, reason, conflicts, suggestions
- [ ] Define `ScheduleResult` dataclass with fields: schedule, unplaced, metadata, explanations
- [ ] Add validation methods (e.g., `Slot.duration()` must be 1h)

**Task 1.2: Implement CSV parser** (`src/parser.py`)
- [ ] Function `parse_csv(file_path) -> List[Student]`
  - Read CSV with pandas
  - **Validate required columns exist** (exact names case-sensitive)
  - **Validate time format:** HH:00 or HH:30 only (reject HH:15, HH:45, etc.)
  - **Validate time range coherence:** debut < fin for each day
  - **Expand time ranges to hourly slots:**
    - **Rules:**
      - 08:00-19:00 → [08:00-09:00, 09:00-10:00, ..., 18:00-19:00] (11 slots)
      - 08:30-19:00 → [08:30-09:30, 09:30-10:30, ..., 18:00-19:00] (11 slots)
      - 08:00-19:30 → [08:00-09:00, 09:00-10:00, ..., 18:30-19:30] (12 slots)
      - 08:15-19:00 → ERROR (start must be :00 or :30)
    - All slots are 1-hour duration
  - Build Student objects with available_slots
- [ ] Function `validate_linked_groups(students) -> List[Tuple[str, str]]`
  - Check reciprocity (if A links to B, B must link to A)
  - **Check overlapping availability (REQUIRED for partial linking):**
    - Find intersection of available_slots between linked students
    - If empty intersection → ERROR with clear message: "Vincent and Jerome have no overlapping availability"
  - **Partial linking support:** Allow different `sessions_per_week` (min sessions together, rest solo)
  - Warn if sessions_per_week differ (partial linking will apply)
- [ ] Exception handling with clear error messages

**Task 1.3: Write parser tests** (`tests/test_parser.py`)
- [ ] Test valid CSV parsing
- [ ] Test time range expansion (08:00-19:00 → slots list)
- [ ] Test validation errors (missing columns, invalid format, plage incohérente)
- [ ] Test linked groups validation (reciprocal, non-reciprocal)

### Phase 2: Scheduler Core (OR-Tools)

**Task 2.1: Implement Phase 1 - Skeleton** (`src/scheduler.py`)
- [ ] Function `load_recurring_slots_csv(csv_path) -> List[ScheduledClass]`
  - Load recurring slots from CSV
  - **Format specification:**
    - Required columns (case-sensitive): `nom`, `jour`, `heure_debut`, `heure_fin`
    - Day format: lowercase French day names (`lundi`, `mardi`, `mercredi`, `jeudi`, `vendredi`, `samedi`)
    - Time format: HH:00 or HH:30 (e.g., `08:00`, `17:30`)
    - Duration: Must be exactly 1 hour (end - start = 1h)
    - Multiple recurring slots for same student: Multiple rows with same `nom`
  - Parse and validate time format (HH:00 or HH:30 only)
  - Build ScheduledClass objects
- [ ] Function `validate_skeleton(skeleton, all_students, coach_reserved) -> ValidationResult`
  - **Check no overlap between ANY courses** (UN SEUL COURS À LA FOIS)
    - For each pair of courses, verify no time overlap
    - Logic: `start1 < end2 AND start2 < end1` means overlap → invalid
  - Check capacity per class (2-3 students)
  - Check all student names exist in main CSV
  - Check slots within student availabilities
  - Check no overlap with coach reserved slots
- [ ] Function `place_recurring_slots(recurring_slots) -> Dict[Slot, ScheduledClass]`
  - Build initial schedule with recurring placements
  - Mark students as "placed" in skeleton

**Task 2.2: Implement Phase 2 - OR-Tools Optimization** (`src/scheduler.py`)
- [ ] Function `optimize_variations(remaining_students, skeleton, constraints) -> ScheduleResult`
  - Create CP-SAT model
  - Define variables: `assignment[student_idx, slot_idx]` (BoolVar)
  - **Hard constraints:**
    - Each student placed exactly `sessions_per_week` times
    - Slot capacity: 2-3 students per class
    - **UN SEUL COURS À LA FOIS: no overlap between ANY classes**
      - AddNoOverlap constraint on all course interval variables
      - Much simpler than multi-capacity: binary constraint (overlap or not)
    - **Linked groups: Partial linking** (min sessions together if different counts)
    - Coach reserved slots never used (loaded from Streamlit session state)
    - Skeleton slots locked (cannot be modified)
    - **Time granularity: slots only start at :00 or :30**
  - **Soft constraints (penalties in objective):**
    - Respect recurring habits (weight 10)
    - Balance load per day (weight 5)
    - Fill existing classes 2→3 before new slot (weight 3)
  - **Progressive timeout strategy:**
    - Phase 2a (0-5 sec): All constraints (hard + soft with weights)
    - Phase 2b (5-10 sec): Relax soft constraints (hard only)
    - Phase 2c (10-15 sec): Further relaxation (maximize placements)
  - Handle partial solution if no complete solution found

**Task 2.3: Implement graceful degradation**
- [ ] Function `extract_partial_solution(solver, model, students) -> ScheduleResult`
  - If OPTIMAL or FEASIBLE: return complete/partial schedule
  - If INFEASIBLE: return empty schedule with detailed explanations
  - For each unplaced student:
    - Identify conflicting constraints
    - Generate suggestions (alternative slots from their availability)

**Task 2.4: Write scheduler tests** (`tests/test_scheduler.py`)
- [ ] Test skeleton loading and validation
- [ ] Test Phase 2 with small dataset (10 students)
- [ ] Test hard constraints respected (capacity, no overlap, linked groups)
- [ ] Test soft constraints optimization (recurring habits preferred)
- [ ] Test partial solution when infeasible
- [ ] Test explanations for unplaced students

### Phase 3: Output Formatting

**Task 3.1: Implement JSON formatter** (`src/formatter.py`)
- [ ] Function `to_json(schedule_result) -> dict`
  - Structure: metadata, schedule, unplaced, explanations
  - Serialize datetime objects to ISO-8601 strings
  - Include constraint scores in explanations

**Task 3.2: Implement Markdown formatter** (`src/formatter.py`)
- [ ] Function `to_markdown(schedule_result) -> str`
  - Visual table by day/time
  - **Status indicators using emojis/symbols:**
    - 🔒 locked (recurring or manually locked)
    - ✅ proposed (algo suggestion)
    - ⚠️ needs_validation (conflicts detected)
  - Section for unplaced students with reasons
  - Section for explanations (why decisions made)
  - Template-based (no LLM cost)

**Task 3.3: Write formatter tests** (`tests/test_formatter.py`)
- [ ] Test JSON output structure
- [ ] Test Markdown readability
- [ ] Test edge cases (empty schedule, all unplaced)

### Phase 4: Streamlit UI

**Task 4.1: Create Streamlit app** (`app.py`)
- [ ] Title and instructions
- [ ] Download buttons:
  - "📥 Télécharger Template Disponibilités" (main CSV)
  - "📥 Télécharger Template Créneaux Récurrents" (recurring CSV)
- [ ] File uploaders:
  - Upload disponibilités CSV (drag & drop)
  - Upload créneaux récurrents CSV (optional)
- [ ] **Coach reserved slots UI:**
  - Multiselect or time picker to block slots
  - **Storage format:**
    - Structure: `List[Slot]` stored in `st.session_state['coach_reserved']`
    - Persistence: Session-only for MVP (lost on app restart)
    - Future: Save to `coach_reserved_slots.csv` for persistence across sessions
  - **Validation:** UI warns if reserved slot conflicts with existing recurring skeleton
- [ ] Button "⚡ Générer Planning"
- [ ] Display results:
  - Visual schedule (table by day/time with color coding)
  - List of unplaced students with reasons
  - Explanations section
- [ ] Buttons "💾 Télécharger JSON" and "📄 Télécharger Markdown"
- [ ] **Session state management** for:
  - Uploaded CSVs
  - Current schedule
  - Coach reserved slots
  - Manual adjustments (Phase 2+)
- [ ] Error handling with friendly messages

**Task 4.2: Test Streamlit app manually**
- [ ] Test on Mac with template CSV
- [ ] Test upload and generation flow
- [ ] Test downloads (JSON + Markdown)
- [ ] Test error messages (invalid CSV)

### Phase 5: Documentation & Deployment

**Task 5.1: Write README** (`README.md`)
- [ ] Installation instructions (`pip install -r requirements.txt`)
- [ ] Usage instructions (`streamlit run app.py`)
- [ ] Architecture overview
- [ ] Testing instructions (`pytest`)

**Task 5.2: Create requirements.txt**
- [ ] List all dependencies with versions
- [ ] Test fresh install on clean venv

**Task 5.3: Integration test end-to-end**
- [ ] Test with Tony's template CSV (10 students)
- [ ] Validate output makes sense
- [ ] Benchmark execution time (< 10 sec)
- [ ] Validate memory usage (< 100 MB)

### Acceptance Criteria

**Parser:**
- **Given** a valid CSV with 10 students and plages horaires  
  **When** `parse_csv()` is called  
  **Then** returns 10 Student objects with expanded slots (e.g., 08:00-19:00 → 11 slots)

- **Given** a CSV with invalid time format (e.g., "8h00")  
  **When** `parse_csv()` is called  
  **Then** raises ValidationError with clear message

**Scheduler:**
- **Given** 10 students with compatible availabilities  
  **When** `generate_schedule()` is called  
  **Then** returns ScheduleResult with all students placed (100% success) AND no course overlap

- **Given** 10 students with conflicting availabilities (overbooking)  
  **When** `generate_schedule()` is called  
  **Then** returns ScheduleResult with max students placed + unplaced list with reasons

- **Given** linked group (Vincent, Jerome) with same sessions_per_week  
  **When** `generate_schedule()` is called  
  **Then** both are placed in same slot or both unplaced

- **Given** linked group (Vincent: 2 sessions, Jerome: 1 session) with overlapping availability  
  **When** `generate_schedule()` is called  
  **Then** returns schedule with 1 shared course + 1 solo course for Vincent

- **Given** linked group (Vincent, Jerome) with NO overlapping availability  
  **When** `generate_schedule()` is called  
  **Then** both unplaced with error "No overlapping availability for linked group"

- **Given** schedule with cours1 (08:00-09:00) and cours2 (08:30-09:30)  
  **When** validation runs  
  **Then** raises error "Course overlap detected" (UN SEUL COURS À LA FOIS violated)

- **Given** back-to-back courses (08:00-09:00 then 09:00-10:00)  
  **When** validation runs  
  **Then** passes (no overlap, touching boundaries OK with half-open intervals)

**Performance:**
- **Given** 50 students (Tony's real dataset)  
  **When** `generate_schedule()` is called  
  **Then** completes in < 10 seconds

**Streamlit UI:**
- **Given** Tony opens app and uploads valid CSV  
  **When** clicks "Générer Planning"  
  **Then** sees visual schedule + download buttons within 10 sec

## Additional Context

### Dependencies

**Python packages :**
- `ortools` (Google OR-Tools) - Algo optimisation
- `pandas` (manipulation CSV) - Parsing données
- `streamlit` (UI web locale) - Interface utilisateur
- Standard lib : `re`, `json`, `datetime`

**Installation :**
```bash
pip install ortools pandas streamlit
```

### Architecture Économique (Multi-Tenant)

**Coûts CPU/Mémoire par planning :**
- Phase 1 (Squelette) : < 0.5 sec CPU, ~10 MB RAM
- Phase 2 (OR-Tools) : 5-10 sec CPU, ~50 MB RAM
- **Total : < 10 sec CPU, < 100 MB RAM par génération**
- **Note :** Contrainte "UN SEUL COURS À LA FOIS" simplifie drastiquement l'algo vs gestion multi-capacity
  - Pas besoin de gérer simultanéité
  - Juste contrainte NoOverlap sur tous les cours
  - Espace de recherche plus petit → potentiellement < 5 sec

**Scalabilité multi-tenant :**
- **100 coachs** : VPS 2 cores @ 10€/mois suffit largement
- **500 coachs** : VPS 4 cores @ 20€/mois suffit
- **1000+ coachs** : Architecture asynchrone (queue + workers) nécessaire
- **Pas de GPU, pas de ML** = coûts minimes

**Architecture MVP (Synchrone) :**
```
Client Streamlit (local) 
    ↓ HTTP
API Python (1 serveur)
    ↓
OR-Tools Scheduler
    ↓
JSON + Markdown output
```

**Transition multi-tenant future :**
- Streamlit local → Web app hébergée
- API synchrone → Queue asynchrone (Redis + Workers) si > 500 coachs
- Coût marginal par coach : ~0.02€/mois (CPU/RAM)
- Permet pricing abordable : 9-19€/mois pour coach

### Testing Strategy

**Framework :** pytest

**Structure :**
```
tests/
├── __init__.py
├── conftest.py          # Fixtures partagées
├── test_parser.py       # Unit tests parser
├── test_scheduler.py    # Unit tests scheduler
├── test_formatter.py    # Unit tests formatter
├── test_integration.py  # Tests end-to-end
└── fixtures/
    ├── test_schedule.csv              # 10 students, valid
    ├── test_overbooking.csv          # Conflicting availabilities (infeasible)
    ├── test_linked_group_conflict.csv # Partial linking edge case
    └── test_recurring_slots.csv       # Recurring skeleton test
```

**Types de tests :**

**1. Unit Tests (parser)**
- Parsing CSV valide → Student objects corrects
- Expansion plages horaires (08:00-19:00 → slots list)
- Validation format (HH:MM, plage cohérente)
- Validation groupes liés (reciprocité)
- Gestion erreurs (colonnes manquantes, format invalide)

**2. Unit Tests (scheduler)**
- Squelette loading et placement
- Contraintes hard respectées (capacity, no overlap, linked groups)
- Contraintes soft optimisées (habitudes récurrentes, balance jours)
- Solution partielle si infaisable
- Explications pour unplaced students

**3. Unit Tests (formatter)**
- JSON output structure correcte
- Markdown readability (headers, tables)
- Serialization datetime → ISO-8601

**4. Integration Tests**
- End-to-end : CSV → parse → schedule → format → JSON + Markdown
- Avec fixture 10 students (template-disponibilites.csv)
- Validation output cohérent avec input

**5. Performance Tests**
- Benchmark avec 50 students (Tony's dataset) < 10 sec
- Memory profiling < 100 MB RAM

**Coverage target :** 80%+ sur parser, scheduler, formatter

**Fixtures partagées (conftest.py) :**
```python
@pytest.fixture
def sample_students():
    return [
        Student(name="Vincent", sessions_per_week=2, ...),
        Student(name="Jerome", sessions_per_week=1, ...),
        ...
    ]

@pytest.fixture
def sample_csv_path():
    return "tests/fixtures/test_schedule.csv"
```

**Commande de test :**
```bash
pytest tests/ -v --cov=src --cov-report=html
```

### Notes

**Références brainstorming :**
- 18+ fonctionnalités identifiées, 10 core pour MVP
- Cette spec couvre seulement l'algo (fonctionnalité #3 du MVP)
- Les autres features (UI, auth, etc.) seront spécifiées séparément

**Parcours utilisateur MVP (Tony) :**

1. **Setup initial** (une fois) :
   - Tony installe : `pip install ortools pandas streamlit`
   - Tony télécharge les templates :
     - `template-disponibilites.csv` (disponibilités élèves)
     - `template-recurring-slots.csv` (créneaux récurrents)
   - Tony lance : `streamlit run app.py`

2. **Chaque semaine (préparation vendredi soir)** :
   - Tony ouvre `template-disponibilites.csv` dans Excel/Numbers
   - Met à jour les disponibilités des élèves (modifications uniquement)
   - **Première semaine uniquement :** Remplit `template-recurring-slots.csv` avec élèves ayant habitudes fixes
   - Sauvegarde en CSV

3. **Chaque samedi matin** :
   - Tony ouvre l'app Streamlit dans son navigateur (localhost:8501)
   - Upload ses CSVs :
     - Disponibilités élèves (obligatoire)
     - Créneaux récurrents (optionnel après première semaine)
   - **Bloque ses créneaux personnels** via UI (ex: lundi 12h-13h, mercredi 18h-19h)
   - Clique "⚡ Générer Planning"
   - **Algo génère en 10-15 sec max** (progressive relaxation si besoin)
   - Tony voit :
     - Planning visuel (tableau par jour/heure, color-coded)
     - Liste élèves non placés avec explications détaillées
     - Suggestions d'ajustement pour chaque conflit
     - Bouton "💾 Télécharger JSON" + "📄 Télécharger Markdown"
   - **Temps : 30 min au lieu de 3h**

4. **Si ajustements nécessaires** (Phase 2+, hors MVP) :
   - Tony édite manuellement via UI (drag & drop futur)
   - Verrouille créneaux ajustés
   - Clique "Re-optimiser" → algo respecte les verrous

**Note MVP :** Continuité semaine-à-semaine = fresh start. Si Tony veut garder ajustements, il doit éditer `template-recurring-slots.csv` manuellement. Feature "Sauvegarder comme récurrent" prévue Phase 2.

## Décisions Clés Issues de l'Adversarial Review & Advanced Elicitation

**F1 - Capacité Garage (CORRIGÉ après clarification) :**
- **Décision FINALE :** UN SEUL COURS À LA FOIS (jamais de cours simultanés)
- Capacité par cours : 2-3 élèves + Tony
- **Exemples valides :**
  - 08:00-09:00 puis 09:00-10:00 (enchaînement direct) ✅
  - 08:00-09:00 puis 09:30-10:30 (pause 30 min) ✅
  - 08:00-09:00 puis 09:00-10:00 puis 10:30-11:30 (mix) ✅
- **Exemples invalides :**
  - 08:00-09:00 ET 08:30-09:30 (chevauchement) ❌
  - 09:00-10:00 ET 09:30-10:30 (chevauchement) ❌
- **Simplification majeure :** Pas de gestion multi-cours simultanés, juste contrainte "no overlap"

**F2 - Format Créneaux Récurrents :**
- **Décision :** Template CSV (`template-recurring-slots.csv`) au lieu de JSON
- Tony remplit dans Excel, plus accessible que JSON
- Feature future : UI pour marquer créneaux récurrents + détection automatique patterns

**F3 - Granularité Horaires :**
- **Décision :** HH:00 ou HH:30 uniquement (demi-heure)
- Valide : `08:00`, `08:30`, `17:00`, `17:30`
- Invalide : `08:15`, `10:45` (pas de minute)
- **Flexibilité totale :** Pas de pattern forcé (:00/:30 alternés)
- Tony peut mixer librement : 08:00-09:00 → 09:00-10:00 → 10:30-11:30
- Pas de pause obligatoire entre cours

**F5 - Slots Réservés Coach :**
- **Décision :** UI Streamlit pour bloquer plages horaires
- Pas de config file (trop technique pour Tony)
- Tony sélectionne via multiselect/time picker dans l'app

**F6 - Groupes Liés Sessions Différentes :**
- **Décision :** Partial linking avec prérequis overlap
- Vincent (2 sessions) + Jerome (1 session) → 1 cours ensemble, 1 solo Vincent
- **Prérequis :** Overlapping availability required (sinon infeasible)
- **Exemple infeasible :** Vincent (dispo lundi/mardi) + Jerome (dispo jeudi/vendredi) → pas d'overlap → both unplaced
- Algo optimise quels slots spécifiques pour min(sessions) ensemble

**F7 - Continuité Semaine-à-Semaine :**
- **Décision MVP :** Fresh start chaque semaine (simple)
- Phase 2+ : Bouton "Sauvegarder comme récurrent" + import JSON semaine précédente

**F8 - Timeout OR-Tools :**
- **Décision :** Progressive relaxation avec early termination
- **Phase 2a (max 5 sec):** All constraints (hard + soft)
  - If INFEASIBLE before timeout → proceed to Phase 2b immediately (no wasted time)
- **Phase 2b (max 5 sec):** Hard constraints only
  - If INFEASIBLE before timeout → proceed to Phase 2c immediately
- **Phase 2c (max 5 sec):** Maximize placements (relaxed)
- **Total worst-case:** < 15 sec, but often < 5 sec if quick INFEASIBLE detection

**Futures Features (Out of MVP) :**
- Détection automatique patterns récurrents depuis historique
- Continuité automatique semaine N → semaine N+1
- Drag & drop UI pour ajustements manuels
- Export Google Calendar
- Multi-tenant hébergé
