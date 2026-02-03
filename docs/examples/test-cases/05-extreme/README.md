# Test Case 05 - Extrême

**Niveau :** ⭐⭐⭐⭐⭐ Limite Maximale  
**Élèves :** 30  
**Complexité :** Extrême

---

## 📋 Caractéristiques

- **30 étudiants** avec disponibilités très variées :
  - 10 paires de groupes liés (20 étudiants)
  - 10 étudiants solo
- **54 créneaux récurrents individuels** formant **18 classes** :
  - **TOUS les 18 créneaux sont à capacité maximale** (3 étudiants chacun)
- **Mix complet de `sessions_par_semaine` :** 1, 2, 3, et 4 cours par semaine
- **Horaires variés avec :00 et :30** sur toute la journée
- **Créneaux sur 6 jours** (lundi à samedi)
- **Total : 89 sessions** à générer (54 récurrents + 35 à générer par l'algorithme)
- **Charge extrême** : Test des limites du système

---

## 🎯 Objectif

Valider les limites absolues du système et la performance sous charge maximale :
- ✅ Montée en charge maximale (30 étudiants, 89 sessions totales)
- ✅ Tous les créneaux récurrents à capacité max (18 créneaux × 3 étudiants)
- ✅ 10 groupes liés à gérer simultanément (complexité maximale)
- ✅ Mix complet de sessions_par_semaine (1, 2, 3, 4)
- ✅ Créneaux à :00 et :30 sur toute la journée (08:00-18:30)
- ✅ Répartition sur 6 jours
- ✅ Optimisation pour placer 35 sessions supplémentaires
- ✅ Performance CPU sous charge extrême (temps < 20s)

---

## 📊 Détails des Étudiants

### Groupes Liés (10 paires)

**Léa & Noah** (Experts ultra flexibles)
- 4 cours/semaine chacun
- Ultra-flexibles : lundi à samedi (08:00-13:00 ou 12:00)
- Récurrents : lundi 08:30, mardi 09:00, vendredi 10:00, samedi 11:00 (4 créneaux = complet)

**Emma & Lucas** (Avancés matins toute semaine)
- 4 cours/semaine chacun
- Disponibles 6 jours/7 : lundi à samedi (08:30-12:30 ou 12:00)
- Récurrents : lundi 09:30, jeudi 08:30 (2 créneaux)

**Alice & Gabriel** (Intermédiaires après-midi)
- 3 cours/semaine chacun
- Disponibles : mardi à samedi (14:00-18:30 ou 10:00-13:00 samedi)
- Récurrents : mardi 15:00, jeudi 16:00 (2 créneaux)

**Sofia & Louis** (Avancés milieu matinée)
- 3 cours/semaine chacun
- Disponibles 6 jours/7 : lundi à samedi (09:00-12:30 ou 12:00)
- Récurrents : mardi 10:00, samedi 10:00 (2 créneaux)

**Chloé & Arthur** (Experts ultra disponibles)
- 4 cours/semaine chacun
- Ultra-disponibles : lundi à samedi (08:00-18:00 ou 13:00)
- Récurrents : lundi 11:00, jeudi 08:30 (2 créneaux)

**Jade & Raphaël** (Flexibles après-midi)
- 2 cours/semaine chacun
- Disponibles : mardi à samedi (15:00-18:00 ou 09:30-12:30)
- Récurrent : jeudi 16:30 (1 créneau)

**Zoé & Maxime** (Réguliers milieu matinée)
- 3 cours/semaine chacun
- Disponibles 6 jours/7 : lundi à samedi (09:30-13:00 ou 12:30)
- Récurrents : mercredi 10:00, vendredi 11:30 (2 créneaux)

**Camille & Hugo** (Débutants fin matinée)
- 2 cours/semaine chacun
- Disponibles 6 jours/7 : lundi à samedi (10:00-12:00)
- Récurrent : mardi 10:00 (partagé avec Sofia & Louis) (1 créneau)

**Inès & Tom** (Avancés matins complets)
- 3 cours/semaine chacun
- Disponibles 6 jours/7 : lundi à samedi (08:00-12:00)
- Récurrents : mercredi 08:00, samedi 09:00 (2 créneaux)

**Élise & Théo** (Experts réguliers)
- 4 cours/semaine chacun
- Disponibles 6 jours/7 : lundi à samedi (09:00-13:00 ou 12:00)
- Récurrents : mercredi 11:00, vendredi 09:00 (2 créneaux)

### Étudiants Solo (10)

**Manon** (Solo ultra flexible pro)
- 4 cours/semaine
- Ultra-flexible : lundi à samedi (08:00-18:00 ou 13:00)
- Récurrents : lundi 08:30, mercredi 11:00, samedi 11:00 (3 créneaux)

**Lina** (Solo matins très régulière)
- 4 cours/semaine
- Disponible 6 jours/7 : lundi à samedi (09:00-13:00 ou 12:00)
- Récurrents : mardi 09:00, vendredi 10:00 (2 créneaux)

**Océane** (Solo matins décalés)
- 3 cours/semaine
- Disponible 6 jours/7 : lundi à samedi (08:30-12:00)
- Récurrents : lundi 09:30, vendredi 11:30 (2 créneaux)

**Jules** (Solo fin matinée régulier)
- 3 cours/semaine
- Disponible 6 jours/7 : lundi à samedi (10:00-13:00 ou 12:00)
- Récurrents : lundi 11:00, mercredi 10:00, samedi 09:00 (3 créneaux = complet)

**Paul** (Solo après-midi)
- 2 cours/semaine
- Disponible : mardi à samedi (14:30-18:00 ou 10:30-13:00)
- Récurrent : mardi 15:00 (1 créneau)

**Nina** (Solo fin après-midi)
- 2 cours/semaine
- Disponible : mardi à vendredi (15:30-18:30)
- Récurrent : jeudi 16:00 (1 créneau)

**Clara** (Solo début matinée)
- 1 cours/semaine
- Disponible : lundi à vendredi (08:00-10:00)
- Récurrents : Aucun

**Marc** (Solo matins longs)
- 3 cours/semaine
- Disponible 6 jours/7 : lundi à samedi (08:00-12:30 ou 12:00)
- Récurrents : mercredi 08:00, vendredi 09:00 (2 créneaux)

**Léna** (Solo milieu matinée)
- 1 cours/semaine
- Disponible : lundi à vendredi (10:30-12:30)
- Récurrents : Aucun

**Eva** (Solo fin journée samedi)
- 2 cours/semaine
- Disponible : mardi à samedi (16:00-18:00 ou 11:00-13:00)
- Récurrent : jeudi 16:30 (1 créneau)

---

## 📊 Résultat Attendu

- **~89 cours générés** (total des sessions_par_semaine)
- **Tous les groupes liés respectés** (10 paires toujours ensemble)
- **54 créneaux récurrents individuels** intégrés au squelette (18 classes à capacité max)
- **18 créneaux à capacité maximale** (3 étudiants chacun - record absolu)
- **35 sessions supplémentaires** à générer par l'algorithme
- **Temps d'exécution :** < 20s (charge extrême)

### Métriques Attendues

- Taux de placement : **~100%** (tous les étudiants placés)
- Créneaux récurrents : **100%** (tous utilisés)
- Groupes liés : **100%** (toujours ensemble)
- Créneaux à capacité max : **18** (validation maximale absolue)
- Performance : < 20s pour 30 étudiants et 89 sessions

---

## 🚀 Test dans Streamlit

```bash
./run-mvp.sh start
```

1. Upload `disponibilites.csv` (30 étudiants)
2. Upload `recurring-slots.csv` (54 slots = 18 classes)
3. Cliquer sur "Générer Planning"
4. Vérifier :
   - ✅ ~100% des étudiants placés
   - ✅ Groupes liés respectés (10 paires)
   - ✅ Créneaux récurrents intégrés (18 classes, tous à 3 étudiants)
   - ✅ Créneaux à :00 et :30 sur toute la journée
   - ✅ Créneaux samedi bien placés
   - ✅ Pas de chevauchement de cours (UN SEUL COURS À LA FOIS)
   - ✅ Temps d'exécution raisonnable (< 20s)
   - ✅ Utilisation CPU/mémoire acceptable

---

## 🔍 Validation des Fichiers

Avant de tester dans Streamlit, valider les CSV :

```bash
python scripts/validate_test_csv.py docs/examples/test-cases/05-extreme/
```

---

## ⚙️ Logique Créneaux Récurrents vs Sessions Par Semaine

**Total : 89 sessions** (54 récurrents + 35 à générer)

| Étudiant | sessions_par_semaine | Récurrents (fixes) | À générer | Total |
|----------|---------------------|-------------------|-----------|-------|
| Léa | 4 | 4 (lun 08:30, mar 09:00, ven 10:00, sam 11:00) | 0 | 4 ✅ |
| Noah | 4 | 4 (lun 08:30, mar 09:00, ven 10:00, sam 11:00) | 0 | 4 ✅ |
| Emma | 4 | 2 (lun 09:30, jeu 08:30) | 2 | 4 ✅ |
| Lucas | 4 | 2 (lun 09:30, jeu 08:30) | 2 | 4 ✅ |
| Alice | 3 | 2 (mar 15:00, jeu 16:00) | 1 | 3 ✅ |
| Gabriel | 3 | 2 (mar 15:00, jeu 16:00) | 1 | 3 ✅ |
| Sofia | 3 | 2 (mar 10:00, sam 10:00) | 1 | 3 ✅ |
| Louis | 3 | 2 (mar 10:00, sam 10:00) | 1 | 3 ✅ |
| Chloé | 4 | 2 (lun 11:00, jeu 08:30) | 2 | 4 ✅ |
| Arthur | 4 | 2 (lun 11:00, jeu 08:30) | 2 | 4 ✅ |
| Jade | 2 | 1 (jeu 16:30) | 1 | 2 ✅ |
| Raphaël | 2 | 1 (jeu 16:30) | 1 | 2 ✅ |
| Zoé | 3 | 2 (mer 10:00, ven 11:30) | 1 | 3 ✅ |
| Maxime | 3 | 2 (mer 10:00, ven 11:30) | 1 | 3 ✅ |
| Camille | 2 | 1 (mar 10:00) | 1 | 2 ✅ |
| Hugo | 2 | 1 (sam 10:00) | 1 | 2 ✅ |
| Inès | 3 | 2 (mer 08:00, sam 09:00) | 1 | 3 ✅ |
| Tom | 3 | 2 (mer 08:00, sam 09:00) | 1 | 3 ✅ |
| Élise | 4 | 2 (mer 11:00, ven 09:00) | 2 | 4 ✅ |
| Théo | 4 | 2 (mer 11:00, ven 09:00) | 2 | 4 ✅ |
| Manon | 4 | 3 (lun 08:30, mer 11:00, sam 11:00) | 1 | 4 ✅ |
| Lina | 4 | 2 (mar 09:00, ven 10:00) | 2 | 4 ✅ |
| Océane | 3 | 2 (lun 09:30, ven 11:30) | 1 | 3 ✅ |
| Jules | 3 | 3 (lun 11:00, mer 10:00, sam 09:00) | 0 | 3 ✅ |
| Paul | 2 | 1 (mar 15:00) | 1 | 2 ✅ |
| Nina | 2 | 1 (jeu 16:00) | 1 | 2 ✅ |
| Clara | 1 | 0 | 1 | 1 ✅ |
| Marc | 3 | 2 (mer 08:00, ven 09:00) | 1 | 3 ✅ |
| Léna | 1 | 0 | 1 | 1 ✅ |
| Eva | 2 | 1 (jeu 16:30) | 1 | 2 ✅ |

---

## 🐛 Points de Vigilance

- **18 créneaux à capacité maximale** : TOUS les créneaux récurrents ont 3 étudiants (record absolu)
- **10 groupes liés simultanés** : Complexité de gestion des contraintes au maximum
- **Léa & Noah** : 4 cours/semaine avec 4 récurrents → déjà complets
- **Jules** : 3 cours/semaine avec 3 récurrents → déjà complet
- **35 sessions à générer** : Optimisation complexe pour placer les cours restants
- **Charge CPU extrême** : Temps d'exécution critique (< 20s attendu)
- **Mémoire** : Surveiller l'utilisation mémoire sous cette charge
- **Créneaux :00 et :30** : Validation sur toute la plage horaire (08:00-18:30)

---

## 📝 Notes

Ce test case valide :
- ✅ La montée en charge maximale (30 étudiants, 89 sessions)
- ✅ La capacité maximale absolue (18 créneaux à 3 étudiants)
- ✅ La gestion de 10 groupes liés simultanés (complexité maximale)
- ✅ Le mix complet de sessions_par_semaine (1, 2, 3, 4)
- ✅ Les créneaux à :00 et :30 sur toute la journée
- ✅ La répartition sur 6 jours (lundi-samedi)
- ✅ L'optimisation pour placer 35 cours supplémentaires
- ✅ La performance CPU sous charge extrême

**Edge Cases Couverts :**
- EC4 : Capacité Maximum (18 créneaux à 3 étudiants - validation absolue)
- EC5 : Créneaux Samedi (6 créneaux différents)
- EC6 : Créneaux à :30 (nombreux créneaux sur toute la journée)
- EC10 : Montée en charge maximale (30 étudiants, 89 sessions)
- EC11 : Performance CPU extrême (temps d'exécution critique)

**Edge Cases Non Couverts :**  
Pour les cas limites restants (groupes incompatibles, disponibilités insuffisantes, etc.), voir [`../EDGE_CASES_TODO.md`](../EDGE_CASES_TODO.md)

---

## 🏆 Objectif Final

Ce test case représente la **limite maximale** du système tel que spécifié. Si ce test passe avec succès :
- ✅ Le système peut gérer jusqu'à 30 étudiants
- ✅ Le système supporte jusqu'à ~90 sessions par semaine
- ✅ Le système gère jusqu'à 10 groupes liés simultanés
- ✅ La performance reste acceptable sous charge maximale
- ✅ L'algorithme d'optimisation fonctionne pour placer 35+ sessions supplémentaires

**Prêt pour la production !** 🚀
