# Test Case 02 - Moyen

**Niveau :** ⭐⭐ Intermédiaire  
**Élèves :** 9  
**Complexité :** Moyenne

---

## 📋 Caractéristiques

- **9 élèves** avec disponibilités variées :
  - 3 paires de groupes liés (6 étudiants)
  - 3 étudiants solo
- **Groupes liés :**
  - Sophie & Julie (débutantes, matins)
  - Marc & Thomas (intermédiaires, après-midis)
  - Laura & Paul (avancés, très flexibles)
- **10 créneaux récurrents** répartis sur 5 jours (lundi à vendredi)
- **1 créneau à capacité max** (3 étudiants : Sophie, Julie, Laura)
- **Mix de `sessions_par_semaine` :** 1, 2, et 3 cours par semaine
- **Horaires variés :** matins (08:00-12:00) et après-midis (14:00-18:00)

---

## 🎯 Objectif

Valider la gestion de complexité moyenne :
- ✅ Groupes liés avec disponibilités communes
- ✅ Mix de fréquences (1-3 cours/semaine)
- ✅ Récurrents variés sur plusieurs jours
- ✅ Étudiants solo à placer de manière optimale
- ✅ Gestion des contraintes de capacité (2-3 étudiants/classe)

---

## 📊 Détails des Étudiants

### Groupes Liés

**Sophie & Julie** (Débutantes) + **Laura** (Avancée)
- 2 cours/semaine chacune (Sophie, Julie), 3 cours/semaine (Laura)
- Disponibles : lundi 09:00-12:00 (tous les trois)
- Récurrent : lundi 09:00-10:00 (3 étudiants - capacité max)

**Marc & Thomas** (Intermédiaires)
- 2 cours/semaine chacun
- Disponibles : mardi à vendredi 14:00-18:00
- Récurrent : mardi 15:00-16:00

**Laura & Paul** (Avancés)
- 3 cours/semaine chacun
- Très flexibles : lundi à mercredi + vendredi matin, samedi
- Récurrents Laura : lundi 09:00-10:00 (avec Sophie & Julie), mercredi 08:00-09:00 (avec Paul)
  - **Note** : Laura a 3 cours/semaine = 2 récurrents (fixes) + 1 cours à générer par l'algorithme
- Récurrent Paul : mercredi 08:00-09:00 (avec Laura)
  - **Note** : Paul a 3 cours/semaine = 1 récurrent (fixe) + 2 cours à générer par l'algorithme

### Étudiants Solo

**Nicolas** (Expert, matins)
- 1 cours/semaine
- Disponible : lundi, mercredi, jeudi, vendredi 10:00-12:00
- Récurrent : vendredi 10:00-11:00

**Isabelle** (Après-midis uniquement)
- 2 cours/semaine
- Disponible : mardi à vendredi 15:00-18:00
- Récurrent : jeudi 16:00-17:00

**Maxime** (Matins tôt)
- 1 cours/semaine
- Disponible : lundi, mardi, mercredi, vendredi 08:00-11:00
- Récurrent : vendredi 09:00-10:00

---

## 📊 Résultat Attendu

- **~15-18 cours générés** (total des sessions_par_semaine = 17)
- **Tous les groupes liés respectés** (paires toujours ensemble)
- **10 créneaux récurrents** intégrés au squelette (dont 1 à capacité max)
- **Optimisation des créneaux** pour placer les étudiants solo
- **Temps d'exécution :** < 5s

### Métriques Attendues

- Taux de placement : **100%** (tous les étudiants placés)
- Créneaux récurrents : **100%** (tous utilisés)
- Groupes liés : **100%** (toujours ensemble)

---

## 🚀 Test dans Streamlit

```bash
./run-mvp.sh start
```

1. Upload `disponibilites.csv` (9 étudiants)
2. Upload `recurring-slots.csv` (10 créneaux)
3. Cliquer sur "Générer Planning"
4. Vérifier :
   - ✅ 100% des étudiants placés
   - ✅ Groupes liés respectés
   - ✅ Créneaux récurrents intégrés
   - ✅ Pas de chevauchement de cours (UN SEUL COURS À LA FOIS)
   - ⚠️ **Warnings attendus** : 2 créneaux à 1 étudiant (Nicolas vendredi 10:00, Maxime vendredi 09:00)
     - Status `NEEDS_VALIDATION` pour ces créneaux
     - Suggestions d'étudiants compatibles affichées

---

## 🔍 Validation des Fichiers

Avant de tester dans Streamlit, valider les CSV :

```bash
python scripts/validate_test_csv.py docs/examples/test-cases/02-moyen/
```

---

## ⚙️ Logique Créneaux Récurrents vs Sessions Par Semaine

**Principe :**  
Les créneaux récurrents (squelette) comptent dans le total `sessions_par_semaine`. L'algorithme doit ensuite placer les sessions restantes.

**Exemples dans ce test case :**

| Étudiant | sessions_par_semaine | Récurrents (fixes) | À générer par algo | Total |
|----------|---------------------|-------------------|-------------------|-------|
| Sophie | 2 | 1 (lundi 09:00) | 1 | 2 ✅ |
| Julie | 2 | 1 (lundi 09:00) | 1 | 2 ✅ |
| Marc | 2 | 1 (mardi 15:00) | 1 | 2 ✅ |
| Thomas | 2 | 1 (mardi 15:00) | 1 | 2 ✅ |
| Laura | 3 | 2 (lundi 09:00, mercredi 08:00) | 1 | 3 ✅ |
| Paul | 3 | 1 (mercredi 08:00) | 2 | 3 ✅ |
| Nicolas | 1 | 1 (vendredi 10:00) | 0 | 1 ✅ |
| Isabelle | 2 | 1 (jeudi 16:00) | 1 | 2 ✅ |
| Maxime | 1 | 1 (vendredi 09:00) | 0 | 1 ✅ |

**Total :** 17 sessions (10 récurrents + 7 à générer)

---

## 🐛 Points de Vigilance

- **Laura & Paul** : 3 cours/semaine chacun → vérifier que tous sont placés
- **Groupes liés** : doivent avoir des disponibilités communes
- **Étudiants solo** : peuvent nécessiter la formation de nouveaux groupes
- **Créneaux variés** : différents jours et heures pour tester la flexibilité

---

## 📝 Notes

Ce test case valide :
- La gestion de groupes liés multiples
- La mixité de fréquences (1-3 cours/semaine)
- L'optimisation pour compléter les créneaux avec des étudiants solo
- La répartition sur toute la semaine (lundi-vendredi)
- La capacité maximale (3 étudiants par créneau)
- Les warnings pour créneaux à 1 étudiant

**Edge Cases Non Couverts :**  
Pour les cas limites non testés ici (groupes incompatibles, disponibilités insuffisantes, etc.), voir [`EDGE_CASES_TODO.md`](../EDGE_CASES_TODO.md)
