# MVP Streamlit - SaaS Planz

Interface Streamlit pour le MVP de SaaS Planz - Phase exploratoire.

---

## 🎯 Objectif

Prototype fonctionnel pour Tony permettant de :
- Upload CSVs disponibilités élèves
- Bloquer ses créneaux personnels
- Générer planning automatique avec OR-Tools
- Télécharger résultats (JSON + Markdown)

---

## 🚀 Lancer l'Application

### Avec Docker (Recommandé)

```bash
# Depuis la racine du projet
cd apps/mvp-streamlit
docker compose up -d

# Ouvrir http://localhost:8501
```

### Sans Docker

```bash
# Depuis la racine du projet
python3 -m venv venv
source venv/bin/activate
pip install -r apps/mvp-streamlit/requirements.txt

# Lancer
cd apps/mvp-streamlit
streamlit run app.py
```

---

## 📁 Structure

```
mvp-streamlit/
├── app.py                    # Application Streamlit
├── Dockerfile                # Image Docker
├── docker-compose.yml        # Orchestration
├── requirements.txt          # Dépendances
└── README.md                 # Ce fichier
```

---

## 🔧 Dépendances

**Core (logique métier) :**
- `core/models.py` - Dataclasses
- `core/parser.py` - Parsing CSV
- `core/scheduler.py` - OR-Tools algo
- `core/formatter.py` - Export JSON/Markdown

**MVP Streamlit :**
- `streamlit` - Interface web
- `pandas` - Manipulation CSV
- `ortools` - Optimisation

---

## 🧪 Tests

```bash
# Tests du core (depuis racine)
pytest tests/

# Tests manuels
python3 scripts/test_models_only.py
```

---

## 📚 Documentation

- **Guide utilisateur** : `../../docs/examples/README-template.md`
- **Guide Docker** : `../../docs/docker/DOCKER_QUICKSTART.md`
- **Tests** : `../../docs/guides/TESTING.md`

---

## 🎨 Features

✅ Upload CSV disponibilités  
✅ Upload CSV créneaux récurrents  
✅ Blocage créneaux coach  
✅ Génération planning (OR-Tools)  
✅ Affichage visuel par jour  
✅ Download JSON + Markdown  
✅ Gestion erreurs avec messages clairs  

---

## 🔄 Hot-Reload

Avec Docker Compose, les changements dans `app.py` et `core/` sont détectés automatiquement :

1. Modifier le code
2. Sauvegarder
3. Refresh navigateur
4. ✅ Changement appliqué

---

## 🚧 Limitations MVP

- Session-only (pas de persistance)
- Coach reserved slots perdus au restart
- Pas d'ajustements manuels drag-and-drop
- Pas de notifications élèves
- Monoposte (pas multi-tenant)

---

## 🎯 Prochaines Phases

Après validation du MVP, prochaines itérations :

- **Phase 2** : Web app (Next.js + FastAPI)
- **Phase 3** : Multi-tenant SaaS
- **Phase 4** : Mobile app
- **Phase 5** : WhatsApp integration

---

**Status :** ✅ MVP Fonctionnel  
**Version :** 0.1.0 (Phase exploratoire)  
**Tech Stack :** Python 3.11 + Streamlit + OR-Tools
