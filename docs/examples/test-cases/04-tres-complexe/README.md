# Test Case 04 - Très Complexe

**Niveau :** ⭐⭐⭐⭐ Expert  
**Élèves :** 22  
**Complexité :** Très élevée

---

## 📋 Caractéristiques

- **22 étudiants** avec disponibilités complexes :
  - 7 paires de groupes liés (14 étudiants)
  - 8 étudiants solo
- **39 créneaux récurrents individuels** formant **13 classes** :
  - **TOUS les 13 créneaux sont à capacité maximale** (3 étudiants chacun)
- **Mix de `sessions_par_semaine` :** 1, 2, 3, et 4 cours par semaine
- **Horaires variés avec :00 et :30** : 08:00, 08:30, 09:00, 09:30, 10:00, etc.
- **Créneaux sur 6 jours** (lundi à samedi)
- **Total : 57 sessions** à générer (39 récurrents + 18 à générer par l'algorithme)

---

## 🎯 Objectif

Valider la gestion de très haute complexité et montée en charge :
- ✅ Montée en charge extrême (22 étudiants, 39 récurrents, 57 sessions totales)
- ✅ Tous les créneaux récurrents à capacité max (13 créneaux × 3 étudiants)
- ✅ 7 groupes liés à gérer simultanément
- ✅ Mix de toutes les valeurs de sessions_par_semaine (1-4)
- ✅ Créneaux à :00 et :30 mélangés
- ✅ Répartition sur 6 jours
- ✅ Optimisation pour placer 18 sessions supplémentaires

---

## 📊 Détails des Étudiants

### Groupes Liés

**Sofia & Lucas** (Experts très disponibles)
- 4 cours/semaine chacun
- Disponibles 6 jours/7 : lundi à vendredi (08:00-13:00), samedi (08:00-12:00)
- Récurrents : lundi 08:30, mardi 09:00, jeudi 08:00, samedi 11:00 (4 créneaux = complet)
- **Note** : 4 cours = 4 récurrents + 0 à générer

**Emma & Noah** (Avancés matins)
- 3 cours/semaine chacun
- Disponibles 6 jours/7 : lundi à vendredi (08:30-12:30), samedi (09:00-12:00)
- Récurrents : lundi 09:30, vendredi 10:00 (2 créneaux)
- **Note** : 3 cours = 2 récurrents + 1 à générer

**Léo & Alice** (Intermédiaires après-midi)
- 3 cours/semaine chacun
- Disponibles : mardi à vendredi (14:00-18:30), samedi (10:00-13:00)
- Récurrents : mardi 15:00, jeudi 16:00 (2 créneaux)
- **Note** : 3 cours = 2 récurrents + 1 à générer

**Gabriel & Inès** (Débutants semaine matins)
- 2 cours/semaine chacun
- Disponibles : lundi à vendredi (09:00-12:00)
- Récurrent : mercredi 09:00 (1 créneau)
- **Note** : 2 cours = 1 récurrent + 1 à générer

**Louis & Chloé** (Experts flexibilité max)
- 3 cours/semaine chacun
- Très flexibles : lundi à samedi (08:00-13:00)
- Récurrents : lundi 11:00, jeudi 08:00 (2 créneaux)
- **Note** : 3 cours = 2 récurrents + 1 à générer

**Arthur & Jade** (Flexibles après-midi)
- 2 cours/semaine chacun
- Disponibles : mardi à vendredi (15:00-18:00), samedi (09:30-12:30)
- Récurrent : vendredi 16:00 (1 créneau)
- **Note** : 2 cours = 1 récurrent + 1 à générer

**Raphaël & Zoé** (Réguliers milieu matinée)
- 3 cours/semaine chacun
- Disponibles 6 jours/7 : lundi à samedi (09:30-13:00 ou 12:30)
- Récurrents : mercredi 10:30, samedi 10:00 (2 créneaux)
- **Note** : 3 cours = 2 récurrents + 1 à générer

### Étudiants Solo

**Maxime** (Solo ultra-flexible)
- 4 cours/semaine
- Ultra-flexible : lundi à samedi (08:00-18:00 ou 13:00 samedi)
- Récurrents : lundi 08:30, mercredi 10:30, samedi 11:00 (3 créneaux)
- **Note** : 4 cours = 3 récurrents + 1 à générer

**Camille** (Solo fin matinée)
- 3 cours/semaine
- Disponible 6 jours/7 : lundi à samedi (10:00-13:00 ou 12:00)
- Récurrents : lundi 11:00, vendredi 10:00 (2 créneaux)
- **Note** : 3 cours = 2 récurrents + 1 à générer

**Hugo** (Solo après-midi)
- 2 cours/semaine
- Disponible : mardi à vendredi (14:30-18:00), samedi (10:30-13:00)
- Récurrents : mardi 15:00, vendredi 16:00 (2 créneaux)
- **Note** : 2 cours = 2 récurrents + 0 à générer

**Manon** (Solo début matinée)
- 1 cours/semaine
- Disponible : lundi à vendredi (08:00-10:00)
- Récurrent : mercredi 09:00 (1 créneau)
- **Note** : 1 cours = 1 récurrent + 0 à générer

**Théo** (Solo matins variés)
- 3 cours/semaine
- Disponible 6 jours/7 : lundi à samedi (08:30-12:00)
- Récurrent : lundi 09:30 (1 créneau)
- **Note** : 3 cours = 1 récurrent + 2 à générer

**Lina** (Solo fin après-midi)
- 2 cours/semaine
- Disponible : mardi à vendredi (15:30-18:30)
- Récurrent : jeudi 16:00 (1 créneau)
- **Note** : 2 cours = 1 récurrent + 1 à générer

**Élise** (Solo très régulière)
- 4 cours/semaine
- Disponible 6 jours/7 : lundi à samedi (09:00-13:00 ou 12:00)
- Récurrents : mardi 09:00, samedi 10:00 (2 créneaux)
- **Note** : 4 cours = 2 récurrents + 2 à générer

**Tom** (Solo milieu matinée)
- 1 cours/semaine
- Disponible : lundi à vendredi (10:30-12:30)
- Récurrents : Aucun
- **Note** : 1 cours = 0 récurrent + 1 à générer

---

## 📊 Résultat Attendu

- **~57 cours générés** (total des sessions_par_semaine)
- **Tous les groupes liés respectés** (7 paires toujours ensemble)
- **39 créneaux récurrents individuels** intégrés au squelette (13 classes à capacité max)
- **13 créneaux à capacité maximale** (3 étudiants chacun)
- **18 sessions supplémentaires** à générer par l'algorithme
- **Temps d'exécution :** < 15s

### Métriques Attendues

- Taux de placement : **~100%** (tous les étudiants placés)
- Créneaux récurrents : **100%** (tous utilisés)
- Groupes liés : **100%** (toujours ensemble)
- Créneaux à capacité max : **13** (validation maximale)

---

## 🚀 Test dans Streamlit

```bash
./run-mvp.sh start
```

1. Upload `disponibilites.csv` (22 étudiants)
2. Upload `recurring-slots.csv` (39 slots = 13 classes)
3. Cliquer sur "Générer Planning"
4. Vérifier :
   - ✅ ~100% des étudiants placés
   - ✅ Groupes liés respectés (7 paires)
   - ✅ Créneaux récurrents intégrés (13 classes, tous à 3 étudiants)
   - ✅ Créneaux à :00 et :30 fonctionnent
   - ✅ Créneaux samedi bien placés
   - ✅ Pas de chevauchement de cours (UN SEUL COURS À LA FOIS)
   - ✅ Temps d'exécution raisonnable (< 15s)

---

## 🔍 Validation des Fichiers

Avant de tester dans Streamlit, valider les CSV :

```bash
python scripts/validate_test_csv.py docs/examples/test-cases/04-tres-complexe/
```

---

## ⚙️ Logique Créneaux Récurrents vs Sessions Par Semaine

**Principe :**  
Les créneaux récurrents (squelette) comptent dans le total `sessions_par_semaine`. L'algorithme doit ensuite placer les sessions restantes.

**Exemples dans ce test case :**

| Étudiant | sessions_par_semaine | Récurrents (fixes) | À générer par algo | Total |
|----------|---------------------|-------------------|-------------------|-------|
| Sofia | 4 | 4 (lun 08:30, mar 09:00, jeu 08:00, sam 11:00) | 0 | 4 ✅ |
| Lucas | 4 | 4 (lun 08:30, mar 09:00, jeu 08:00, sam 11:00) | 0 | 4 ✅ |
| Emma | 3 | 2 (lun 09:30, ven 10:00) | 1 | 3 ✅ |
| Noah | 3 | 2 (lun 09:30, ven 10:00) | 1 | 3 ✅ |
| Léo | 3 | 2 (mar 15:00, jeu 16:00) | 1 | 3 ✅ |
| Alice | 3 | 2 (mar 15:00, jeu 16:00) | 1 | 3 ✅ |
| Gabriel | 2 | 1 (mer 09:00) | 1 | 2 ✅ |
| Inès | 2 | 1 (mer 09:00) | 1 | 2 ✅ |
| Louis | 3 | 2 (lun 11:00, jeu 08:00) | 1 | 3 ✅ |
| Chloé | 3 | 2 (lun 11:00, jeu 08:00) | 1 | 3 ✅ |
| Arthur | 2 | 1 (ven 16:00) | 1 | 2 ✅ |
| Jade | 2 | 1 (ven 16:00) | 1 | 2 ✅ |
| Raphaël | 3 | 2 (mer 10:30, sam 10:00) | 1 | 3 ✅ |
| Zoé | 3 | 2 (mer 10:30, sam 10:00) | 1 | 3 ✅ |
| Maxime | 4 | 3 (lun 08:30, mer 10:30, sam 11:00) | 1 | 4 ✅ |
| Camille | 3 | 2 (lun 11:00, ven 10:00) | 1 | 3 ✅ |
| Hugo | 2 | 2 (mar 15:00, ven 16:00) | 0 | 2 ✅ |
| Manon | 1 | 1 (mer 09:00) | 0 | 1 ✅ |
| Théo | 3 | 1 (lun 09:30) | 2 | 3 ✅ |
| Lina | 2 | 1 (jeu 16:00) | 1 | 2 ✅ |
| Élise | 4 | 2 (mar 09:00, sam 10:00) | 2 | 4 ✅ |
| Tom | 1 | 0 | 1 | 1 ✅ |

**Total :** 57 sessions (39 récurrents + 18 à générer)

---

## 🐛 Points de Vigilance

- **13 créneaux à capacité maximale** : Tous les créneaux récurrents ont 3 étudiants
- **Sofia & Lucas** : 4 cours/semaine avec 4 récurrents → déjà complets, rien à générer
- **Hugo & Manon** : Déjà complets avec leurs récurrents
- **7 groupes liés** : Complexité maximale pour la gestion des contraintes
- **Mix :00 et :30** : Valider le bon fonctionnement sur tous les créneaux
- **18 sessions à générer** : L'algorithme doit optimiser le placement
- **Charge CPU** : Temps d'exécution potentiellement plus long (surveiller < 15s)

---

## 📝 Notes

Ce test case valide :
- ✅ La montée en charge extrême (22 étudiants, 57 sessions)
- ✅ La capacité maximale systématique (13 créneaux à 3 étudiants)
- ✅ La gestion de 7 groupes liés simultanés
- ✅ Le mix complet de sessions_par_semaine (1, 2, 3, 4)
- ✅ Les créneaux à :00 et :30 mélangés
- ✅ La répartition sur 6 jours (lundi-samedi)
- ✅ L'optimisation pour placer 18 cours supplémentaires

**Edge Cases Couverts :**
- EC4 : Capacité Maximum (13 créneaux à 3 étudiants - validation maximale)
- EC5 : Créneaux Samedi (4 créneaux différents)
- EC6 : Créneaux à :30 (multiples créneaux)
- EC10 : Montée en charge (22 étudiants, 57 sessions)

**Edge Cases Non Couverts :**  
Pour les cas limites restants (groupes incompatibles, disponibilités insuffisantes, etc.), voir [`../EDGE_CASES_TODO.md`](../EDGE_CASES_TODO.md)
