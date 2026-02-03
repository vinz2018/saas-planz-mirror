# SaaS Planz - Intelligent Scheduling Algorithm

Algorithme d'optimisation pour la génération automatique de planning sportif avec contraintes multiples.

**Structure :** Monorepo avec `core/` réutilisable et `apps/` par phase

---

## ⚡ Quick Start

```bash
./run-mvp.sh start
open http://localhost:8501
```

**Guide complet :** Voir `QUICKSTART.md`

---

## 🎯 Objectif

Automatiser la création du planning hebdomadaire de Tony (coach sportif) avec ~50 élèves, en gérant :
- Disponibilités changeantes des élèves
- Groupes liés (couples/amis)
- Créneaux récurrents (habitudes)
- Contraintes physiques (capacité garage, durée cours)

**Gain de temps :** De 3-4h à 30 min par semaine

---

## 🏗️ Architecture

### Algorithme 2 Phases

**Phase 1 - Squelette (< 1 sec) :**
- Place les créneaux récurrents pré-définis
- Valide l'absence de conflits
- Réduit l'espace de recherche de ~90%

**Phase 2 - Variations (< 10 sec) :**
- OR-Tools CP-SAT optimise les créneaux variables
- Génère solution complète ou partielle avec explications
- Progressive relaxation si contraintes incompatibles

### Contraintes

**Hard (doivent être respectées) :**
- **UN SEUL COURS À LA FOIS** (pas de chevauchement)
- 2-3 élèves par cours + Tony
- Cours exactement 1h (start :00 ou :30)
- Groupes liés ensemble (partial linking si sessions différentes)
- Slots réservés coach jamais utilisés

**Soft (à maximiser) :**
- Respect habitudes récurrentes (poids 10)
- Distribution équilibrée jours (poids 5)
- Remplir cours existants vs nouveau (poids 3)

---

## 📦 Installation

### Option 1: Docker (Recommandé - Rien à installer sur ton PC)

```bash
# Lancer l'application MVP Streamlit
./run-mvp.sh start

# Ou directement depuis le dossier MVP
cd apps/mvp-streamlit
./docker-dev.sh start

# Ouvrir http://localhost:8501
```

**Guide complet:** Voir `docs/docker/DOCKER_GUIDE.md` ou `docs/docker/DOCKER_QUICKSTART.md`

### Option 2: Installation Locale

```bash
# Créer environnement virtuel
python3 -m venv venv
source venv/bin/activate  # Sur Mac/Linux
# venv\Scripts\activate  # Sur Windows

# Installer dépendances
pip install -r requirements.txt
```

---

## 🚀 Usage

### Avec Docker

```bash
# Démarrer l'app MVP
./run-mvp.sh start

# Ouvrir http://localhost:8501 dans le navigateur

# Voir les logs
./run-mvp.sh logs

# Tester
./run-mvp.sh test

# Arrêter
./run-mvp.sh stop
```

### Sans Docker

### 1. Préparer les données

**Template disponibilités élèves :** `docs/examples/template-disponibilites.csv`

```csv
nom,sessions_par_semaine,lundi_debut,lundi_fin,mardi_debut,mardi_fin,...,groupe_lie,notes
Vincent,2,,,17:00,18:30,,,,,12:00,13:30,,,jerome,
Jerome,1,,,17:00,18:30,,,,,,,,,vincent,
```

**Template créneaux récurrents :** `docs/examples/template-recurring-slots.csv`

```csv
nom,jour,heure_debut,heure_fin
Vincent,mardi,17:00,18:00
Jerome,mardi,17:00,18:00
```

### 2. Lancer l'application Streamlit (MVP)

```bash
streamlit run app.py
```

- Upload les CSVs
- Bloquer créneaux personnels coach
- Cliquer "Générer Planning"
- Télécharger résultats (JSON + Markdown)

---

## 🧪 Tests

```bash
# Lancer tous les tests
pytest

# Avec coverage
pytest --cov=src --cov-report=html

# Tests spécifiques
pytest tests/test_parser.py -v

# Ou avec Docker
./scripts/docker-dev.sh test
```

**Guide de tests complet:** Voir `docs/guides/TESTING.md`

---

## 📁 Structure du Projet

```
saas-planz/
├── core/                   # Logique métier réutilisable
│   ├── models.py           # Dataclasses: Student, Slot, Schedule
│   ├── parser.py           # CSV parsing & validation
│   ├── scheduler.py        # OR-Tools optimization
│   └── formatter.py        # JSON + Markdown output
│
├── apps/                   # Différentes interfaces/phases
│   └── mvp-streamlit/      # MVP actuel (Phase exploratoire)
│       ├── app.py          # Interface Streamlit
│       ├── Dockerfile
│       ├── docker-compose.yml
│       └── docker-dev.sh
│
├── tests/                  # Tests du core
├── docs/                   # Documentation
├── scripts/                # Scripts utilitaires
└── README.md
```

---

## ✅ État Actuel (MVP Ready - Structure Core/Apps)

**✅ Phase 1: Foundation (Models + Parser)**
- [x] Data models (`src/models.py`) - 220 lignes
- [x] CSV parser with validation (`src/parser.py`) - 340 lignes
- [x] Parser tests (`tests/test_parser.py`) - 320 lignes
- [x] Manual tests validated (20+ assertions passed)

**✅ Phase 2: Scheduler Core (OR-Tools)**
- [x] Phase 1 Skeleton algorithm (`src/scheduler.py`) - 650 lignes
- [x] Phase 2 OR-Tools optimization with CP-SAT
- [x] Graceful degradation + explanations
- [x] Progressive timeout strategy (0-5s, 5-10s, 10-15s)
- [x] Scheduler tests (`tests/test_scheduler.py`)
- ⚠️ **Requires OR-Tools:** `pip install ortools`

**✅ Phase 3: Output Formatting**
- [x] JSON formatter (`src/formatter.py`) - 200 lignes
- [x] Markdown formatter with emoji indicators
- [x] Save/export functions

**✅ Phase 4: Streamlit UI**
- [x] File upload (`app.py`) - 300 lignes
- [x] Coach reserved slots UI
- [x] Results display (grouped by day)
- [x] Download buttons (JSON + Markdown)
- [x] Error handling with friendly messages
- ⚠️ **Requires Streamlit:** `pip install streamlit`

**⏳ Phase 5: Testing & Deployment** (optional)
- [x] README with full documentation
- [x] Manual test scripts (models, parser)
- [ ] Install dependencies (pandas, ortools, streamlit, pytest)
- [ ] Run full test suite
- [ ] Performance benchmarks
- [ ] Integration tests end-to-end

---

## 🎯 Prochaines Étapes (Pour Lancer le MVP)

### Option 1: Avec Docker (Recommandé)

```bash
./scripts/docker-dev.sh start
```

### Option 2: Installation Locale

1. **Installer les dépendances** (obligatoire)
   ```bash
   bash scripts/install.sh
   # ou manuellement:
   pip install pandas ortools streamlit pytest
   ```

2. **Tester le parser** (validé sans dépendances)
   ```bash
   python3 scripts/test_models_only.py  # ✅ Déjà validé (20+ tests)
   ```

3. **Lancer l'application Streamlit**
   ```bash
   streamlit run app.py
   ```

4. **Utiliser l'interface:**
   - Télécharger les templates
   - Remplir le CSV avec les disponibilités
   - Upload dans l'interface
   - Bloquer tes créneaux personnels
   - Cliquer "Générer Planning"
   - Télécharger les résultats (JSON + Markdown)

5. **Tests complets** (optionnel, après installation)
   ```bash
   pytest -v  # Tous les tests
   pytest tests/test_parser.py -v  # Tests parser
   ```

---

## 📊 Performance Targets

- Phase 1 (Squelette): < 0.5 sec
- Phase 2 (OR-Tools): < 10 sec
- **Total**: < 10 sec CPU, < 100 MB RAM
- **Scalabilité**: 100 coachs sur VPS 2 cores @ 10€/mois

---

## 📚 Documentation

### Implémentation
- **Tech-Spec complète** : `_bmad-output/implementation-artifacts/tech-spec-algo-generation-planning.md`
- **Rapport d'implémentation** : `docs/implementation/IMPLEMENTATION_COMPLETE.md`
- **Self-check report** : `docs/implementation/SELF_CHECK_REPORT.md`

### Docker
- **Quick Start** : `docs/docker/DOCKER_QUICKSTART.md`
- **Guide complet** : `docs/docker/DOCKER_GUIDE.md`
- **Setup complet** : `docs/docker/DOCKER_SETUP_COMPLETE.md`

### Guides
- **Guide de tests** : `docs/guides/TESTING.md`
- **Instructions templates** : `docs/examples/README-*.md`

### Brainstorming
- **Session initiale** : `_bmad-output/brainstorming/brainstorming-session-2026-02-01.md`

---

## 📝 License

Projet privé - © 2026
