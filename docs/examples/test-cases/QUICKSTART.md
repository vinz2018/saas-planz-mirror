# 🚀 Quick Start - Tester les Cas

Guide rapide pour tester l'application Streamlit avec les cas de test.

---

## ⚡ Test en 3 Minutes

### 1. Lancer Streamlit
```bash
cd /home/vincent/saas-planz
./run-mvp.sh start
```

### 2. Ouvrir dans le navigateur
```
http://localhost:8501
```

### 3. Tester avec 01-simple
1. **Upload disponibilités**
   - Cliquer sur "Browse files"
   - Sélectionner `docs/examples/test-cases/01-simple/disponibilites.csv`

2. **Upload récurrents**
   - Cliquer sur "Browse files"  
   - Sélectionner `docs/examples/test-cases/01-simple/recurring-slots.csv`

3. **Générer**
   - Cliquer sur "Générer Planning"
   - Attendre ~2 secondes

4. **Vérifier**
   - ✅ 5 élèves placés
   - ✅ Bob & Charlie toujours ensemble
   - ✅ ~5 cours générés
   - ✅ Aucun overlap

---

## 📂 Fichiers Disponibles

**✅ Déjà créés :**
- `01-simple/disponibilites.csv` (5 élèves)
- `01-simple/recurring-slots.csv` (2 récurrents)
- `README.md` (index)
- `QUICKSTART.md` (ce fichier)

**📝 À créer (si besoin) :**
Les autres cas de test (02 à 05) peuvent être créés manuellement ou avec le script :
```bash
python3 scripts/generate_test_cases.py
```

---

## 🎯 Test Minimal Fonctionnel

Le cas **01-simple** suffit pour valider que l'application fonctionne :
- Upload de CSV
- Parsing correct
- Génération de planning
- Respect des contraintes (groupes liés, capacité, durée)
- Affichage des résultats
- Download JSON/Markdown

---

## 📊 Résultat Attendu (01-simple)

**Planning généré :**
```
LUNDI
  08:00-09:00 : Alice, Emma [Récurrent]

MARDI  
  15:00-16:00 : Bob, Charlie [Récurrent]

MERCREDI
  09:00-10:00 : Alice, Emma
  14:00-15:00 : Bob, Charlie

VENDREDI
  08:00-09:00 : David, (1-2 autres)

SAMEDI
  09:00-10:00 : David, (1-2 autres)
```

**Statistiques :**
- 5/5 élèves placés (100%)
- ~5-6 cours générés
- 1 groupe lié respecté (Bob & Charlie)
- 2 récurrents intégrés

---

## 🐛 Si Problème

### Erreur de parsing
- Vérifier que les CSV sont bien formatés
- Vérifier les virgules et guillemets

### Aucun planning généré
- Vérifier les logs Streamlit
- Vérifier que les disponibilités sont valides

### Élèves non placés
- Normal si contraintes impossibles
- Vérifier les explications dans "Élèves non placés"

---

**Prêt !** Lance `./run-mvp.sh start` et teste avec `01-simple`.
