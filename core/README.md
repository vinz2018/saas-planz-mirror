# Core - Logique Métier SaaS Planz

Code métier réutilisable, indépendant de l'interface (Streamlit, web, mobile, etc.).

---

## 📦 Modules

### `models.py` (220 lignes)

Modèles de données avec validation :
- `Slot` - Créneau horaire (1h, :00 ou :30)
- `Student` - Élève avec disponibilités
- `ScheduledClass` - Cours planifié (2-3 élèves)
- `UnplacedStudent` - Explications pour élèves non placés
- `ScheduleResult` - Résultat complet

**Usage :**
```python
from core.models import Slot, Student, ScheduleResult
```

---

### `parser.py` (340 lignes)

Parsing et validation des CSVs :
- `parse_csv()` - Parse disponibilités élèves
- `parse_recurring_slots_csv()` - Parse créneaux récurrents
- `validate_linked_groups()` - Validation groupes liés
- `expand_time_range_to_slots()` - Expansion plages horaires

**Usage :**
```python
from core.parser import parse_csv

students = parse_csv("disponibilites.csv")
```

---

### `scheduler.py` (650 lignes)

Algorithme 2-phase avec OR-Tools :
- **Phase 1 Skeleton** - Placement créneaux récurrents
- **Phase 2 OR-Tools** - Optimisation CP-SAT
- Progressive timeout (0-5s, 5-10s, 10-15s)
- Graceful degradation

**Usage :**
```python
from core.scheduler import generate_schedule

result = generate_schedule(
    students=students,
    recurring_slots_path="recurring.csv",
    coach_reserved_slots=reserved
)
```

---

### `formatter.py` (200 lignes)

Export des résultats :
- `to_json()` - Export JSON structuré
- `to_markdown()` - Export Markdown human-readable
- `save_json()`, `save_markdown()` - Sauvegarde fichiers

**Usage :**
```python
from core.formatter import to_json, to_markdown

json_data = to_json(result)
markdown_text = to_markdown(result)
```

---

## 🎯 Contraintes Implémentées

### Hard Constraints
- **UN SEUL COURS À LA FOIS** (no overlap)
- Capacité 2-3 élèves par cours
- Durée exactement 1h
- Granularité :00 ou :30
- Groupes liés avec partial linking
- Slots coach réservés jamais utilisés

### Soft Constraints (à maximiser)
- Respect habitudes récurrentes (poids 10)
- Distribution équilibrée par jour (poids 5)
- Remplir cours existants avant nouveau (poids 3)

---

## 🧪 Tests

Tests dans `/tests` (racine du projet) :
- `test_parser.py` - 40+ test cases
- `test_scheduler.py` - Tests skeleton + OR-Tools
- `test_integration.py` - Tests end-to-end

---

## 📚 Dépendances

```python
pandas>=2.1.4      # CSV parsing
ortools>=9.8.3296  # CP-SAT solver
```

---

## 🔄 Utilisation dans les Apps

Toutes les apps (Streamlit, Next.js, mobile) importent depuis `core/` :

**MVP Streamlit :**
```python
from core.parser import parse_csv
from core.scheduler import generate_schedule
from core.formatter import to_json
```

**API FastAPI (future) :**
```python
from core.scheduler import generate_schedule

@app.post("/api/schedule")
async def create_schedule(students: List[StudentDTO]):
    result = generate_schedule(students)
    return result
```

---

## 🚀 Performance

- **Phase 1 Skeleton** : < 0.5 sec
- **Phase 2 OR-Tools** : < 10 sec
- **Total** : < 10 sec CPU, < 100 MB RAM

---

## 📖 Documentation Complète

- **Tech-Spec** : `../_bmad-output/implementation-artifacts/tech-spec-algo-generation-planning.md`
- **Tests** : `../docs/guides/TESTING.md`
- **README principal** : `../README.md`

---

**Version :** 1.0.0 (Stable pour MVP)  
**License :** Privé  
**Maintainer :** Vincent
