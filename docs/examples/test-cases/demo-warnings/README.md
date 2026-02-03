# Test Case Demo - Warnings pour Créneaux à 1 Étudiant

**Objectif :** Démontrer le système de warnings pour les créneaux récurrents avec 1 seul étudiant.

## 📋 Caractéristiques

- **5 étudiants** :
  - Alice & Bob (groupe lié, 2 cours/semaine chacun)
  - Charlie (solo, 1 cours/semaine)
  - David (solo, 2 cours/semaine)
  - Emma (solo, 1 cours/semaine)

- **4 créneaux récurrents** :
  - lundi 09:00-10:00 : Alice, Bob (✅ 2 étudiants - OK)
  - mardi 10:00-11:00 : Charlie (⚠️ 1 étudiant - WARNING)
  - mercredi 08:00-09:00 : Emma (⚠️ 1 étudiant - WARNING)

## 🎯 Résultat Attendu

**Dans Streamlit :**
1. ✅ Le planning est généré avec succès (pas d'erreur)
2. ⚠️ Section "Avertissements et Optimisations Possibles" visible
3. ⚠️ 2 warnings affichés :
   - Warning 1 : Créneau mardi 10:00-11:00 (Charlie seul)
   - Warning 2 : Créneau mercredi 08:00-09:00 (Emma seule)
4. 💡 Suggestions affichées pour chaque warning :
   - Pour Charlie : David disponible sur ce créneau
   - Pour Emma : Aucun autre étudiant disponible

## 🚀 Test dans Streamlit

```bash
./run-mvp.sh start
```

1. Upload `disponibilites.csv`
2. Upload `recurring-slots.csv`
3. Cliquer sur "Générer Planning"
4. Vérifier la section "⚠️ Avertissements et Optimisations Possibles"
5. Développer les expanders pour voir les suggestions

## ✅ Validation

- ✅ Pas d'erreur (créneaux à 1 étudiant acceptés)
- ✅ Status `NEEDS_VALIDATION` appliqué aux créneaux problématiques
- ✅ Warnings générés automatiquement
- ✅ Suggestions pertinentes basées sur les disponibilités
- ✅ Interface utilisateur claire avec expanders

---

**Note :** Ce test case démontre que le système accepte les créneaux récurrents à 1 étudiant tout en alertant l'utilisateur et en proposant des optimisations.
