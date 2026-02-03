# 🧪 Cas de Test - Complexité Croissante

5 cas de test pour valider l'algorithme de scheduling avec Streamlit.

---

## 📊 Vue d'Ensemble

| Cas | Élèves | Groupes Liés | Récurrents | Complexité | Temps Attendu |
|-----|--------|--------------|------------|------------|---------------|
| **01-simple** | 5 | 1 | 2 | ⭐ Basique | < 2s |
| **02-moyen** | 13 | 2 | 5 | ⭐⭐ Moyen | < 5s |
| **03-complexe** | 25 | 4 | 12 | ⭐⭐⭐ Avancé | 5-10s |
| **04-tres-complexe** | 39 | 7 | 27 | ⭐⭐⭐⭐ Expert | 10-15s |
| **05-extreme** | 50 | 10 | 35 | ⭐⭐⭐⭐⭐ Extrême | 10-20s |

---

## 🎯 Objectif

Tester progressivement l'algorithme avec des scénarios de plus en plus complexes :
- Valider les contraintes de base
- Tester les groupes liés multiples
- Valider l'équilibrage de charge
- Tester les cas edge (élèves avec 1 seul créneau, sans dispos, etc.)
- Valider la scalabilité (jusqu'à 50 élèves)

---

## 📂 Structure

Chaque dossier `XX-nom/` contient :
- `disponibilites.csv` - Disponibilités des élèves
- `recurring-slots.csv` - Créneaux récurrents (squelette)
- `README.md` - Description détaillée du cas de test

---

## 🚀 Utilisation dans Streamlit

### Test Rapide (01-simple)
```bash
./run-mvp.sh start
# Dans Streamlit:
# 1. Upload docs/examples/test-cases/01-simple/disponibilites.csv
# 2. Upload docs/examples/test-cases/01-simple/recurring-slots.csv
# 3. Générer Planning
# 4. Vérifier : 5 élèves placés, 1 groupe lié respecté
```

### Test Progressif
1. Commencer par `01-simple` (validation de base)
2. Passer à `02-moyen` (groupes multiples)
3. Continuer avec `03-complexe` (contraintes serrées)
4. Tester `04-tres-complexe` (proche du réel)
5. Valider avec `05-extreme` (cas réel de Tony : 50 élèves)

---

## ✅ Critères de Validation

Pour chaque cas de test :

### Obligatoire (Hard Constraints)
- [ ] Aucun overlap (1 cours à la fois)
- [ ] 2-3 élèves par cours (+ Tony = 3-4 personnes)
- [ ] Tous les cours durent exactement 1h
- [ ] Groupes liés toujours ensemble
- [ ] Créneaux coach réservés respectés (si définis)

### Recommandé (Soft Constraints)
- [ ] Récurrents intégrés au squelette
- [ ] Répartition équilibrée sur la semaine
- [ ] Maximum d'élèves placés
- [ ] Explications claires pour unplaced

### Performance
- [ ] Temps de génération < 20s
- [ ] Mémoire < 200 MB
- [ ] Pas de timeout
- [ ] Interface réactive

---

## 🐛 Cas Edge Testés

Les cas de test incluent :

**Contraintes temporelles :**
- ✅ Élèves avec 1 seul créneau possible
- ✅ Élèves sans disponibilités
- ✅ Élèves ultra-flexibles (toute la semaine)
- ✅ Préférences :30 (08:30, 09:30, etc.)

**Contraintes sociales :**
- ✅ Couples (2 personnes toujours ensemble)
- ✅ Groupes d'amis (2-3 personnes ensemble)
- ✅ Multiples groupes liés simultanés

**Contraintes logistiques :**
- ✅ Créneaux récurrents contraignants (squelette lourd)
- ✅ Élèves pivot (présents dans nombreux récurrents)
- ✅ Distribution temporelle (matin, après-midi, soir, weekend)

---

## 📈 Progression de Complexité

### 01-Simple (5 élèves)
- **But :** Valider fonctionnement de base
- **Focus :** 1 groupe lié, 2 récurrents simples
- **Attendu :** 100% placés, < 2s

### 02-Moyen (13 élèves)
- **But :** Tester groupes multiples
- **Focus :** 2 groupes liés, 5 récurrents, contraintes horaires
- **Attendu :** 100% placés, < 5s

### 03-Complexe (25 élèves)
- **But :** Valider contraintes serrées
- **Focus :** 4 groupes liés, 12 récurrents, élèves avec 1 seul créneau
- **Attendu :** 95-100% placés, 5-10s

### 04-Très Complexe (39 élèves)
- **But :** Proche du cas réel
- **Focus :** 7 groupes liés, 27 récurrents, nombreux cas edge
- **Attendu :** 95-98% placés (1 impossible), 10-15s

### 05-Extrême (50 élèves)
- **But :** Cas réel de Tony
- **Focus :** 10 groupes liés, 35 récurrents, tous les cas edge
- **Attendu :** 90-95% placés, 10-20s

---

## 📝 Notes pour Tony

Ces cas de test te permettent de :

1. **Valider l'outil** avant de l'utiliser avec tes vrais élèves
2. **Comprendre les limites** (quels cas sont impossibles)
3. **Voir les explications** quand un élève ne peut pas être placé
4. **Tester différents scénarios** (ajout d'élèves, changement de dispos)

**Conseil :** Commence par `01-simple` pour te familiariser, puis teste `04-tres-complexe` qui est proche de ton cas réel.

---

**Créé le :** 2026-02-02  
**Pour :** Test et validation MVP Streamlit
