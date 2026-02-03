# Edge Cases à Tester - TODO

Ce document liste les cas limites identifiés qui devraient être couverts par des test cases dédiés.

---

## 🚨 High Priority

### EC1 : Groupes Liés avec Disponibilités Incompatibles
**Description :** Deux étudiants configurés comme groupe lié mais sans disponibilités communes.

**Exemple :**
- Sophie (groupe_lie: Julie) : disponible lundi 08:00-12:00
- Julie (groupe_lie: Sophie) : disponible mardi 14:00-18:00 uniquement

**Comportement Attendu :**
- Le parser devrait détecter l'incohérence
- Générer une erreur claire : "Groupe lié Sophie-Julie : aucune disponibilité commune"
- Suggestions : "Vérifier les disponibilités ou retirer le lien de groupe"

**Statut :** ❌ Non testé  
**Test Case Suggéré :** `06-edge-cases/incompatible-linked-groups/`

---

### EC2 : Étudiant avec Très Peu de Disponibilités
**Description :** Un étudiant avec seulement 2h de disponibilité par semaine mais `sessions_par_semaine=2`.

**Exemple :**
- Martin : sessions_par_semaine=2, disponible samedi 09:00-11:00 uniquement

**Comportement Attendu :**
- Impossible de placer 2 cours de 1h dans une seule plage de 2h (car 2 cours séparés)
- Le système devrait le placer une seule fois et signaler l'échec pour la 2ème session
- Message : "Martin : impossible de placer 2 cours/semaine avec seulement 2h disponibles"

**Statut :** ❌ Non testé  
**Test Case Suggéré :** `06-edge-cases/insufficient-availability/`

---

### EC3 : Créneau Récurrent à 1 Étudiant (Warnings)
**Description :** Créneau récurrent avec un seul étudiant. Le système devrait générer un warning mais accepter.

**Exemple :**
- Nicolas : lundi 10:00-11:00 (seul dans ce créneau récurrent)

**Comportement Attendu :**
- Le créneau est accepté avec status `NEEDS_VALIDATION`
- Warning généré : "Créneau lundi 10:00-11:00 avec 1 seul étudiant. Envisager d'ajouter : Alice, Bob..."
- Suggestions d'étudiants compatibles affichées

**Statut :** ⚠️ Partiellement implémenté (code modifié mais pas testé end-to-end)  
**Test Case Suggéré :** `02-moyen/` (déjà présent : Isabelle seule jeudi 16:00-17:00)

---

## 🔶 Medium Priority

### EC4 : Capacité Maximum (3 Étudiants)
**Description :** Valider le comportement quand un créneau a exactement 3 étudiants (limite max).

**Exemple :**
- Créneau récurrent mardi 15:00-16:00 avec Alice, Bob, Charlie (3 étudiants)

**Comportement Attendu :**
- Le créneau est accepté et marqué comme "full"
- L'algorithme ne doit pas essayer d'ajouter un 4ème étudiant dans ce créneau

**Statut :** ❌ Non testé  
**Test Case Suggéré :** `03-complexe/`

---

### EC5 : Créneaux Samedi
**Description :** Valider la gestion des cours le samedi (jour moins fréquent).

**Exemple :**
- Laura disponible samedi 09:00-12:00
- Créneau récurrent samedi 10:00-11:00

**Comportement Attendu :**
- Le samedi est traité comme n'importe quel autre jour
- Les créneaux samedi sont correctement placés dans le planning

**Statut :** ❌ Non testé (02-moyen n'a pas de recurring samedi)  
**Test Case Suggéré :** `03-complexe/`

---

### EC6 : Créneaux à :30 minutes
**Description :** Valider les créneaux commençant ou finissant à :30.

**Exemple :**
- Sophie disponible lundi 09:30-12:00
- Créneau récurrent lundi 09:30-10:30

**Comportement Attendu :**
- Les créneaux à :30 sont acceptés
- L'algorithme peut placer des cours à 09:30, 10:30, 11:30, etc.

**Statut :** ❌ Non testé  
**Test Case Suggéré :** `03-complexe/`

---

### EC7 : `sessions_par_semaine=3` avec 1 Seul Récurrent
**Description :** Étudiant avec 3 cours/semaine mais un seul créneau récurrent.

**Exemple :**
- Laura : sessions_par_semaine=3, récurrent mercredi 08:00-09:00 (1 cours fixe)
- Les 2 autres cours doivent être générés par l'algorithme

**Comportement Attendu :**
- Le créneau récurrent compte comme 1/3 des sessions
- L'algorithme doit placer les 2 cours restants dans les disponibilités flexibles
- Documentation claire dans le planning : "Laura : 1 cours fixe + 2 cours générés"

**Statut :** ⚠️ Présent dans 02-moyen mais pas documenté  
**Test Case Suggéré :** `02-moyen/` (Laura et Paul)

---

## 🟢 Low Priority

### EC8 : Noms avec Caractères Spéciaux
**Description :** Noms d'étudiants avec accents, apostrophes, traits d'union.

**Exemple :**
- Léa, Jean-François, O'Connor

**Comportement Attendu :**
- Les noms sont correctement parsés et affichés
- Pas d'erreur d'encodage UTF-8

**Statut :** ❌ Non testé  
**Test Case Suggéré :** `05-extreme/`

---

### EC9 : Notes avec Virgules
**Description :** Notes contenant des virgules (potentiellement problématiques en CSV).

**Exemple :**
- Notes : "Préfère le matin, éviter les après-midis"

**Comportement Attendu :**
- Le parser gère correctement les virgules échappées dans les notes
- Validation du script détecte les virgules non échappées

**Statut :** ⚠️ Partiellement testé (validation détecte les erreurs)  
**Test Case Suggéré :** `05-extreme/`

---

## 📝 Comment Utiliser ce Document

1. **Avant de créer un nouveau test case**, consulter cette liste
2. **Cocher les edge cases couverts** avec ✅ au fur et à mesure
3. **Ajouter de nouveaux edge cases** découverts pendant le développement
4. **Prioriser** les edge cases selon leur impact sur Tony (High > Medium > Low)

---

## 🎯 Roadmap Suggérée

**Phase 1 : Validation du Happy Path**
- ✅ Test Case 01 : Simple (5 étudiants, happy path)
- ✅ Test Case 02 : Moyen (9 étudiants, groupes variés)

**Phase 2 : Complexité Croissante**
- 🔜 Test Case 03 : Complexe (12-15 étudiants, samedi, capacité max)
- 🔜 Test Case 04 : Très Complexe (20+ étudiants, tous les jours)

**Phase 3 : Edge Cases et Robustesse**
- 🔜 Test Case 05 : Extrême (caractères spéciaux, notes complexes)
- 🔜 Test Case 06 : Edge Cases (groupes incompatibles, dispo insuffisantes)

**Phase 4 : Tests Automatisés**
- 🔜 Pytest pour chaque edge case
- 🔜 CI/CD avec validation automatique des CSV
