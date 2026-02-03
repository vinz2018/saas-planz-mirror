# 📁 Structure du Projet SaaS Planz

Structure organisée et propre après réorganisation (2026-02-02).

---

## 🌳 Arborescence

```
saas-planz/
│
├── 📄 README.md                    # Point d'entrée principal
├── 📋 requirements.txt             # Dépendances (racine)
├── 🔒 .dockerignore                # Exclusions Docker
├── 🔒 .gitignore                   # Exclusions git
├── 🚀 run-mvp.sh                   # Launcher rapide MVP
│
├── 🔷 core/                        # LOGIQUE MÉTIER (réutilisable)
│   ├── README.md                   # Doc API core
│   ├── __init__.py
│   ├── models.py                   # Dataclasses (220 lignes)
│   ├── parser.py                   # Parsing CSV (340 lignes)
│   ├── scheduler.py                # OR-Tools algo (650 lignes)
│   └── formatter.py                # Export JSON/Markdown (200 lignes)
│
├── 📱 apps/                        # INTERFACES PAR PHASE
│   ├── README.md                   # Index apps
│   │
│   └── mvp-streamlit/              # MVP Phase 1 (exploratoire)
│       ├── README.md               # Doc MVP
│       ├── app.py                  # UI Streamlit
│       ├── Dockerfile              # Image Docker MVP
│       ├── docker-compose.yml      # Orchestration MVP
│       ├── requirements.txt        # Deps MVP
│       └── docker-dev.sh           # Dev commands MVP
│
├── 🧪 tests/                       # TESTS DU CORE
│   ├── __init__.py
│   ├── conftest.py                 # Pytest config
│   ├── test_parser.py              # Tests parser (40+ cases)
│   ├── test_scheduler.py           # Tests scheduler
│   ├── test_integration.py         # Tests end-to-end
│   └── fixtures/                   # Fixtures CSV
│       ├── test_schedule.csv       # 10 étudiants
│       └── test_recurring_slots.csv
│
├── 📚 docs/                        # DOCUMENTATION
│   ├── README.md                   # Index documentation
│   │
│   ├── examples/                   # TEMPLATES CSV
│   │   ├── template-disponibilites.csv
│   │   ├── template-recurring-slots.csv
│   │   ├── README-template.md
│   │   └── README-recurring-slots.md
│   │
│   ├── implementation/             # DOCS IMPLÉMENTATION
│   │   ├── IMPLEMENTATION_COMPLETE.md
│   │   └── SELF_CHECK_REPORT.md
│   │
│   ├── docker/                     # DOCS DOCKER
│   │   ├── DOCKER_QUICKSTART.md
│   │   ├── DOCKER_GUIDE.md
│   │   ├── DOCKER_SETUP_COMPLETE.md
│   │   └── DOCKER_RECAP.txt
│   │
│   └── guides/                     # GUIDES GÉNÉRAUX
│       └── TESTING.md
│
├── 🔧 scripts/                     # SCRIPTS UTILITAIRES
│   ├── README.md                   # Index scripts
│   ├── install.sh                  # Install dépendances
│   ├── test_models_only.py         # Tests modèles (no deps)
│   ├── manual_test.py              # Tests parser
│   └── test_scheduler_manual.py    # Tests scheduler
│
└── 🔐 _bmad-output/                # BMAD artifacts
    ├── brainstorming/
    └── implementation-artifacts/
```

---

## 📊 Statistiques

### Code Source
- **src/** : 4 fichiers, ~1,410 lignes
- **tests/** : 5 fichiers, ~770 lignes
- **app.py** : 1 fichier, ~300 lignes
- **Total code** : ~2,480 lignes

### Documentation
- **docs/** : 12 fichiers markdown
- **README** : 4 fichiers (racine, docs/, scripts/, guides/)

### Scripts
- **scripts/** : 6 fichiers (3 bash, 3 python)

---

## 🎯 Navigation Rapide

### Pour Démarrer

| Besoin | Fichier |
|--------|---------|
| Démarrage projet | `README.md` |
| Lancer avec Docker | `docs/docker/DOCKER_QUICKSTART.md` |
| Installation locale | `scripts/install.sh` |

### Pour Développer

| Besoin | Fichier |
|--------|---------|
| Scripts Docker | `scripts/docker-dev.sh` |
| Tests | `docs/guides/TESTING.md` |
| Code source | `src/` |
| Tests unitaires | `tests/` |

### Pour Utiliser (Tony)

| Besoin | Fichier |
|--------|---------|
| Template disponibilités | `docs/examples/template-disponibilites.csv` |
| Template récurrents | `docs/examples/template-recurring-slots.csv` |
| Guide remplissage | `docs/examples/README-template.md` |

### Pour Comprendre

| Besoin | Fichier |
|--------|---------|
| Implémentation | `docs/implementation/IMPLEMENTATION_COMPLETE.md` |
| Tech-spec | `_bmad-output/implementation-artifacts/tech-spec-algo-generation-planning.md` |
| Self-check | `docs/implementation/SELF_CHECK_REPORT.md` |

---

## 📂 Organisation par Type

### Markdown (.md)
```
README.md                              (racine)
docs/README.md                         (index docs)
docs/examples/README-*.md              (2 fichiers)
docs/implementation/*.md               (2 fichiers)
docs/docker/*.md                       (3 fichiers)
docs/guides/*.md                       (1 fichier)
scripts/README.md                      (index scripts)
```

### Scripts Bash (.sh)
```
scripts/docker-dev.sh                  (dev Docker)
scripts/install.sh                     (install deps)
```

### Scripts Python de Test (.py - hors src/)
```
scripts/test_models_only.py
scripts/manual_test.py
scripts/test_scheduler_manual.py
```

### Configuration
```
requirements.txt                       (deps Python)
Dockerfile                             (Docker image)
docker-compose.yml                     (Docker orchestration)
.dockerignore                          (Docker exclusions)
.gitignore                             (Git exclusions)
```

---

## 🔄 Changements Appliqués

### ✅ Fichiers Déplacés

**Documentation → `docs/`**
- `IMPLEMENTATION_COMPLETE.md` → `docs/implementation/`
- `SELF_CHECK_REPORT.md` → `docs/implementation/`
- `DOCKER_GUIDE.md` → `docs/docker/`
- `DOCKER_QUICKSTART.md` → `docs/docker/`
- `DOCKER_SETUP_COMPLETE.md` → `docs/docker/`
- `DOCKER_RECAP.txt` → `docs/docker/`
- `TESTING.md` → `docs/guides/`

**Scripts → `scripts/`**
- `docker-dev.sh` → `scripts/`
- `install.sh` → `scripts/`
- `test_models_only.py` → `scripts/`
- `manual_test.py` → `scripts/`
- `test_scheduler_manual.py` → `scripts/`

### ✅ Références Mises à Jour

**Fichiers mis à jour :**
- ✅ `README.md` - Tous les liens vers docs/ et scripts/
- ✅ `Dockerfile` - Chemins scripts
- ✅ `docker-compose.yml` - Volumes et commandes
- ✅ `scripts/docker-dev.sh` - Chemins relatifs
- ✅ `docs/docker/DOCKER_*.md` - Tous les chemins
- ✅ `docs/implementation/IMPLEMENTATION_COMPLETE.md` - Liens

### ✅ README Ajoutés

**Nouveaux fichiers de navigation :**
- ✅ `docs/README.md` - Index de toute la documentation
- ✅ `scripts/README.md` - Index et usage des scripts

---

## 🎨 Principes d'Organisation

### 1. Séparation par Type
- **Code** → `src/`, `tests/`
- **Documentation** → `docs/`
- **Scripts** → `scripts/`
- **Config** → racine

### 2. Hiérarchie Logique
- `docs/` contient sous-dossiers thématiques
- Chaque sous-dossier a un README si nécessaire
- Fichiers racine = point d'entrée ou config

### 3. Nommage Cohérent
- **UPPERCASE.md** = Documentation importante
- **lowercase.py** = Code source
- **lowercase.sh** = Scripts
- **Préfixes** : DOCKER_, test_, etc.

### 4. Navigation Facilitée
- README dans chaque dossier important
- Liens relatifs corrects
- Structure tree visible

---

## 🚀 Commandes Rapides

### Démarrer

```bash
./scripts/docker-dev.sh start
```

### Tester

```bash
./scripts/docker-dev.sh test
```

### Lire la doc

```bash
# Quick start Docker
cat docs/docker/DOCKER_QUICKSTART.md

# Guide complet
cat docs/docker/DOCKER_GUIDE.md

# Tests
cat docs/guides/TESTING.md
```

### Explorer

```bash
# Voir structure
tree -L 2

# Lister docs
ls -la docs/

# Lister scripts
ls -la scripts/
```

---

## 📝 Maintenance

### Ajouter une documentation

1. Choisir le dossier approprié dans `docs/`
2. Créer le fichier `.md`
3. Mettre à jour `docs/README.md`
4. Mettre à jour le README principal si nécessaire

### Ajouter un script

1. Créer dans `scripts/`
2. Rendre exécutable : `chmod +x scripts/nom.sh`
3. Documenter dans `scripts/README.md`
4. Tester

### Refactoring futur

Si le projet grandit :
- `docs/api/` pour documentation API
- `docs/architecture/` pour diagrammes
- `scripts/dev/` et `scripts/deploy/` pour séparer
- `tools/` pour outils externes

---

## ✅ Avantages de cette Structure

✅ **Lisible** - Structure claire et intuitive  
✅ **Navigable** - README dans chaque section  
✅ **Maintenable** - Séparation logique par type  
✅ **Scalable** - Facile d'ajouter de nouveaux éléments  
✅ **Professionnelle** - Standards de l'industrie  
✅ **Git-friendly** - .gitignore bien placés  
✅ **Docker-friendly** - .dockerignore optimisé  

---

**Dernière mise à jour :** 2026-02-02  
**Version :** 1.0 (Structure propre)
