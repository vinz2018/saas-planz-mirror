# Test Case 03 - Complexe

**Niveau :** ⭐⭐⭐ Avancé  
**Élèves :** 14  
**Complexité :** Élevée

---

## 📋 Caractéristiques

- **14 étudiants** avec disponibilités complexes :
  - 5 paires de groupes liés (10 étudiants)
  - 4 étudiants solo
- **Groupes liés :**
  - Camille & Léa (avancées, très flexibles, 6 jours/7)
  - Antoine & Lucas (intermédiaires, après-midis)
  - Marie & Pierre (débutants, matins semaine)
  - Océane & Hugo (experts, toute disponibilité)
  - Chloé & Thomas (flexibles, horaires variés)
- **18 créneaux récurrents** répartis sur **6 jours** (lundi à samedi)
- **6 créneaux à capacité max** (3 étudiants)
- **Mix de `sessions_par_semaine` :** 1, 2, et 3 cours par semaine
- **Horaires variés avec :30** : 08:30, 09:30, 15:30, 16:00, etc.
- **Créneaux samedi** : 3 créneaux testant la gestion du week-end

---

## 🎯 Objectif

Valider la gestion de complexité élevée et edge cases :
- ✅ Montée en charge (14 étudiants, 18 récurrents)
- ✅ Créneaux à :30 minutes (EC6)
- ✅ Gestion du samedi (EC5)
- ✅ Multiples créneaux à capacité max (3 étudiants)
- ✅ Mix de tous les jours de la semaine
- ✅ Horaires variés et chevauchements complexes

---

## 📊 Détails des Étudiants

### Groupes Liés

**Camille & Léa** (Avancées, très flexibles)
- 3 cours/semaine chacune
- Disponibles 6 jours/7 : lundi à vendredi (08:30-13:00), samedi (09:00-12:00)
- Récurrents : lundi 08:30-09:30 (avec Océane - capacité max), samedi 10:00-11:00 (avec Raphaël - capacité max)
- **Note** : 3 cours = 2 récurrents + 1 à générer

**Antoine & Lucas** (Intermédiaires, après-midis)
- 2 cours/semaine chacun
- Disponibles : mardi à vendredi 14:00-18:00
- Récurrent : mardi 15:00-16:00 (avec Julien - capacité max)
- **Note** : 2 cours = 1 récurrent + 1 à générer

**Marie & Pierre** (Débutants, matins semaine)
- 2 cours/semaine chacun
- Disponibles : lundi, mardi, jeudi, vendredi 09:00-12:30
- Récurrent : mercredi 09:00-10:00 (avec Hugo - capacité max)
- **Note** : 2 cours = 1 récurrent + 1 à générer

**Océane & Hugo** (Experts, toute disponibilité)
- 3 cours/semaine chacun
- Très flexibles : lundi à samedi, 08:00-13:00
- Récurrents : lundi 08:30-09:30 (avec Camille & Léa), mercredi 09:00-10:00 (avec Marie & Pierre), vendredi 09:30-10:30 (avec Zoé)
- **Note Océane** : 3 cours = 3 récurrents + 0 à générer
- **Note Hugo** : 3 cours = 2 récurrents + 1 à générer

**Chloé & Thomas** (Flexibles, horaires variés)
- 2 cours/semaine chacun
- Disponibles : mardi à vendredi 15:30-18:30, samedi 10:00-13:00
- Récurrent : jeudi 16:00-17:00 (avec Manon - capacité max)
- **Note** : 2 cours = 1 récurrent + 1 à générer

### Étudiants Solo

**Julien** (Solo, milieux de matinée)
- 1 cours/semaine
- Disponible : lundi à vendredi 10:00-12:00
- Récurrent : mardi 15:00-16:00 (avec Antoine & Lucas - capacité max)
- **Note** : 1 cours = 1 récurrent + 0 à générer

**Manon** (Solo, après-midi + samedi matin)
- 2 cours/semaine
- Disponible : mardi à vendredi 14:30-18:00, samedi 09:30-12:30
- Récurrent : jeudi 16:00-17:00 (avec Chloé & Thomas - capacité max)
- **Note** : 2 cours = 1 récurrent + 1 à générer

**Raphaël** (Solo, débuts de matinée)
- 1 cours/semaine
- Disponible : lundi, mardi, mercredi, vendredi 08:00-10:30
- Récurrent : samedi 10:00-11:00 (avec Camille & Léa - capacité max)
- **Note** : 1 cours = 1 récurrent + 0 à générer

**Zoé** (Solo, très régulière)
- 3 cours/semaine
- Très régulière : lundi à samedi 09:30-13:00 (ou 12:30 samedi)
- Récurrent : vendredi 09:30-10:30 (avec Océane & Hugo - capacité max)
- **Note** : 3 cours = 1 récurrent + 2 à générer

---

## 📊 Résultat Attendu

- **~30-33 cours générés** (total des sessions_par_semaine = 31)
- **Tous les groupes liés respectés** (5 paires toujours ensemble)
- **18 créneaux récurrents** intégrés au squelette
- **6 créneaux à capacité max** (3 étudiants chacun)
- **Créneaux à :30** validés (08:30, 09:30, 15:30, etc.)
- **Créneaux samedi** validés (3 créneaux)
- **Temps d'exécution :** < 10s

### Métriques Attendues

- Taux de placement : **~100%** (tous les étudiants placés)
- Créneaux récurrents : **100%** (tous utilisés)
- Groupes liés : **100%** (toujours ensemble)
- Créneaux à capacité max : **6** (validation du comportement)

---

## 🚀 Test dans Streamlit

```bash
./run-mvp.sh start
```

1. Upload `disponibilites.csv` (14 étudiants)
2. Upload `recurring-slots.csv` (18 créneaux)
3. Cliquer sur "Générer Planning"
4. Vérifier :
   - ✅ ~100% des étudiants placés
   - ✅ Groupes liés respectés (5 paires)
   - ✅ Créneaux récurrents intégrés (18)
   - ✅ Créneaux à capacité max (6 avec 3 étudiants)
   - ✅ Créneaux à :30 minutes fonctionnent
   - ✅ Créneaux samedi bien placés
   - ✅ Pas de chevauchement de cours (UN SEUL COURS À LA FOIS)

---

## 🔍 Validation des Fichiers

Avant de tester dans Streamlit, valider les CSV :

```bash
python scripts/validate_test_csv.py docs/examples/test-cases/03-complexe/
```

---

## ⚙️ Logique Créneaux Récurrents vs Sessions Par Semaine

**Principe :**  
Les créneaux récurrents (squelette) comptent dans le total `sessions_par_semaine`. L'algorithme doit ensuite placer les sessions restantes.

**Exemples dans ce test case :**

| Étudiant | sessions_par_semaine | Récurrents (fixes) | À générer par algo | Total |
|----------|---------------------|-------------------|-------------------|-------|
| Camille | 3 | 2 (lundi 08:30, samedi 10:00) | 1 | 3 ✅ |
| Léa | 3 | 2 (lundi 08:30, samedi 10:00) | 1 | 3 ✅ |
| Antoine | 2 | 1 (mardi 15:00) | 1 | 2 ✅ |
| Lucas | 2 | 1 (mardi 15:00) | 1 | 2 ✅ |
| Marie | 2 | 1 (mercredi 09:00) | 1 | 2 ✅ |
| Pierre | 2 | 1 (mercredi 09:00) | 1 | 2 ✅ |
| Océane | 3 | 3 (lundi 08:30, mercredi 09:00, vendredi 09:30) | 0 | 3 ✅ |
| Hugo | 3 | 2 (mercredi 09:00, vendredi 09:30) | 1 | 3 ✅ |
| Chloé | 2 | 1 (jeudi 16:00) | 1 | 2 ✅ |
| Thomas | 2 | 1 (jeudi 16:00) | 1 | 2 ✅ |
| Julien | 1 | 1 (mardi 15:00) | 0 | 1 ✅ |
| Manon | 2 | 1 (jeudi 16:00) | 1 | 2 ✅ |
| Raphaël | 1 | 1 (samedi 10:00) | 0 | 1 ✅ |
| Zoé | 3 | 1 (vendredi 09:30) | 2 | 3 ✅ |

**Total :** 31 sessions (18 récurrents + 13 à générer)

---

## 🐛 Points de Vigilance

- **Océane** : 3 cours/semaine avec 3 récurrents → déjà complète, rien à générer
- **Créneaux à capacité max** : 6 créneaux avec 3 étudiants chacun
- **Créneaux à :30** : 08:30, 09:30, 15:30 → valider le bon fonctionnement
- **Créneaux samedi** : 3 créneaux différents (10:00, pas d'autres)
- **Groupes liés multiples** : 5 paires à gérer simultanément
- **Étudiants solo** : doivent être intégrés dans les créneaux optimaux

---

## 📝 Notes

Ce test case valide :
- ✅ La montée en charge (14 étudiants, 31 sessions)
- ✅ Les créneaux à :30 minutes (EC6)
- ✅ La gestion du samedi (EC5)
- ✅ Les créneaux à capacité maximale (EC4)
- ✅ La complexité de 5 groupes liés simultanés
- ✅ L'optimisation pour placer 13 cours supplémentaires via l'algorithme
- ✅ La répartition sur 6 jours (lundi-samedi)

**Edge Cases Couverts :**
- EC4 : Capacité Maximum (6 créneaux à 3 étudiants)
- EC5 : Créneaux Samedi (3 créneaux)
- EC6 : Créneaux à :30 (multiples créneaux)

**Edge Cases Non Couverts :**  
Pour les cas limites restants (groupes incompatibles, disponibilités insuffisantes, etc.), voir [`../EDGE_CASES_TODO.md`](../EDGE_CASES_TODO.md)
