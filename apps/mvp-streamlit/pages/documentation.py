"""
Documentation & Aide - Page dédiée aux exemples et FAQ
"""

import streamlit as st

# NOTE: Ne PAS appeler st.set_page_config() dans les pages du dossier pages/
# La config est héritée du script principal (app.py)

st.title("📚 Documentation & Aide - SaaS Planz")
st.markdown("**Guide complet avec exemples pratiques et réponses aux questions fréquentes**")
st.divider()

# ============================================================================
# SECTION 1: EXEMPLES PRATIQUES
# ============================================================================

st.header("💡 Exemples Pratiques")
st.markdown("Voici des exemples concrets pour comprendre comment remplir vos CSV.")

# Exemple 1: Simple
with st.expander("📘 **Exemple Simple** - Un élève avec disponibilités basiques", expanded=False):
    st.markdown("### Cas d'usage")
    st.markdown("""
    **Alice** veut **2 cours par semaine** et est disponible:
    - **Lundi** : 08:00 à 12:00
    - **Mercredi** : 09:00 à 11:00
    """)
    
    st.markdown("### Correspondance CSV")
    st.code("""nom,sessions_par_semaine,lundi_debut,lundi_fin,mardi_debut,mardi_fin,mercredi_debut,mercredi_fin,jeudi_debut,jeudi_fin,vendredi_debut,vendredi_fin,samedi_debut,samedi_fin,groupe_lie,notes
Alice,2,08:00,12:00,,,09:00,11:00,,,,,,,,Débutante""", language="csv")
    
    st.info("💡 **Points clés:**\n- `sessions_par_semaine` = 2 signifie qu'Alice aura **exactement 2 cours** par semaine\n- Les cellules vides (`,,,`) indiquent pas de disponibilité ce jour-là\n- Format horaire: **HH:MM** avec minutes en :00 ou :30 uniquement")

# Exemple 2: Groupe lié
with st.expander("📗 **Exemple Moyen** - Deux élèves voulant cours ensemble (groupe lié)", expanded=False):
    st.markdown("### Cas d'usage")
    st.markdown("""
    **Sophie** et **Julie** veulent **2 cours par semaine ensemble** (même créneau).
    
    Disponibilités communes:
    - **Lundi** : 09:00 à 12:00
    - **Mardi** : 09:00 à 11:00
    - **Jeudi** : 14:00 à 17:00
    """)
    
    st.markdown("### Correspondance CSV")
    st.code("""nom,sessions_par_semaine,lundi_debut,lundi_fin,mardi_debut,mardi_fin,mercredi_debut,mercredi_fin,jeudi_debut,jeudi_fin,vendredi_debut,vendredi_fin,samedi_debut,samedi_fin,groupe_lie,notes
Sophie,2,09:00,12:00,09:00,11:00,,,14:00,17:00,,,,,Julie,Débutante motivée
Julie,2,09:00,12:00,09:00,11:00,,,14:00,17:00,,,,,Sophie,Débutante motivée""", language="csv")
    
    st.info("💡 **Points clés:**\n- Colonne `groupe_lie`: Sophie met **\"Julie\"** et Julie met **\"Sophie\"**\n- Les deux élèves doivent avoir **mêmes disponibilités** pour être placées ensemble\n- L'algorithme garantit qu'elles seront toujours dans le même cours")

# Exemple 3: Complexe avec :30
with st.expander("📙 **Exemple Complexe** - Horaires variés avec demi-heures", expanded=False):
    st.markdown("### Cas d'usage")
    st.markdown("""
    **Camille** veut **3 cours par semaine** avec horaires variés incluant des demi-heures (`:30`).
    
    Disponibilités:
    - **Lundi** : 08:30 à 12:00
    - **Mardi** : 08:30 à 12:00
    - **Mercredi** : 08:30 à 12:00
    - **Vendredi** : 09:00 à 13:00
    - **Samedi** : 09:00 à 12:00
    """)
    
    st.markdown("### Correspondance CSV")
    st.code("""nom,sessions_par_semaine,lundi_debut,lundi_fin,mardi_debut,mardi_fin,mercredi_debut,mercredi_fin,jeudi_debut,jeudi_fin,vendredi_debut,vendredi_fin,samedi_debut,samedi_fin,groupe_lie,notes
Camille,3,08:30,12:00,08:30,12:00,08:30,12:00,,,09:00,13:00,09:00,12:00,,Avancée très flexible""", language="csv")
    
    st.info("💡 **Points clés:**\n- Les heures peuvent se terminer par `:00` ou `:30` (ex: 08:30, 09:00, 17:30)\n- `sessions_par_semaine` = 3 signifie Camille aura **3 cours différents** dans la semaine\n- Plus les disponibilités sont larges, plus l'algorithme a de flexibilité")

# Exemple 4: Créneaux récurrents
with st.expander("📕 **Exemple Créneaux Récurrents** - Cours fixes garantis", expanded=False):
    st.markdown("### Cas d'usage")
    st.markdown("""
    **Vincent** veut **TOUJOURS** être le **mardi 17:00-18:00** (créneau fixe garanti).
    
    Ce créneau sera **obligatoirement** dans le planning, contrairement aux disponibilités qui sont des plages flexibles.
    """)
    
    st.markdown("### Correspondance CSV (fichier séparé)")
    st.code("""nom,jour,heure_debut,heure_fin
Vincent,mardi,17:00,18:00
Hugo,lundi,08:00,09:00
Juliette,lundi,08:00,09:00""", language="csv")
    
    st.info("💡 **Points clés:**\n- Format plus simple: nom, jour, heure_debut, heure_fin\n- Ces créneaux sont **garantis** et figés dans le planning\n- Plusieurs élèves peuvent partager le même créneau (ex: Hugo et Juliette le lundi 08:00)")
    
    st.warning("⚠️ **Différence importante:**\n- **Disponibilités** = plages horaires où l'élève *peut* être placé (flexible)\n- **Créneaux récurrents** = cours *fixes* garantis (non flexible)")

st.divider()

# ============================================================================
# SECTION 2: FAQ
# ============================================================================

st.header("❓ FAQ - Questions Fréquentes")

with st.expander("❓ **Pourquoi un élève n'est pas placé ?**", expanded=False):
    st.markdown("""
    Un élève peut ne pas être placé pour plusieurs raisons:
    
    **1. Disponibilités insuffisantes**
    - L'élève a demandé 3 cours/semaine mais n'a fourni que 2 créneaux disponibles
    - Les créneaux disponibles sont trop courts (ex: 30 minutes alors qu'un cours dure 1h)
    
    **2. Conflits avec groupes liés**
    - L'élève veut être avec un partenaire (`groupe_lie`) mais leurs disponibilités ne se chevauchent pas
    - Le groupe lié a des contraintes incompatibles
    
    **3. Créneaux déjà réservés**
    - Les créneaux disponibles de l'élève sont bloqués par vos créneaux personnels (Étape 2)
    - Les créneaux sont occupés par d'autres créneaux récurrents
    
    **4. Saturation du planning**
    - Tous les créneaux disponibles sont déjà remplis par d'autres élèves
    
    **💡 Solution:** Vérifiez les suggestions dans la section "Élèves Non Placés" qui propose des actions concrètes.
    """)

with st.expander("❓ **Que signifie 'sessions_par_semaine' ?**", expanded=False):
    st.markdown("""
    La colonne `sessions_par_semaine` indique le **nombre EXACT de cours** que l'élève souhaite par semaine.
    
    **Exemples:**
    - `sessions_par_semaine = 1` → L'élève aura **1 cours par semaine**
    - `sessions_par_semaine = 2` → L'élève aura **2 cours par semaine** (le plus courant)
    - `sessions_par_semaine = 3` → L'élève aura **3 cours par semaine**
    
    **⚠️ Important:**
    - L'algorithme essaiera de placer l'élève **exactement ce nombre de fois**
    - Si impossible (disponibilités insuffisantes, conflits), l'élève sera marqué "non placé"
    - L'élève ne sera **jamais** placé moins ou plus que le nombre demandé
    
    **💡 Astuce:** Assurez-vous que les disponibilités couvrent suffisamment de créneaux pour atteindre le nombre demandé.
    """)

with st.expander("❓ **Comment créer un groupe lié ?**", expanded=False):
    st.markdown("""
    Un **groupe lié** permet à deux élèves d'être **toujours ensemble** dans les mêmes cours.
    
    **Étapes:**
    1. Dans la colonne `groupe_lie`, l'élève A met le nom de l'élève B
    2. Dans la colonne `groupe_lie`, l'élève B met le nom de l'élève A
    3. Les deux élèves doivent avoir les **mêmes disponibilités** et le **même nombre de sessions_par_semaine**
    
    **Exemple concret:**
    ```csv
    nom,sessions_par_semaine,lundi_debut,lundi_fin,...,groupe_lie
    Sophie,2,09:00,12:00,...,Julie
    Julie,2,09:00,12:00,...,Sophie
    ```
    
    **💡 Points clés:**
    - Les noms dans `groupe_lie` doivent correspondre **exactement** aux noms de la colonne `nom`
    - Les deux élèves seront toujours placés ensemble (même créneau, même cours)
    - Si un des deux ne peut pas être placé, l'autre ne le sera pas non plus
    
    **⚠️ Limitation:** Actuellement, seuls les **groupes de 2** sont supportés (pas de groupes de 3+).
    """)

with st.expander("❓ **Que faire si le planning ne me convient pas ?**", expanded=False):
    st.markdown("""
    Si le planning généré ne vous satisfait pas, voici les actions possibles:
    
    **1. Ajuster les disponibilités élèves**
    - Élargir les plages horaires disponibles
    - Ajouter des jours supplémentaires
    - Modifier les heures de début/fin pour plus de flexibilité
    
    **2. Ajouter des créneaux récurrents**
    - Fixer certains élèves sur des créneaux spécifiques
    - Garantir que certains cours tombent toujours au même moment
    
    **3. Modifier vos créneaux réservés (Étape 2)**
    - Réduire le nombre de créneaux bloqués pour libérer plus de place
    - Déplacer vos créneaux personnels sur des horaires moins demandés
    
    **4. Ajuster `sessions_par_semaine`**
    - Réduire le nombre de cours demandés par certains élèves si trop de demande
    - Augmenter pour des élèves sous-utilisés
    
    **💡 Astuce:** Consultez la section "Avertissements et Optimisations" qui suggère des améliorations possibles.
    """)

with st.expander("❓ **Différence entre disponibilités et créneaux récurrents ?**", expanded=False):
    st.markdown("""
    Ces deux fichiers CSV ont des rôles très différents:
    
    ### 📄 Disponibilités (fichier principal)
    - **Rôle:** Indiquer les **plages horaires flexibles** où l'élève *peut* être placé
    - **Flexibilité:** L'algorithme **choisit** les meilleurs créneaux dans ces plages
    - **Exemple:** Alice dispo lundi 08:00-12:00 → elle sera placée à un moment dans cette plage (ex: 09:00-10:00)
    
    ### 📌 Créneaux Récurrents (fichier optionnel)
    - **Rôle:** Définir des **cours fixes garantis** (toujours au même moment)
    - **Flexibilité:** **Aucune** - le créneau est figé et obligatoire
    - **Exemple:** Vincent veut **toujours** mardi 17:00-18:00 → ce créneau sera dans le planning, garanti
    
    **Quand utiliser quoi ?**
    
    | Situation | Fichier à utiliser |
    |-----------|-------------------|
    | Élève flexible sur les horaires | **Disponibilités** uniquement |
    | Élève veut cours régulier mais pas forcément même heure chaque semaine | **Disponibilités** uniquement |
    | Élève veut **toujours** le même créneau (ex: mardi 17h) | **Créneaux récurrents** |
    | Coach veut garantir un groupe à une heure fixe | **Créneaux récurrents** |
    
    **💡 Bon à savoir:** Vous pouvez combiner les deux ! Un élève peut avoir un créneau récurrent **et** des disponibilités pour ses autres cours.
    """)

with st.expander("❓ **Comment bloquer mes créneaux personnels ?**", expanded=False):
    st.markdown("""
    Pour éviter que l'algorithme ne génère des cours sur vos créneaux personnels (entraînements, rendez-vous, etc.):
    
    **Étapes:**
    1. Allez à l'**Étape 2** de l'interface principale
    2. Sélectionnez le **jour** et les **heures début/fin** du créneau à bloquer
    3. Cliquez sur **"➕ Ajouter Créneau Réservé"**
    4. Le créneau apparaît dans la liste et peut être supprimé (🗑️) si besoin
    
    **Exemple:**
    - Vous avez un entraînement personnel le **jeudi 18:00-19:00**
    - Ajoutez ce créneau → aucun élève ne sera placé à ce moment-là
    
    **💡 Astuce:** 
    - Vous pouvez ajouter autant de créneaux réservés que nécessaire
    - Les créneaux sont sauvegardés pendant votre session
    - Pensez à les re-saisir si vous rechargez la page
    
    **⚠️ Note:** Ces créneaux réservés sont **différents** des créneaux récurrents:
    - **Créneaux réservés (Étape 2):** Bloquent des créneaux pour vous (coach)
    - **Créneaux récurrents (CSV):** Garantissent des cours fixes pour certains élèves
    """)

st.divider()

# ============================================================================
# SECTION 3: RETOUR PAGE PRINCIPALE
# ============================================================================

st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("### 🏠 Prêt à générer votre planning ?")
    if st.button("↩️ Retour à la page principale", type="primary", use_container_width=True):
        st.switch_page("app.py")
