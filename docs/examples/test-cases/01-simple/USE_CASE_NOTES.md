# Use Cases Identifiés - Test Case 01-Simple

## 🚨 Use Case Important : Créneaux Récurrents vs Disponibilités

### Problème Rencontré
Lors du test du POC, nous avons identifié un conflit entre un créneau récurrent et les disponibilités déclarées :
- **Emma** : Créneau récurrent `lundi 08:00-09:00`
- **Emma** : Disponibilité déclarée `lundi 10:00-12:00`

Le parser a rejeté cette incohérence avec l'erreur :
```
Row 3 (Emma): Recurring slot lundi 08:00:00-09:00:00 not in student's availability
```

### Contexte Réel
Dans la vraie vie, ce cas peut arriver pour plusieurs raisons :
1. **Créneaux exceptionnels** : Accord verbal entre coach et élève pour un cours en dehors des disponibilités habituelles
2. **Disponibilités incomplètes** : L'élève oublie de déclarer certaines plages horaires qu'il utilise déjà
3. **Créneaux legacy** : Cours existants depuis longtemps, avant la mise en place du système de disponibilités structurées

### Solutions Possibles pour l'Application Finale

#### Option A : Warning + Override (⭐ Recommandé)
- Afficher un **warning visuel** dans l'UI
- Permettre au coach de **forcer le placement** (bouton "Ignorer et continuer")
- Logger ces exceptions pour audit

**Avantages :**
- Flexibilité pour gérer les cas réels
- Visibilité sur les incohérences sans bloquer le workflow

**Inconvénients :**
- Risque d'erreurs si le coach force sans vérifier

---

#### Option B : Validation Stricte
- **Bloquer** la génération du planning
- Forcer la correction des disponibilités d'abord (ajouter le créneau 08:00-09:00 pour Emma)

**Avantages :**
- Données toujours cohérentes
- Force la rigueur

**Inconvénients :**
- Workflow plus lourd
- Peut frustrer l'utilisateur pour des exceptions légitimes

---

#### Option C : Suggestions de Correction Intelligentes
- Détecter le conflit
- Proposer **automatiquement** : "Emma a un cours récurrent lundi 08:00-09:00 mais ce créneau n'est pas dans ses disponibilités. Voulez-vous l'ajouter ?"
- Boutons : `Ajouter aux disponibilités` / `Supprimer le créneau récurrent` / `Ignorer`

**Avantages :**
- UX optimale (guidage)
- Résolution rapide

**Inconvénients :**
- Logique plus complexe à implémenter

---

### Recommandation pour le MVP
**Option A (Warning + Override)** avec :
- Un warning visible : ⚠️ "Emma : Créneau lundi 08:00-09:00 en dehors des disponibilités déclarées"
- Un bouton "Générer quand même" avec confirmation
- Un log des exceptions forcées dans les résultats

### Correction Temporaire pour le POC
Pour ce test case, nous avons corrigé `recurring-slots.csv` pour que Emma soit à `lundi 10:00-11:00` (dans sa plage de disponibilité).

---

## 📋 Actions Futures
- [ ] Implémenter Option A dans Streamlit UI
- [ ] Ajouter un test case spécifique pour ce scénario (test-case 06-conflicts ?)
- [ ] Documenter le comportement dans la doc utilisateur
- [ ] Ajouter des logs d'audit pour les overrides

---

**Date** : 2026-02-01  
**Identifié par** : Vincent (POC testing)  
**Priorité** : Moyenne (bloque le workflow actuel, mais contournable)
