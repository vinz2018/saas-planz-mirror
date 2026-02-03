# Template CSV - Créneaux Récurrents

## 📋 Instructions d'utilisation

Ce template permet de définir les **créneaux récurrents** des élèves ayant des habitudes fixes (même jour/heure chaque semaine).

1. **Télécharger** ce template : `template-recurring-slots.csv`
2. **Identifier** les élèves avec habitudes fixes (ex: Vincent toujours mardi 17h)
3. **Remplir** une ligne par créneau récurrent
4. **Sauvegarder** en CSV
5. **Upload** dans l'application Streamlit (optionnel - si absent, algo optimise tout)

---

## 📊 Colonnes du Template

| Colonne | Description | Exemple | Obligatoire |
|---------|-------------|---------|-------------|
| `nom` | Prénom/Nom de l'élève | `Vincent` | ✅ Oui |
| `jour` | Jour de la semaine | `lundi` | ✅ Oui |
| `heure_debut` | Heure de début du cours | `08:00` ou `17:30` | ✅ Oui |
| `heure_fin` | Heure de fin du cours | `09:00` ou `18:30` | ✅ Oui |

---

## ✅ Format des Valeurs

### Jours (toujours en minuscules) :
- `lundi`, `mardi`, `mercredi`, `jeudi`, `vendredi`, `samedi`, `dimanche`

### Heures (format HH:MM, sur :00 ou :30 uniquement) :
- ✅ Correct : `08:00`, `08:30`, `17:00`, `17:30`
- ❌ Incorrect : `8h`, `08:15`, `17h30`

### Durée :
- Tous les cours doivent durer exactement **1 heure**
- Exemple : `08:00 → 09:00` ✅
- Exemple invalide : `08:00 → 10:00` ❌ (2h)

---

## 💡 Exemples

### Élève avec 2 créneaux récurrents :
```csv
Vincent,mardi,17:00,18:00
Vincent,vendredi,12:00,13:00
```
☝️ Vincent a toujours cours mardi 17h-18h ET vendredi 12h-13h

### Groupe d'élèves au même créneau :
```csv
Hugo,lundi,08:00,09:00
Juliette,lundi,08:00,09:00
```
☝️ Hugo et Juliette font toujours cours ensemble le lundi 8h-9h

### Élève avec 1 seul créneau récurrent :
```csv
Sarah,mercredi,10:00,11:00
```
☝️ Sarah a toujours cours mercredi 10h-11h (ses autres sessions sont optimisées par l'algo)

---

## 🚫 Erreurs Courantes

**❌ Élève non présent dans le CSV principal :**
```csv
Marie,lundi,08:00,09:00  # ERREUR si Marie n'est pas dans template-disponibilites.csv
```

**❌ Créneau hors des disponibilités de l'élève :**
```csv
Vincent,lundi,08:00,09:00  # ERREUR si Vincent n'est pas dispo lundi matin dans le CSV principal
```

**❌ Trop d'élèves dans un même cours :**
```csv
# 4 élèves dans le même cours → ERREUR (max 3 élèves + Tony)
Hugo,lundi,08:00,09:00
Juliette,lundi,08:00,09:00
Sarah,lundi,08:00,09:00
Victor,lundi,08:00,09:00
```
☝️ Maximum **3 élèves par cours** + Tony

**❌ Cours qui se chevauchent (UN SEUL COURS À LA FOIS) :**
```csv
# Cours simultanés → ERREUR (un seul cours à la fois)
Hugo,lundi,08:00,09:00
Sarah,lundi,08:30,09:30
```
☝️ Ces deux cours se chevauchent (08:30-09:00 en commun) → **INVALIDE**

**❌ Durée incorrecte :**
```csv
Vincent,mardi,17:00,19:00  # ERREUR - 2h au lieu de 1h
```

---

## 📌 Notes Importantes

1. **Ce fichier est optionnel** : Si vous ne l'uploadez pas, l'algorithme optimisera tous les créneaux (pas de squelette récurrent).

2. **Squelette = 70-80% des élèves** : En général, vous devriez avoir ici les élèves avec habitudes très fixes. Les autres sont dans le CSV principal uniquement.

3. **Validation stricte** : L'algorithme vérifie que le squelette respecte toutes les contraintes :
   - **UN SEUL COURS À LA FOIS** (aucun chevauchement entre cours)
   - Capacité par cours (2-3 élèves + Tony)
   - Disponibilités respectées
   - Pas de conflits élèves

4. **Contrainte UN SEUL COURS À LA FOIS** : Très important ! Vous ne pouvez PAS avoir :
   - Lundi 08:00-09:00 (Hugo, Juliette)
   - Lundi 08:30-09:30 (Sarah, Victor)
   → Ces deux cours se chevauchent → ERREUR

5. **Groupes liés** : Si Vincent et Jerome font toujours cours ensemble, mettez-les sur la même ligne (même jour/heure) et spécifiez leur lien dans le CSV principal (`groupe_lie`).

6. **Nombre de sessions** : Si Vincent a `sessions_par_semaine=2` et vous définissez 2 créneaux récurrents ici, il sera placé uniquement via le squelette (pas d'optimisation).

---

## 🔄 Mise à jour des récurrents

**Scénario :** Après la première semaine, Tony ajuste manuellement le planning (déplace Sarah de lundi 8h à mardi 9h). Il veut garder cet ajustement pour les semaines suivantes.

**Solution (Phase 2+) :** Bouton "💾 Sauvegarder comme récurrent" dans l'UI pour mettre à jour ce CSV automatiquement.

**MVP :** Tony doit éditer manuellement ce CSV si les habitudes changent.

---

## 🆘 Support

Problème avec le template ? Contacte Vincent avec :
- Le fichier CSV problématique
- Message d'erreur (si applicable)
- Capture d'écran
