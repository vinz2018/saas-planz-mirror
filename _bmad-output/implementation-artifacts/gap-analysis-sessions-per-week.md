# Gap Analysis - Contrainte `sessions_par_semaine`

**Analyste :** Mary  
**Date :** 2026-02-02  
**Criticité :** 🔴 HAUTE  
**Impact :** Code, Tests, Documentation, UI

---

## 🎯 Executive Summary

La contrainte **`sessions_par_semaine`** (nombre de cours par élève par semaine) est **PARTIELLEMENT implémentée** dans la codebase. Elle existe dans la spec, les modèles, le parser et l'algorithme OR-Tools, **MAIS** :

1. ❌ **Fichiers de test créés incorrectement** (format simplifié sans cette colonne)
2. ⚠️ **Documentation UI Streamlit incomplète** (pas de guidance sur ce champ critique)
3. ⚠️ **Explications unplaced manquantes** (ne mentionnent pas quota non atteint)
4. ⚠️ **Tests unitaires incomplets** (pas de test spécifique pour contrainte sessions_per_week)

**Recommandation :** Corrections immédiates + complétion documentation avant test avec Tony.

---

## 🔍 Détails de l'Analyse

### 1. ✅ **Spec Technique (COMPLET)**

**Fichier :** `_bmad-output/implementation-artifacts/tech-spec-algo-generation-planning.md`

**Status :** ✅ Bien spécifié

**Mentions :**
- Ligne 50 : Colonne `sessions_par_semaine` dans CSV
- Ligne 164 : Dataclass `Student` avec champ `sessions_per_week`
- Ligne 435 : Task "Define `Student` dataclass with fields: sessions_per_week"

**Extrait clé :**
```
- Colonnes : `nom, sessions_par_semaine, lundi_debut, lundi_fin, ...`
```

**Évaluation :** ✅ CONFORME

---

### 2. ✅ **Modèles de Données (COMPLET)**

**Fichier :** `core/models.py`

**Status :** ✅ Implémenté correctement

**Code :**
```python
@dataclass
class Student:
    name: str
    sessions_per_week: int  # ✅ Présent
    available_slots: List[Slot] = field(default_factory=list)
    linked_group: Optional[str] = None
    notes: str = ""
```

**Évaluation :** ✅ CONFORME

---

### 3. ✅ **Parser CSV (COMPLET)**

**Fichier :** `core/parser.py`

**Status :** ✅ Implémenté avec validation

**Code (lignes 159-162) :**
```python
sessions_per_week = int(row["sessions_par_semaine"])
if sessions_per_week <= 0 or sessions_per_week > 7:
    errors.append(
        f"Row {idx+2} ({name}): sessions_par_semaine must be 1-7, got {sessions_per_week}"
    )
```

**Validations présentes :**
- ✅ Colonne obligatoire
- ✅ Valeur 1-7 (raisonnable)
- ✅ Au moins `sessions_per_week` slots disponibles (ligne 207-210)

**Évaluation :** ✅ CONFORME

---

### 4. ✅ **Algorithme OR-Tools (COMPLET)**

**Fichier :** `core/scheduler.py`

**Status :** ✅ Implémenté comme contrainte hard

**Code (ligne 392-395) :**
```python
# Constraint 1: Each student placed exactly sessions_per_week times
for i, student in enumerate(students):
    student_vars = [assignments[(i, j)] for j in range(num_slots) if (i, j) in assignments]
    model.Add(sum(student_vars) == student.sessions_per_week)
```

**Fonctionnement :**
- Contrainte **HARD** : élève doit être placé **exactement** `sessions_per_week` fois
- Si impossible, élève va dans "unplaced"
- Gestion du partial linking : `min(sessions_per_week)` (ligne 458)

**Évaluation :** ✅ CONFORME

---

### 5. ✅ **Template CSV Officiel (COMPLET)**

**Fichier :** `docs/examples/template-disponibilites.csv`

**Status :** ✅ Colonne présente

**Header :**
```csv
nom,sessions_par_semaine,lundi_debut,lundi_fin,mardi_debut,mardi_fin,...
```

**Exemples :**
```csv
Vincent,2,,,17:00,18:30,,,,,12:00,13:30,,,jerome,
Jerome,1,,,17:00,18:30,,,,,,,,,vincent,Toujours avec Vincent
Hugo,2,08:00,09:00,,,,,08:00,09:00,,,,,
```

**Évaluation :** ✅ CONFORME

---

### 6. ✅ **Documentation Template (COMPLET)**

**Fichier :** `docs/examples/README-template.md`

**Status :** ✅ Documenté clairement

**Extrait (ligne 18) :**
```markdown
| `sessions_par_semaine` | Nombre de cours souhaités par semaine | `2` | ✅ Oui |
```

**Exemples fournis :**
- Vincent (2 sessions)
- Jerome (1 session)
- Guidance sur partial linking

**Évaluation :** ✅ CONFORME

---

### 7. ❌ **Fichiers de Test (INCOMPLETS - CRITIQUE)**

**Fichiers :** `docs/examples/test-cases/01-simple/disponibilites.csv`

**Status :** ❌ **FORMAT INCORRECT**

**Problème :** Header simplifié créé par erreur :
```csv
Nom,Lundi,Mardi,Mercredi,Jeudi,Vendredi,Samedi,Groupe_lié,Notes
```

**❌ Manque :**
- Colonne `sessions_par_semaine`
- Séparation `_debut` / `_fin` par jour
- Format HH:MM correct

**Devrait être :**
```csv
nom,sessions_par_semaine,lundi_debut,lundi_fin,mardi_debut,mardi_fin,...
```

**Impact :** 
- 🔴 **Fichier de test inutilisable** avec le parser actuel
- 🔴 **Parser va crasher** (colonne manquante)
- 🔴 **Test impossible** dans Streamlit

**Évaluation :** ❌ **NON CONFORME - BLOQUANT**

---

### 8. ⚠️ **UI Streamlit (INCOMPLET)**

**Fichier :** `apps/mvp-streamlit/app.py`

**Status :** ⚠️ Pas de guidance spécifique

**Ce qui manque :**
1. **Pas d'info-box** expliquant `sessions_par_semaine`
2. **Pas d'aperçu** des valeurs dans le CSV uploadé
3. **Pas de validation visuelle** avant génération
4. **Erreurs pas user-friendly** si colonne manquante

**Recommandation :**
```python
st.info("""
💡 **Colonne obligatoire :** `sessions_par_semaine`
   - Indiquez combien de cours chaque élève souhaite par semaine (1-7)
   - Exemple : Alice = 2 cours/semaine, Bob = 1 cours/semaine
""")
```

**Évaluation :** ⚠️ **AMÉLIORATION NÉCESSAIRE**

---

### 9. ⚠️ **Explications Unplaced (INCOMPLET)**

**Fichier :** `core/scheduler.py` (fonction `_generate_unplaced_explanation`)

**Status :** ⚠️ Ne mentionne pas quota non atteint

**Code actuel (ligne 640-680) :**
Explications basées sur :
- Pas de disponibilités
- Créneaux déjà remplis
- Groupe lié sans overlap

**Ce qui manque :**
```python
if student.sessions_per_week > len(placed_slots):
    suggestions.append(
        f"- Quota non atteint : demandait {student.sessions_per_week} cours/semaine, "
        f"seulement {len(placed_slots)} placé(s)"
    )
```

**Évaluation :** ⚠️ **AMÉLIORATION NÉCESSAIRE**

---

### 10. ⚠️ **Tests Unitaires (INCOMPLETS)**

**Fichiers :** `tests/test_parser.py`, `tests/test_scheduler.py`

**Status :** ⚠️ Pas de test spécifique pour `sessions_per_week`

**Tests existants :**
- ✅ Validation format CSV
- ✅ Parsing disponibilités
- ✅ Contraintes OR-Tools

**Tests manquants :**
```python
def test_sessions_per_week_constraint():
    """Test que chaque élève est placé exactement sessions_per_week fois."""
    # Alice: 2 sessions → doit avoir 2 cours
    # Bob: 1 session → doit avoir 1 cours
    # etc.
```

**Évaluation :** ⚠️ **AMÉLIORATION RECOMMANDÉE**

---

## 📋 Récapitulatif des Gaps

| Composant | Status | Criticité | Action |
|-----------|--------|-----------|--------|
| **Tech-Spec** | ✅ Complet | - | Aucune |
| **Modèles (`models.py`)** | ✅ Complet | - | Aucune |
| **Parser (`parser.py`)** | ✅ Complet | - | Aucune |
| **Scheduler (`scheduler.py`)** | ✅ Complet | - | Aucune |
| **Template CSV officiel** | ✅ Complet | - | Aucune |
| **Documentation template** | ✅ Complet | - | Aucune |
| **Fichiers de test** | ❌ Incorrect | 🔴 HAUTE | **Recréer immédiatement** |
| **UI Streamlit** | ⚠️ Incomplet | 🟡 MOYENNE | Ajouter guidance |
| **Explications unplaced** | ⚠️ Incomplet | 🟡 MOYENNE | Ajouter mention quota |
| **Tests unitaires** | ⚠️ Incomplet | 🟢 BASSE | Ajouter tests spécifiques |

---

## 🎯 Recommandations Prioritaires

### 🔴 **Priorité 1 : BLOCKER (Immédiat)**

**Problème :** Fichiers de test au mauvais format

**Action :**
1. **Supprimer** `docs/examples/test-cases/01-simple/disponibilites.csv` (format incorrect)
2. **Recréer** avec le bon format (incluant `sessions_par_semaine`)
3. **Vérifier** que tous les cas de test (02-05) utilisent le bon format

**Fichiers à corriger :**
- `docs/examples/test-cases/01-simple/disponibilites.csv` ❌
- `docs/examples/test-cases/02-moyen/disponibilites.csv` (à vérifier)
- `docs/examples/test-cases/03-complexe/disponibilites.csv` (à vérifier)
- `docs/examples/test-cases/04-tres-complexe/disponibilites.csv` (à vérifier)
- `docs/examples/test-cases/05-extreme/disponibilites.csv` (à vérifier)

**Exemple de contenu correct :**
```csv
nom,sessions_par_semaine,lundi_debut,lundi_fin,mardi_debut,mardi_fin,mercredi_debut,mercredi_fin,jeudi_debut,jeudi_fin,vendredi_debut,vendredi_fin,samedi_debut,samedi_fin,groupe_lie,notes
Alice,2,08:00,12:00,,,,09:00,11:00,,,,,,,,Débutante
Bob,1,,,14:00,18:00,14:00,17:00,14:00,16:00,,,,,Charlie,Niveau intermédiaire
Charlie,1,,,14:00,18:00,14:00,17:00,14:00,16:00,,,,,Bob,Niveau intermédiaire
David,1,,,,,,,,,08:00,12:00,09:00,13:00,,Expert
Emma,2,10:00,12:00,10:00,12:00,10:00,12:00,,,,,,,"Flexible, préfère le matin"
```

---

### 🟡 **Priorité 2 : IMPORTANT (Avant test avec Tony)**

**Problème :** UI Streamlit ne guide pas sur `sessions_par_semaine`

**Action :**
Ajouter dans `apps/mvp-streamlit/app.py` :

```python
st.info("""
💡 **Colonne obligatoire dans le CSV :** `sessions_par_semaine`

Indiquez combien de cours chaque élève souhaite par semaine :
- 1 cours/semaine : élève occasionnel
- 2 cours/semaine : élève régulier (le plus courant)
- 3+ cours/semaine : élève intensif

**Important :** L'algorithme placera chaque élève **exactement** ce nombre de fois. 
Si impossible, l'élève sera marqué "non placé" avec explication.
""")

# Après upload CSV, afficher aperçu
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success(f"✅ {len(df)} élèves chargés")
    
    # Vérifier colonne sessions_par_semaine
    if 'sessions_par_semaine' in df.columns:
        total_sessions = df['sessions_par_semaine'].sum()
        st.metric("Total cours à placer", total_sessions)
        st.caption(f"~{total_sessions} cours à générer (1h chacun)")
    else:
        st.error("❌ Colonne 'sessions_par_semaine' manquante dans le CSV")
```

---

### 🟢 **Priorité 3 : NICE TO HAVE (Amélioration continue)**

**1. Explications unplaced plus détaillées**

Ajouter dans `core/scheduler.py` :
```python
if len(placed_slots) < student.sessions_per_week:
    reasons.append(
        f"Quota non atteint : demandait {student.sessions_per_week} cours/semaine, "
        f"seulement {len(placed_slots)} cours placé(s)"
    )
    suggestions.append(
        f"- Augmenter les disponibilités pour atteindre {student.sessions_per_week} cours"
    )
```

**2. Tests unitaires spécifiques**

Créer `tests/test_sessions_per_week.py` :
```python
def test_exact_sessions_per_week_constraint():
    """Verify each student is placed exactly sessions_per_week times."""
    students = [
        Student("Alice", sessions_per_week=2, ...),
        Student("Bob", sessions_per_week=1, ...),
    ]
    result = generate_schedule(students, ...)
    
    # Count Alice in schedule
    alice_count = sum(1 for c in result.schedule if "Alice" in c.students)
    assert alice_count == 2, f"Alice should have 2 courses, got {alice_count}"
    
    # Count Bob in schedule
    bob_count = sum(1 for c in result.schedule if "Bob" in c.students)
    assert bob_count == 1, f"Bob should have 1 course, got {bob_count}"
```

---

## 💡 Réponse à la Question Initiale de Vincent

**Question :** "Nous avons perdu le nombre de cours par semaine pour une personne"

**Réponse :** Non, nous ne l'avons pas perdu ! 🎯

La contrainte **`sessions_par_semaine`** est **bien présente et fonctionnelle** dans :
- ✅ La tech-spec
- ✅ Les modèles de données
- ✅ Le parser CSV
- ✅ L'algorithme OR-Tools (contrainte hard)
- ✅ Le template CSV officiel
- ✅ La documentation

**MAIS** nous avons **un bug dans les fichiers de test** que je viens de créer, qui utilisent un format simplifié incorrect sans cette colonne.

**Impact :**
- Le **code core est OK** ✅
- Les **templates officiels sont OK** ✅
- Les **fichiers de test sont KO** ❌ (à recréer immédiatement)
- La **documentation UI pourrait être améliorée** ⚠️

---

## 📊 Métrique de Conformité

**Score global :** 8/10 (80%)

**Détail :**
- Spec/Code : 10/10 ✅
- Templates : 10/10 ✅
- Documentation : 9/10 ✅
- Tests : 4/10 ❌
- UI : 7/10 ⚠️

**Conclusion :** La contrainte est bien implémentée, mais les fichiers de test et l'UI nécessitent des corrections immédiates.

---

## 🚀 Plan d'Action

**Aujourd'hui (BLOCKER) :**
1. ✅ Recréer tous les fichiers de test CSV au bon format
2. ✅ Vérifier que le parser accepte les nouveaux fichiers
3. ✅ Tester 01-simple dans Streamlit

**Avant test avec Tony :**
4. ⚠️ Ajouter guidance UI pour `sessions_par_semaine`
5. ⚠️ Améliorer explications unplaced

**Backlog (Nice to have) :**
6. 🟢 Ajouter tests unitaires spécifiques
7. 🟢 Monitoring métrique (ratio placés vs sessions demandées)

---

**Analyste :** Mary  
**Confiance :** 95% (analysis basée sur code source complet)  
**Prochaine étape :** Corrections immédiates fichiers de test
