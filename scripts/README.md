# 🔧 Scripts Helper

Scripts utilitaires pour le développement et les tests de SaaS Planz.

---

## 📋 Scripts Disponibles

### 🐳 Docker Development

**`docker-dev.sh`** - Script principal pour gérer l'environnement Docker

```bash
# Gestion application
./scripts/docker-dev.sh start       # Démarrer l'app
./scripts/docker-dev.sh stop        # Arrêter l'app
./scripts/docker-dev.sh restart     # Redémarrer
./scripts/docker-dev.sh logs        # Voir logs (live)
./scripts/docker-dev.sh status      # Status containers

# Tests
./scripts/docker-dev.sh test           # Tous tests
./scripts/docker-dev.sh test-models    # Tests rapides
./scripts/docker-dev.sh test-parser    # Tests parser

# Debug
./scripts/docker-dev.sh shell       # Shell dans container
./scripts/docker-dev.sh rebuild     # Rebuild complet
./scripts/docker-dev.sh clean       # Nettoyer tout
```

**Documentation :** Voir `../docs/docker/DOCKER_GUIDE.md`

---

### 📦 Installation

**`install.sh`** - Installation des dépendances Python (sans Docker)

```bash
bash scripts/install.sh
```

Installe :
- pandas
- ortools
- streamlit
- pytest
- pytest-cov

---

### 🧪 Tests Manuels

#### `test_models_only.py`

Tests des modèles sans dépendances externes (pandas, ortools).

```bash
python3 scripts/test_models_only.py
```

**Teste :**
- Validation Slot (durée, granularité, overlap)
- Student availability
- Linked groups
- ScheduledClass capacity
- Explications human-readable

**Status :** ✅ VALIDÉ (20+ assertions passed)

---

#### `manual_test.py`

Tests du parser avec pandas (nécessite pandas installé).

```bash
python3 scripts/manual_test.py
```

**Teste :**
- Parsing temps (HH:00, HH:30)
- Expansion plages horaires
- Validation linked groups
- Parsing CSV complet
- Parsing recurring slots

**Prérequis :** `pip install pandas`

---

#### `test_scheduler_manual.py`

Tests du skeleton scheduler sans OR-Tools.

```bash
python3 scripts/test_scheduler_manual.py
```

**Teste :**
- Validation skeleton
- Détection overlaps (UN SEUL COURS À LA FOIS)
- Validation capacité (2-3 étudiants)
- Coach reserved slots conflicts

**Prérequis :** Aucun (teste uniquement la validation)

---

## 🎯 Utilisation Recommandée

### Développement Local (sans Docker)

```bash
# 1. Installer dépendances
bash scripts/install.sh

# 2. Tester modèles
python3 scripts/test_models_only.py

# 3. Tester parser
python3 scripts/manual_test.py

# 4. Lancer app
streamlit run app.py
```

### Développement avec Docker (recommandé)

```bash
# Tout est géré par docker-dev.sh
./scripts/docker-dev.sh start
./scripts/docker-dev.sh test-models
./scripts/docker-dev.sh logs
```

---

## 📚 Documentation

- **Guide Docker** : `../docs/docker/DOCKER_GUIDE.md`
- **Guide Tests** : `../docs/guides/TESTING.md`
- **README principal** : `../README.md`

---

## ⚙️ Maintenance

### Ajouter un nouveau script

1. Créer le script dans `scripts/`
2. Rendre exécutable : `chmod +x scripts/nom_script.sh`
3. Documenter dans ce README
4. Mettre à jour `.dockerignore` si nécessaire

### Conventions

- Scripts bash : `*.sh`
- Scripts Python : `*.py`
- Tous les scripts doivent avoir un header avec description
- Utiliser des noms descriptifs

---

**Questions ?** → Voir `../docs/docker/DOCKER_GUIDE.md` section "Troubleshooting"
