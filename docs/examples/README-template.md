# Template CSV - Disponibilités Élèves

## 📋 Instructions d'utilisation

1. **Télécharger** ce template : `template-disponibilites.csv`
2. **Ouvrir** dans Excel / Numbers / Google Sheets
3. **Remplir** une ligne par élève avec ses disponibilités
4. **Sauvegarder** en CSV
5. **Upload** dans l'application Streamlit

---

## 📊 Colonnes du Template

| Colonne | Description | Exemple | Obligatoire |
|---------|-------------|---------|-------------|
| `nom` | Prénom ou Nom de l'élève | `Vincent` | ✅ Oui |
| `sessions_par_semaine` | Nombre de cours souhaités par semaine | `2` | ✅ Oui |
| `lundi_debut` | Dispo lundi : heure de début | `08:00` | ❌ Non |
| `lundi_fin` | Dispo lundi : heure de fin | `19:00` | ❌ Non |
| `mardi_debut` | Dispo mardi : heure de début | `17:00` | ❌ Non |
| `mardi_fin` | Dispo mardi : heure de fin | `18:30` | ❌ Non |
| `mercredi_debut` | Dispo mercredi : heure de début | `12:00` | ❌ Non |
| `mercredi_fin` | Dispo mercredi : heure de fin | `14:00` | ❌ Non |
| `jeudi_debut` | Dispo jeudi : heure de début | `08:00` | ❌ Non |
| `jeudi_fin` | Dispo jeudi : heure de fin | `09:00` | ❌ Non |
| `vendredi_debut` | Dispo vendredi : heure de début | `12:00` | ❌ Non |
| `vendredi_fin` | Dispo vendredi : heure de fin | `13:30` | ❌ Non |
| `samedi_debut` | Dispo samedi : heure de début | `09:00` | ❌ Non |
| `samedi_fin` | Dispo samedi : heure de fin | `10:00` | ❌ Non |
| `groupe_lie` | Nom de l'élève avec qui faire cours | `jerome` | ❌ Non (optionnel) |
| `notes` | Commentaires / contraintes spéciales | Texte libre | ❌ Non |

**💡 Important :** Chaque jour a deux colonnes (`_debut` et `_fin`) pour définir une **plage horaire**. Si l'élève n'est pas disponible un jour, laissez les deux colonnes vides.

---

## ✅ Format des Valeurs

### Heures (format HH:MM sur 24h) :
- ✅ Correct : `08:00`, `17:30`, `12:15`
- ❌ Incorrect : `8h`, `8h00`, `17h30`, `8:00` (utilisez toujours 2 chiffres)

### Plages horaires :
- **Toujours remplir les DEUX colonnes** : `_debut` ET `_fin`
- ✅ Correct : `lundi_debut=08:00, lundi_fin=19:00`
- ❌ Incorrect : `lundi_debut=08:00, lundi_fin=(vide)`

### Cellules vides :
- Si l'élève n'est **pas disponible** un jour, laissez `_debut` ET `_fin` vides
- Exemple : pas dispo le mercredi → `mercredi_debut=(vide), mercredi_fin=(vide)`

---

## 💡 Exemples

### Élève dispo sur créneaux précis (2 sessions) :
```csv
Vincent,2,,,17:00,18:30,,,,,12:00,13:30,,,jerome,
```
☝️ Dispo **mardi 17h-18h30** ET **vendredi 12h-13h30**

### Élève dispo toute une journée (1 session) :
```csv
Sarah,1,08:00,19:00,,,,,,,,,,,Dispo toute la journée lundi
```
☝️ Dispo **lundi de 8h à 19h** (l'algo choisira le meilleur créneau)

### Groupe lié (couple/amis) :
```csv
Caroline,1,,,,,,,,,,,09:00,10:00,,Avec Franck
Franck,1,,,,,,,,,,,09:00,10:00,caroline,Avec Caroline
```
☝️ Les deux doivent avoir la **même plage horaire** ET **groupe_lie** renseigné

### Élève dispo plusieurs jours avec plages différentes :
```csv
Hugo,2,08:00,09:00,,,,,08:00,10:00,,,,,
```
☝️ Dispo **lundi 8h-9h** ET **jeudi 8h-10h**

### Élève très flexible (large plage, plusieurs jours) :
```csv
Juliette,2,08:00,19:00,08:00,19:00,08:00,19:00,08:00,19:00,08:00,19:00,,,Très flexible
```
☝️ Dispo **lundi à vendredi, 8h-19h** (l'algo optimisera)

---

## 🚫 Erreurs Courantes

**❌ Heure mal formatée :**
```csv
Vincent,2,,,17h30,18:30  # INCORRECT - utiliser 17:30 (pas 17h30)
```

**❌ Plage incomplète (debut sans fin) :**
```csv
Vincent,2,,,17:00,,,,  # INCORRECT - si mardi_debut renseigné, mardi_fin DOIT l'être aussi
```

**❌ Fin avant début :**
```csv
Vincent,2,,,18:30,17:00  # INCORRECT - mardi_fin (18:30) doit être APRÈS mardi_debut (17:00)
```

**❌ Pas assez de disponibilités :**
```csv
Vincent,2,,,17:00,18:30  # INCORRECT - veut 2 sessions/semaine mais 1 seule plage horaire fournie
```
☝️ **Solution :** Ajouter d'autres plages (ex: `vendredi_debut=12:00, vendredi_fin=13:30`)

**❌ Groupe lié non réciproque :**
```csv
Vincent,2,,,17:00,18:30,,,,,,,,,jerome,
Jerome,1,,,17:00,18:30,,,,,,,,,,  # INCORRECT - Jerome doit aussi avoir groupe_lie=vincent
```

---

## 📌 Notes Importantes

1. **Plages vs créneaux fixes :**
   - Plage large (ex: `08:00,19:00`) → L'algo choisit le meilleur créneau d'1h
   - Plage courte (ex: `17:00,18:00`) → L'algo place le créneau à 17h précisément
   
2. **Plusieurs jours possibles :**
   - Remplir autant de colonnes jour que nécessaire
   - L'algo choisira les jours optimaux selon `sessions_par_semaine`
   
3. **Virgules** : Éviter les virgules dans la colonne `notes` (utiliser point-virgule à la place)

4. **Encoding** : Sauvegarder en UTF-8 si caractères spéciaux (accents)

5. **Ordre** : L'ordre des lignes n'a pas d'importance

---

## 🔄 Migration depuis l'ancien format

Si tu as l'ancien CSV avec texte libre ("entre 8h00 et 9h00"), contacte Vincent pour assistance de migration.

**Conversion rapide :**
- Ancien : `lundi,mardi,mercredi,jeudi,vendredi,samedi entre 8h00 et 19h30`
- Nouveau : `lundi_debut=08:00, lundi_fin=19:30, mardi_debut=08:00, mardi_fin=19:30, ...` (pour chaque jour)

---

## 🆘 Support

Problème avec le template ? Contacte Vincent avec :
- Le fichier CSV problématique
- Message d'erreur (si applicable)
- Capture d'écran
