---
title: 'Amélioration UI/UX MVP Streamlit pour Tony'
slug: 'amelioration-ui-ux-mvp-streamlit'
created: '2026-02-04'
status: 'ready-for-dev'
stepsCompleted: [1, 2, 3, 4]
tech_stack: ['Streamlit', 'Python 3.10+', 'pandas', 'pathlib']
files_to_modify: ['apps/mvp-streamlit/app.py']
code_patterns: ['st.sidebar for navigation', 'st.columns() for layouts', 'st.expander() for collapsible content', 'st.session_state for persistence', 'st.file_uploader() for CSV', 'exception handling with ParseError']
test_patterns: ['manual testing in Streamlit', '6 test-cases in docs/examples/test-cases/', 'pytest for core modules (not UI)']
---

# Tech-Spec: Amélioration UI/UX MVP Streamlit pour Tony

**Created:** 2026-02-04

## Overview

### Problem Statement

L'interface Streamlit MVP (`apps/mvp-streamlit/app.py`) fonctionne et génère des plannings corrects, mais manque de guidage pour Tony (utilisateur final, coach sportif avec background tech).

**Problèmes identifiés :**
- Pas d'exemples concrets de remplissage CSV (difficile de comprendre le format attendu)
- Messages d'erreur en anglais et génériques (ParseError, Exception)
- Pas de FAQ/aide contextuelle accessible rapidement
- Affichage des résultats basique (liste de cours par jour, peu visuel)
- Warnings d'optimisation présents mais peu mis en avant

**Objectif :** Rendre l'interface plus intuitive et guidée pour Tony, avec exemples pratiques, FAQ, messages clairs, et visualisation type agenda.

### Solution

**Améliorer l'UI/UX en 5 axes :**

1. **Page Documentation & Aide séparée** (éviter surcharge sidebar)
   - Utiliser `st.Page` ou navigation pour créer page dédiée
   - Contenu : 3 exemples disponibilités (simple, moyen, complexe) + 1 exemple récurrents
   - Format : "Cas concret → Correspondance CSV"
   - FAQ intégrée : 6 questions fréquentes avec réponses claires

3. **Messages d'erreur en français**
   - Traduction complète des erreurs (y compris messages ParseError anglais)
   - Cas spécifiques : formatage CSV, colonnes manquantes
   - Suggestions d'action concrètes
   - Fonction de traduction pour convertir messages anglais → français

4. **Calendrier visuel façon agenda**
   - Grille hebdomadaire (jours × heures)
   - Voir tout le planning d'un coup d'œil
   - Conserver aussi la vue détaillée actuelle

5. **Amélioration des warnings**
   - Mise en avant des suggestions d'optimisation
   - Explications plus claires

### Scope

**In Scope:**
- Création page "Documentation & Aide" séparée avec exemples pratiques (3 cas disponibilités + 1 récurrents) + FAQ (6 questions)
- Traduction COMPLÈTE messages d'erreur en français (pandas errors + ParseError avec dictionnaire traduction)
- Création composant calendrier visuel grille hebdomadaire
- Amélioration affichage warnings/optimisations

**Out of Scope:**
- Modification de la logique métier (`core/` modules)
- Ajout de nouvelles fonctionnalités de scheduling
- Export PDF/Excel (JSON/Markdown déjà disponibles)
- Authentification ou multi-utilisateurs
- Changement de framework (reste Streamlit)
- Optimisation de performance backend

## Context for Development

### Codebase Patterns

**Structure actuelle :**
```
apps/mvp-streamlit/
├── app.py (401 lignes)         # Interface Streamlit complète
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

**app.py - Structure actuelle :**
- Ligne 23-27 : `st.set_page_config()` - Configuration page
- Ligne 42-77 : Sidebar - Templates download (disponibilités, récurrents)
- Ligne 80-172 : Étape 1 - Upload fichiers + preview
- Ligne 176-231 : Étape 2 - Bloquer créneaux coach
- Ligne 237-292 : Étape 3 - Génération planning
- Ligne 295-396 : Affichage résultats (par jour, warnings, unplaced, download)

**Patterns Streamlit utilisés :**
- `st.sidebar` pour navigation latérale
- `st.columns()` pour layout multi-colonnes
- `st.expander()` pour contenu collapsible
- `st.file_uploader()` pour upload CSV
- `st.session_state` pour persistance données
- `st.metric()` pour afficher KPIs
- `st.success/error/warning/info()` pour messages

**Imports core/ utilisés :**
```python
from core.parser import parse_csv, ParseError
from core.scheduler import generate_schedule
from core.formatter import to_json, to_markdown
from core.models import Slot
```

### Files to Reference

| File | Lines | Purpose | Zones Exactes |
| ---- | ----- | ------- | -------------- |
| `apps/mvp-streamlit/app.py` | 401 | Interface Streamlit complète | L42-77 (sidebar), L138-139 (erreur upload), L170-171 (erreur upload récurrents), L287-292 (erreur parsing), L295-396 (résultats) |
| `docs/examples/template-disponibilites.csv` | 11 | Template CSV disponibilités (10 élèves exemples) | Base pour exemples sidebar |
| `docs/examples/template-recurring-slots.csv` | 7 | Template CSV créneaux récurrents (6 créneaux) | Base pour exemples sidebar |
| `docs/examples/test-cases/01-simple/` | - | Test case simple (5 élèves, 2 groupes) | Exemple "simple" pour sidebar |
| `docs/examples/test-cases/02-moyen/` | - | Test case moyen (9 élèves, 4 groupes) | Exemple "moyen" pour sidebar |
| `docs/examples/test-cases/03-complexe/` | - | Test case complexe (14 élèves, 6 groupes) | Exemple "complexe" pour sidebar |
| `core/parser.py` | 553 | Parse CSV - génère `ParseError` | L46-48 (ParseError class), L69-80 (messages anglais) |
| `core/models.py` | 192 | Dataclasses - `Slot` utilisé dans app.py | Aucune modification nécessaire |

### Technical Decisions

**Décision 1 : Page Documentation séparée (pas sidebar)**
- **Pourquoi :** Éviter surcharge sidebar avec 4 expanders exemples + 6-8 FAQ
- **Alternative rejetée :** Tout dans sidebar (scroll infini, mauvaise UX)
- **Impact :** Navigation plus claire, sidebar reste légère pour templates

**Décision 2 : Calendrier visuel en plus (pas remplacement)**
- **Pourquoi :** Vue liste actuelle utile pour détails, calendrier pour vue d'ensemble
- **Approche :** Ajouter onglets (tabs) ou expanders pour choisir vue
- **Impact :** Utilisateur peut choisir selon besoin (détails vs overview)

**Décision 3 : Messages d'erreur - Catch spécifiques**
- **Pourquoi :** Actuellement `except Exception` générique (ligne 289)
- **Approche :** Ajouter `except pandas.errors.ParserError`, `except KeyError` pour colonnes manquantes
- **Impact :** Messages plus précis et actionnables

**Décision 4 : FAQ statique (pas dynamique/context-aware)**
- **Pourquoi :** Tony a background tech, FAQ simple suffit
- **Alternative rejetée :** Aide contextuelle qui change selon l'étape (trop complexe pour MVP)
- **Impact :** FAQ accessible à tout moment, facile à maintenir

**Décision 5 : Traduction messages erreur par dictionnaire**
- **Pourquoi :** Messages ParseError sont en anglais dans core/parser.py (out of scope de modifier)
- **Approche :** Créer dictionnaire de traduction EN→FR dans app.py
- **Limitation MVP acceptée :** Détection basée sur strings, fragile si messages changent
- **Impact :** Expérience utilisateur 100% française, maintenance simple du dictionnaire

### Investigation Results - Zones Exactes

**1. Création page Documentation séparée**
- Actuellement : 1 page unique avec toute l'interface
- À créer : Page "Documentation & Aide" accessible via navigation
- Pattern : `st.Page()` ou menu sidebar avec lien vers page dédiée
- Contenu : Exemples Pratiques + FAQ

**2. Messages erreur upload - Lignes 138-139 et 170-171**
```python
# Actuel (ligne 138-139):
except Exception as e:
    st.error(f"❌ Erreur lors de la lecture du CSV: {e}")
```
- Problème : Exception trop générique
- Solution : Catch pandas.errors.ParserError, EmptyDataError, KeyError

**3. Messages erreur parsing - Lignes 287-292**
```python
# Actuel:
except ParseError as e:
    st.error(f"❌ Erreur de parsing CSV: {e}")
except Exception as e:
    st.error(f"❌ Erreur: {e}")
    import traceback
    st.code(traceback.format_exc())
```
- ParseError vient de core/parser.py (ligne 46-48)
- Messages actuels en anglais (ex: "Invalid time format")
- Solution : Wrapper traduction ou améliorer présentation

**4. Affichage résultats - Après ligne 295**
- Insérer calendrier visuel avant la liste par jour (ligne 302)
- Utiliser `st.tabs()` pour deux vues : Calendrier / Détails
- Calendrier : grille jours × heures

**Exemples CSV pour documentation (identifiés) :**
- Simple : `/docs/examples/test-cases/01-simple/` (5 élèves, Alice dispo lundi matin)
- Moyen : `/docs/examples/test-cases/02-moyen/` (9 élèves, Sophie+Julie groupe)
- Complexe : `/docs/examples/test-cases/03-complexe/` (14 élèves, horaires variés)

## Implementation Plan

### Tasks

**Phase 1 : Création Page Documentation & Aide**

- [ ] **Task 1.1 : Créer page "Documentation & Aide" séparée**
  - Fichier : `apps/mvp-streamlit/app.py` (ou créer `apps/mvp-streamlit/pages/documentation.py` si architecture multi-pages)
  - Actions :
    1. Décider approche : `st.Page()` multipage OU lien sidebar vers section dédiée
    2. Si multipage : Créer `pages/documentation.py` avec navigation automatique Streamlit
    3. Si section : Ajouter état navigation dans `st.session_state` + menu sidebar
  - Contenu de la page :
    - Header : "📚 Documentation & Aide - SaaS Planz"
    - Section 1 : "Exemples Pratiques" (4 expanders)
    - Section 2 : "FAQ" (6 questions)
    - Lien retour vers page principale

- [ ] **Task 1.2 : Remplir section "Exemples Pratiques"**
  - Fichier : Page documentation créée en Task 1.1
  - Contenu à ajouter :
    - **Exemple Simple** : "Alice veut 2 cours/semaine, dispo lundi 08:00-12:00 et mercredi 09:00-11:00"
      ```
      nom,sessions_par_semaine,lundi_debut,lundi_fin,mercredi_debut,mercredi_fin,...
      Alice,2,08:00,12:00,09:00,11:00,,,,,,,,,
      ```
    - **Exemple Moyen** : "Sophie et Julie veulent 2 cours/semaine ensemble (groupe lié)"
      ```
      Sophie,2,09:00,12:00,,,14:00,17:00,,,,,Julie,
      Julie,2,09:00,12:00,,,14:00,17:00,,,,,Sophie,
      ```
    - **Exemple Complexe** : "Camille veut 3 cours/semaine, horaires variés avec :30"
      ```
      Camille,3,08:30,12:00,08:30,12:00,08:30,12:00,,,09:00,13:00,09:00,12:00,,
      ```
    - **Exemple Récurrents** : "Vincent veut TOUJOURS être le mardi 17:00-18:00"
      ```
      nom,jour,heure_debut,heure_fin
      Vincent,mardi,17:00,18:00
      ```

- [ ] **Task 1.3 : Remplir section "FAQ"**
  - Fichier : Page documentation créée en Task 1.1
  - Questions à ajouter (6 expanders) :
    1. "Pourquoi un élève n'est pas placé ?" → Expliquer contraintes (dispo insuffisantes, conflits groupes liés, créneaux réservés coach)
    2. "Que signifie 'sessions_par_semaine' ?" → Expliquer que c'est le nombre EXACT de cours souhaité par semaine
    3. "Comment créer un groupe lié ?" → Expliquer colonne `groupe_lie` avec noms mutuels (ex: Alice met "Bob", Bob met "Alice")
    4. "Que faire si le planning ne me convient pas ?" → Suggérer ajuster disponibilités élèves, ajouter créneaux réservés, ou modifier récurrents
    5. "Différence entre disponibilités et créneaux récurrents ?" → Expliquer récurrent = créneau FIXE garanti, dispo = plages flexibles où algorithme place
    6. "Comment bloquer mes créneaux personnels ?" → Référence à l'Étape 2 de l'interface principale

- [ ] **Task 1.4 : Ajouter lien vers Documentation dans sidebar**
  - Fichier : `apps/mvp-streamlit/app.py`
  - Position : Remplacer ligne 75-77 (lien actuel vers docs/examples)
  - Actions :
    1. Si multipage : Streamlit gère automatiquement navigation
    2. Si section : Ajouter bouton/lien cliquable qui change état navigation
    3. Texte : "📚 Documentation & Aide" avec icône claire

**Phase 2 : Amélioration Messages d'Erreur**

- [ ] **Task 2.0 : Créer fonction traduction messages erreur EN→FR**
  - Fichier : `apps/mvp-streamlit/app.py`
  - Position : Après imports, avant fonction `main()`
  - Actions :
    1. Créer dictionnaire de traduction :
       ```python
       ERROR_TRANSLATIONS = {
           "Invalid time format": "Format d'heure invalide",
           "Expected HH:MM": "Attendu au format HH:MM",
           "Times must end in :00 or :30": "Les heures doivent se terminer par :00 ou :30",
           "Invalid hour": "Heure invalide",
           "Must be 0-23": "Doit être entre 0 et 23",
           "Invalid time granularity": "Granularité d'heure invalide",
           "start": "début",
           "end": "fin",
           "must be before": "doit être avant",
           "Invalid time range": "Plage horaire invalide",
       }
       ```
    2. Créer fonction de traduction :
       ```python
       def translate_error_message(error_msg: str) -> str:
           """Traduit les messages d'erreur anglais en français.
           
           Limitation MVP: Traduction basée sur strings, fragile si messages 
           dans core/parser.py changent. Pour robustesse future, créer des 
           codes d'erreur ou exceptions typées.
           """
           translated = error_msg
           for en, fr in ERROR_TRANSLATIONS.items():
               translated = translated.replace(en, fr)
           return translated
       ```

- [ ] **Task 2.1 : Améliorer gestion erreurs upload CSV disponibilités**
  - Fichier : `apps/mvp-streamlit/app.py`
  - Position : Lignes 138-139 (bloc `except Exception`)
  - Actions :
    1. Ajouter imports en haut du fichier : `from pandas.errors import ParserError, EmptyDataError`
    2. Remplacer le catch générique par catches spécifiques :
       ```python
       except ParserError as e:
           st.error("❌ **Erreur de format CSV**")
           st.warning("Le fichier ne semble pas être un CSV valide. Vérifiez que :")
           st.markdown("- Les colonnes sont séparées par des **virgules** (`,`)")
           st.markdown("- Le fichier n'est pas au format Excel (.xlsx)")
           st.markdown("- Le fichier est encodé en **UTF-8**")
           st.info("💡 Téléchargez le template fourni pour voir le format attendu.")
       except EmptyDataError:
           st.error("❌ **Fichier vide**")
           st.warning("Le CSV ne contient aucune donnée. Ajoutez au moins un élève.")
       except KeyError as e:
           st.error(f"❌ **Colonne manquante : {e}**")
           st.warning("Le CSV doit contenir toutes les colonnes obligatoires.")
           st.info("💡 Téléchargez le template fourni pour voir les colonnes requises.")
       except Exception as e:
           st.error(f"❌ Erreur inattendue : {e}")
       ```

- [ ] **Task 2.2 : Améliorer gestion erreurs upload CSV récurrents**
  - Fichier : `apps/mvp-streamlit/app.py`
  - Position : Lignes 170-171 (bloc `except Exception`)
  - Actions : Appliquer même pattern que Task 2.1 avec messages adaptés pour récurrents

- [ ] **Task 2.3 : Améliorer présentation erreurs ParseError lors génération**
  - Fichier : `apps/mvp-streamlit/app.py`
  - Position : Lignes 287-292 (blocs `except ParseError` et `except Exception`)
  - Actions :
    1. Traduire et améliorer présentation ParseError :
       ```python
       except ParseError as e:
           st.error("❌ **Erreur de validation CSV**")
           # Traduire le message d'erreur
           error_msg_fr = translate_error_message(str(e))
           st.warning(f"**Détail :** {error_msg_fr}")
           
           # Détecter le type d'erreur et suggérer solution
           error_msg = str(e).lower()
           if "invalid time format" in error_msg or "format" in error_msg:
               st.info("💡 Les heures doivent être au format HH:MM (ex: 08:00, 17:30)")
           elif "granularity" in error_msg or ":00 or :30" in error_msg:
               st.info("💡 Les minutes doivent être :00 ou :30 uniquement")
           elif "missing column" in error_msg or "column" in error_msg:
               st.info("💡 Vérifiez que toutes les colonnes obligatoires sont présentes")
           else:
               st.info("💡 Vérifiez le format de votre CSV avec le template fourni")
       ```
    2. Garder le catch Exception générique mais masquer traceback par défaut :
       ```python
       except Exception as e:
           st.error(f"❌ **Erreur lors de la génération :** {type(e).__name__}")
           st.warning(str(e))
           with st.expander("🔍 Détails techniques (pour debug)"):
               import traceback
               st.code(traceback.format_exc())
       ```

**Phase 3 : Calendrier Visuel**

- [ ] **Task 3.1 : Créer composant calendrier grille hebdomadaire**
  - Fichier : `apps/mvp-streamlit/app.py`
  - Position : Après ligne 300 (après métriques résumé), avant "Planning Hebdomadaire"
  - Actions :
    1. Utiliser `st.tabs()` pour créer 2 vues :
       ```python
       tab_calendar, tab_list = st.tabs(["📅 Vue Calendrier", "📋 Vue Détaillée"])
       ```
    2. Dans `tab_calendar` : Créer grille avec `st.columns()` pour les jours
    3. Pour chaque jour : Afficher créneaux horaires avec cours
    4. Logique de construction :
       - Extraire heures min/max du planning (ex: 08:00-19:00)
       - Créer colonnes pour chaque jour (Lun, Mar, Mer, Jeu, Ven, Sam)
       - Pour chaque slot horaire, afficher cours ou vide
    5. Styling :
       - Utiliser `st.markdown()` avec HTML/CSS inline si nécessaire
       - Cours avec 1 élève → Badge "⚠️ Optimisable"
       - Cours avec 2+ élèves → Badge "✅ OK"
       - Cases vides → "-"

- [ ] **Task 3.2 : Déplacer la vue liste détaillée dans l'onglet dédié**
  - Fichier : `apps/mvp-streamlit/app.py`
  - Position : Code existant lignes 302-324 (boucle sur jours avec expanders)
  - Actions :
    1. Enrober tout le code existant de la section "Planning Hebdomadaire" dans `with tab_list:`
    2. Aucune modification du contenu, juste indentation

**Phase 4 : Amélioration Warnings**

- [ ] **Task 4.1 : Mettre en avant les warnings avec styling amélioré**
  - Fichier : `apps/mvp-streamlit/app.py`
  - Position : Lignes 326-343 (section warnings existante)
  - Actions :
    1. Remplacer `st.info()` par une présentation plus visible :
       ```python
       st.warning(f"⚠️ **{len(result.warnings)} créneau(x) à optimiser**")
       st.markdown("""
       💡 **Pourquoi optimiser ?**
       - Un cours avec 1 seul élève est moins rentable
       - D'autres élèves sont disponibles sur ces créneaux
       - Vous pouvez ajouter ces élèves pour rentabiliser le créneau
       """)
       ```
    2. Améliorer présentation dans expanders :
       - Ajouter badge "⚠️ 1 élève" visible
       - Mettre suggestions en liste numérotée avec actions claires
       - Ajouter bouton "Comment faire ?" qui explique comment ajouter dans CSV récurrents

### Acceptance Criteria

**Page Documentation :**
- **Given** la navigation de l'application
  **When** l'utilisateur accède à "Documentation & Aide"
  **Then** une page dédiée s'affiche avec sections "Exemples Pratiques" et "FAQ"

**Exemples CSV :**
- **Given** la page Documentation
  **When** l'utilisateur consulte la section "Exemples pratiques"
  **Then** 3 exemples disponibilités (simple, moyen, complexe) et 1 exemple récurrents sont affichés avec format "Cas → CSV"

**FAQ :**
- **Given** la page Documentation
  **When** l'utilisateur consulte la section "FAQ"
  **Then** 6 questions fréquentes avec réponses claires sont affichées

**Messages d'erreur français :**
- **Given** un CSV mal formaté (virgules manquantes)
  **When** l'utilisateur tente de charger le fichier
  **Then** message d'erreur en français avec suggestion "vérifier les virgules de séparation"

- **Given** un CSV sans colonne `sessions_par_semaine`
  **When** l'utilisateur tente de générer le planning
  **Then** message d'erreur en français avec suggestion "télécharger le template et vérifier les colonnes"

- **Given** une erreur ParseError (ex: "Invalid time format: '25:00'")
  **When** l'erreur est affichée à l'utilisateur
  **Then** le message est traduit en français (ex: "Format d'heure invalide: '25:00'")

**Calendrier visuel :**
- **Given** un planning généré avec succès
  **When** l'utilisateur consulte les résultats
  **Then** une grille hebdomadaire (jours × heures) affiche les cours de manière visuelle type agenda

- **Given** le calendrier visuel
  **When** un créneau contient 1 seul élève
  **Then** le créneau est marqué visuellement (couleur/icône) pour indiquer optimisation possible

**Warnings améliorés :**
- **Given** un planning avec warnings d'optimisation
  **When** l'utilisateur consulte les avertissements
  **Then** les suggestions sont mises en avant avec explications claires et actionnables

## Additional Context

### Dependencies

**Aucune nouvelle dépendance requise.**

Stack actuelle utilisée :
- `streamlit` (déjà installé)
- `pandas` (déjà installé)
- `pathlib`, `tempfile`, `datetime` (stdlib Python)

### Testing Strategy

**Tests manuels dans Streamlit :**
1. Lancer `./run-mvp.sh start` ou `docker-compose -f apps/mvp-streamlit/docker-compose.yml up`
2. Tester chaque amélioration :
   - Naviguer vers page "Documentation & Aide" → Vérifier page accessible
   - Consulter exemples CSV → Vérifier 3+1 exemples présents et lisibles
   - Consulter FAQ → Vérifier 6 questions/réponses claires
   - Upload CSV mal formaté → Vérifier message français avec suggestion
   - Upload CSV sans colonne → Vérifier message français avec suggestion
   - Upload CSV avec heure invalide (ex: 25:00) → Vérifier message traduit en français
   - Générer planning test-case → Vérifier calendrier visuel affiché
   - Vérifier warnings optimisation bien mis en avant
3. Tester avec les 6 test cases existants (01-simple à 05-extreme + demo-warnings)

**Seuil de succès :**
- Page Documentation & Aide accessible et lisible
- Toutes les nouvelles sections UI visibles et fonctionnelles
- Messages d'erreur 100% en français (y compris ParseError traduits)
- Calendrier visuel affiche correctement les créneaux
- Aucune régression sur génération de planning

### Notes

**Utilisateur final : Tony**
- Coach sportif avec background tech
- Comprend les concepts tech mais apprécie guidage clair
- Utilise l'outil pour générer plannings hebdomadaires élèves

**Style à préserver :**
- Interface en français (déjà le cas)
- Ton professionnel mais accessible
- Icônes emoji pour rendre visuel (déjà utilisé : 📅, ✅, ❌, ⚠️, 🔒, etc.)

**Après cette amélioration :**
- Interface prête pour présentation finale à Tony
- Base solide pour futures évolutions (export PDF, notifications, etc.)
- Documentation utilisateur intégrée directement dans l'app
