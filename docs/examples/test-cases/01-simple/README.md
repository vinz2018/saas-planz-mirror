# Test Case 01 - Simple

**Niveau :** ⭐ Basique  
**Élèves :** 5  
**Complexité :** Faible

---

## 📋 Caractéristiques

- **5 élèves** avec disponibilités variées
- **1 groupe lié** (Bob & Charlie)
- **2 créneaux récurrents** (squelette simple)

---

## 🎯 Objectif

Valider le fonctionnement de base :
- ✅ Tous les élèves placés
- ✅ Groupe lié respecté
- ✅ Récurrents intégrés

---

## 📊 Résultat Attendu

- ~5 cours générés
- Bob et Charlie toujours ensemble  
- Temps < 2s

---

## 🚀 Test dans Streamlit

```bash
./run-mvp.sh start
```

1. Upload `disponibilites.csv`
2. Upload `recurring-slots.csv`
3. Générer Planning
4. Vérifier 100% placés
