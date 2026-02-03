# Script de Validation des CSV de Test Cases

## 📋 Description

Le script `validate_test_csv.py` valide automatiquement les fichiers CSV de test cases avant de les charger dans Streamlit. Il détecte les erreurs de format, les incohérences de données, et les problèmes de validation croisée.

## 🚀 Usage

### Valider un test case unique

```bash
python scripts/validate_test_csv.py docs/examples/test-cases/01-simple/
```

### Valider tous les test cases

```bash
python scripts/validate_test_csv.py docs/examples/test-cases/
```

### Mode strict (warnings = erreurs)

```bash
python scripts/validate_test_csv.py docs/examples/test-cases/ --strict
```

## ✅ Validations Effectuées

### Fichier `disponibilites.csv`

- ✅ Header exact avec 16 colonnes dans le bon ordre
- ✅ Nombre de champs correct (16) pour chaque ligne
- ✅ `sessions_par_semaine` est un entier entre 1 et 7
- ✅ Format d'heure valide : `HH:MM` (ex: `08:00`, pas `8:00`)
- ✅ Plages horaires cohérentes (début < fin)
- ✅ Plages horaires complètes (les deux champs remplis ou vides)

### Fichier `recurring-slots.csv`

- ✅ Header exact avec 4 colonnes
- ✅ Nombre de champs correct (4) pour chaque ligne
- ✅ `nom` existe dans `disponibilites.csv`
- ✅ `jour` est valide (lundi, mardi, etc. en minuscules)
- ✅ Format d'heure valide : `HH:MM`
- ✅ Créneau récurrent **dans** les disponibilités de l'étudiant

### Validations Croisées

- ✅ Cohérence entre `recurring-slots.csv` et `disponibilites.csv`
- ✅ Les créneaux récurrents sont des sous-plages des disponibilités

## 📊 Sorties

### Succès

```
✅ Aucune erreur détectée ! Le test case est valide.
```

### Erreurs

```
❌ disponibilites.csv:3 (colonne: sessions_par_semaine) - Type invalide: '2.5'. Doit être un entier.
❌ recurring-slots.csv:2 - Créneau récurrent lundi 08:00-09:00 non trouvé dans les disponibilités de Alice
```

### Warnings

```
⚠️  recurring-slots.csv:0 - Fichier manquant (optionnel)
```

## 🐛 Leçons Apprises du Debug du Test Case 01

Ce script intègre toutes les validations qui ont été découvertes lors du debug :

1. **Nombre de colonnes exact** : Évite les décalages de champs
2. **Virgules manquantes** : Détecte les champs manquants avant `groupe_lie` et `notes`
3. **Format des heures** : `08:00` au lieu de `8:00` ou autres variantes
4. **Type de `sessions_par_semaine`** : Entier, pas string ou float
5. **Cohérence des créneaux** : Le créneau récurrent doit être **dans** la plage de disponibilité
6. **Virgules dans les notes** : À éviter ou échapper avec guillemets

## 🔧 Intégration dans le Workflow

**Avant de tester un test case dans Streamlit :**

```bash
# 1. Valider les CSV
python scripts/validate_test_csv.py docs/examples/test-cases/XX-nom/

# 2. Si validation OK, tester dans Streamlit
cd /home/vincent/saas-planz && ./run-mvp.sh start
```

## 📝 Code de Sortie

- `0` : Validation réussie
- `1` : Validation échouée (au moins une erreur)

Utile pour l'automatisation et les CI/CD :

```bash
if python scripts/validate_test_csv.py docs/examples/test-cases/; then
    echo "✅ Tous les test cases sont valides"
else
    echo "❌ Des erreurs ont été détectées"
    exit 1
fi
```
