# 📊 Status des Cas de Test

**Créé le :** 2026-02-02  
**Emplacement :** `docs/examples/test-cases/`

---

## ✅ Fichiers Créés

### 01-simple (Prêt à tester ✅)
```
01-simple/
├── disponibilites.csv        ✅ 5 élèves
├── recurring-slots.csv        ✅ 2 récurrents
└── README.md                  ✅ Documentation
```

**Status :** ✅ **COMPLET ET FONCTIONNEL**

### Documentation
```
├── README.md                  ✅ Index des cas de test
├── QUICKSTART.md              ✅ Guide rapide
└── STATUS.md                  ✅ Ce fichier
```

---

## 📝 Cas à Créer (Si Besoin)

Les cas suivants peuvent être créés si tu veux tester des scénarios plus complexes :

### 02-moyen
- 13 élèves
- 2 groupes liés
- 5 récurrents
- Contraintes horaires variées

### 03-complexe
- 25 élèves
- 4 groupes liés
- 12 récurrents
- Créneaux très serrés

### 04-tres-complexe
- 39 élèves
- 7 groupes liés  
- 27 récurrents
- Nombreux cas edge
- ✅ README déjà créé

### 05-extreme
- 50 élèves (cas réel de Tony)
- 10 groupes liés
- 35 récurrents
- Tous les cas edge

---

## 🚀 Comment Tester Maintenant

### Option 1 : Test Rapide (Recommandé)

Utilise **01-simple** qui est complet et fonctionnel :

```bash
# 1. Lancer Streamlit
./run-mvp.sh start

# 2. Ouvrir navigateur
open http://localhost:8501

# 3. Dans Streamlit :
# - Upload: docs/examples/test-cases/01-simple/disponibilites.csv
# - Upload: docs/examples/test-cases/01-simple/recurring-slots.csv
# - Cliquer "Générer Planning"
# - Vérifier : 5 élèves placés, ~5 cours générés
```

**Résultat attendu :**
- ✅ 5/5 élèves placés
- ✅ Bob & Charlie toujours ensemble
- ✅ 2 récurrents intégrés
- ✅ Temps < 2s
- ✅ Aucun overlap

---

### Option 2 : Créer Plus de Cas

Si tu veux tester des scénarios plus complexes, dis-moi lequel tu veux et je le crée :

**Exemples de demandes :**
- "Crée-moi le cas 02-moyen pour tester avec 13 élèves"
- "Je veux tester avec 50 élèves, crée le cas 05-extreme"
- "Crée-moi tous les cas manquants"

---

## 📂 Structure Actuelle

```
docs/examples/test-cases/
├── README.md                    ✅ Index
├── QUICKSTART.md                ✅ Guide rapide
├── STATUS.md                    ✅ Ce fichier
│
├── 01-simple/                   ✅ COMPLET
│   ├── disponibilites.csv
│   ├── recurring-slots.csv
│   └── README.md
│
├── 02-moyen/                    📝 À créer
├── 03-complexe/                 📝 À créer
│
├── 04-tres-complexe/            📝 Partiel (README only)
│   └── README.md
│
└── 05-extreme/                  📝 À créer
```

---

## 💡 Recommandation

**Pour tester maintenant :** Utilise `01-simple` qui est complet et suffit pour valider que l'app fonctionne.

**Pour plus tard :** Si tu veux des tests plus poussés, dis-moi quels cas créer et je les génère.

---

## ✅ Action Immédiate

```bash
./run-mvp.sh start
```

Puis teste avec `01-simple` ! 🚀
