"""
Streamlit UI for SaaS Planz scheduling system.
Local MVP interface for Tony to generate schedules.
"""

try:
    import streamlit as st
except ImportError:
    st = None

from pathlib import Path
import tempfile
from datetime import time

from core.parser import parse_csv, ParseError
from core.scheduler import generate_schedule
from core.formatter import to_json, to_markdown
from core.models import Slot


# Page config
if st:
    st.set_page_config(
        page_title="SaaS Planz - Génération Planning",
        page_icon="📅",
        layout="wide"
    )


def main():
    """Main Streamlit app."""
    if st is None:
        print("Streamlit not installed. Please run: pip install streamlit")
        return
    
    # Title
    st.title("📅 SaaS Planz - Génération Automatique de Planning")
    st.markdown("**Génération intelligente de planning sportif avec contraintes multiples**")
    st.divider()
    
    # Sidebar - Templates download
    with st.sidebar:
        st.header("📥 Télécharger Templates")
        
        st.subheader("1. Template Disponibilités")
        st.markdown("*CSV principal avec les disponibilités des élèves*")
        
        template_path = Path("docs/examples/template-disponibilites.csv")
        if template_path.exists():
            with open(template_path, "r") as f:
                st.download_button(
                    label="📄 Télécharger Template Disponibilités",
                    data=f.read(),
                    file_name="template-disponibilites.csv",
                    mime="text/csv"
                )
        
        st.divider()
        
        st.subheader("2. Template Créneaux Récurrents")
        st.markdown("*CSV optionnel pour les créneaux fixes*")
        
        recurring_template_path = Path("docs/examples/template-recurring-slots.csv")
        if recurring_template_path.exists():
            with open(recurring_template_path, "r") as f:
                st.download_button(
                    label="📄 Télécharger Template Récurrents",
                    data=f.read(),
                    file_name="template-recurring-slots.csv",
                    mime="text/csv"
                )
        
        st.divider()
        
        st.markdown("### 📚 Documentation")
        st.markdown("[Guide d'utilisation](docs/examples/README-template.md)")
        st.markdown("[FAQ & Support](#)")
    
    # Main area - File upload
    st.header("📤 Étape 1: Charger les Fichiers")
    
    # Info box about sessions_par_semaine
    st.info("""
    💡 **Colonne obligatoire dans le CSV :** `sessions_par_semaine`
    
    Indiquez combien de cours chaque élève souhaite par semaine :
    - **1 cours/semaine** : élève occasionnel
    - **2 cours/semaine** : élève régulier (le plus courant)
    - **3+ cours/semaine** : élève intensif
    
    ⚠️ **Important :** L'algorithme placera chaque élève **exactement** ce nombre de fois. 
    Si impossible, l'élève sera marqué "non placé" avec explication.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Disponibilités Élèves (requis)")
        availability_file = st.file_uploader(
            "Charger le CSV des disponibilités",
            type=["csv"],
            key="availability"
        )
        
        # Preview and validation after upload
        if availability_file:
            import pandas as pd
            try:
                df = pd.read_csv(availability_file)
                st.success(f"✅ **{len(df)} élèves** chargés")
                
                # Check for sessions_par_semaine column
                if 'sessions_par_semaine' in df.columns:
                    total_sessions = int(df['sessions_par_semaine'].sum())
                    avg_sessions = df['sessions_par_semaine'].mean()
                    
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.metric("📊 Total cours à placer", total_sessions)
                    with col_b:
                        st.metric("📈 Moyenne par élève", f"{avg_sessions:.1f}")
                    
                    st.caption(f"~{total_sessions} cours de 1h à générer dans la semaine")
                    
                    # Show distribution
                    session_counts = df['sessions_par_semaine'].value_counts().sort_index()
                    st.write("**Répartition :**")
                    for sessions, count in session_counts.items():
                        st.write(f"- {int(sessions)} cours/semaine : {int(count)} élève(s)")
                    
                else:
                    st.error("❌ **Colonne 'sessions_par_semaine' manquante** dans le CSV")
                    st.warning("⚠️ Le CSV doit contenir cette colonne obligatoire. Utilisez le template fourni.")
                
                # Reset file pointer for later use
                availability_file.seek(0)
                
            except Exception as e:
                st.error(f"❌ Erreur lors de la lecture du CSV: {e}")
    
    with col2:
        st.subheader("Créneaux Récurrents (optionnel)")
        recurring_file = st.file_uploader(
            "Charger le CSV des créneaux récurrents",
            type=["csv"],
            key="recurring"
        )
        
        if recurring_file:
            import pandas as pd
            try:
                df_rec = pd.read_csv(recurring_file)
                st.success(f"✅ **{len(df_rec)} créneaux récurrents** chargés")
                
                # Show recurring slots preview
                if not df_rec.empty:
                    st.write("**Aperçu des récurrents :**")
                    # Group by slot to show multiple students on same slot
                    grouped = df_rec.groupby(['jour', 'heure_debut', 'heure_fin'])['nom'].apply(list).reset_index()
                    
                    for _, row in grouped.head(3).iterrows():
                        students = ', '.join(row['nom'])
                        st.write(f"- {row['jour']} {row['heure_debut']}-{row['heure_fin']}: {students}")
                    if len(grouped) > 3:
                        st.caption(f"... et {len(grouped) - 3} autre(s) créneau(x)")
                
                # Reset file pointer
                recurring_file.seek(0)
                
            except Exception as e:
                st.error(f"❌ Erreur lors de la lecture du CSV récurrents: {e}")
    
    st.divider()
    
    # Coach reserved slots
    st.header("🚫 Étape 2: Bloquer vos Créneaux Personnels")
    st.markdown("*Sélectionnez les créneaux que vous souhaitez réserver (entraînements, rendez-vous, etc.)*")
    
    # Initialize session state for coach reserved slots
    if 'coach_reserved' not in st.session_state:
        st.session_state.coach_reserved = []
    
    # Simple UI for adding reserved slots
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        reserved_day = st.selectbox(
            "Jour",
            ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi"],
            key="reserved_day"
        )
    
    with col2:
        reserved_start_hour = st.selectbox("Heure début", list(range(6, 22)), key="reserved_start_hour")
        reserved_start_min = st.selectbox("Minute début", [0, 30], key="reserved_start_min")
    
    with col3:
        reserved_end_hour = st.selectbox("Heure fin", list(range(7, 23)), key="reserved_end_hour")
        reserved_end_min = st.selectbox("Minute fin", [0, 30], key="reserved_end_min")
    
    with col4:
        st.write("")  # Spacing
        if st.button("➕ Ajouter Créneau Réservé"):
            try:
                slot = Slot(
                    day=reserved_day,
                    start_time=time(reserved_start_hour, reserved_start_min),
                    end_time=time(reserved_end_hour, reserved_end_min),
                    is_recurring=False
                )
                
                if slot.is_valid():
                    st.session_state.coach_reserved.append(slot)
                    st.success(f"✅ Créneau ajouté: {reserved_day} {slot.start_time}-{slot.end_time}")
                else:
                    st.error("❌ Créneau invalide (durée doit être 1h, granularité :00 ou :30)")
            except Exception as e:
                st.error(f"❌ Erreur: {e}")
    
    # Display reserved slots
    if st.session_state.coach_reserved:
        st.write("**Créneaux réservés:**")
        for i, slot in enumerate(st.session_state.coach_reserved):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"{i+1}. {slot.day.capitalize()} {slot.start_time.strftime('%H:%M')}-{slot.end_time.strftime('%H:%M')}")
            with col2:
                if st.button("🗑️", key=f"delete_{i}"):
                    st.session_state.coach_reserved.pop(i)
                    st.rerun()
    
    st.divider()
    
    # Generate button
    st.header("⚡ Étape 3: Générer le Planning")
    
    if st.button("🚀 Générer Planning Automatique", type="primary", use_container_width=True):
        if not availability_file:
            st.error("❌ Veuillez charger le fichier des disponibilités")
            return
        
        with st.spinner("Génération du planning en cours..."):
            try:
                # Save uploaded files to temp
                with tempfile.NamedTemporaryFile(mode='wb', suffix='.csv', delete=False) as tmp_avail:
                    tmp_avail.write(availability_file.getvalue())
                    avail_path = tmp_avail.name
                
                recurring_path = None
                if recurring_file:
                    with tempfile.NamedTemporaryFile(mode='wb', suffix='.csv', delete=False) as tmp_rec:
                        tmp_rec.write(recurring_file.getvalue())
                        recurring_path = tmp_rec.name
                
                # Parse students
                students = parse_csv(avail_path)
                st.success(f"✅ {len(students)} élèves chargés")
                
                # Generate schedule
                result = generate_schedule(
                    students=students,
                    recurring_slots_path=recurring_path,
                    coach_reserved_slots=st.session_state.coach_reserved
                )
                
                # Store result in session
                st.session_state.schedule_result = result
                
                # Display success
                st.success("✅ Planning généré avec succès!")
                
                # Display summary
                st.subheader("📊 Résumé")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Cours planifiés", len(result.schedule))
                with col2:
                    st.metric("Élèves placés", result.metadata.get("placed_students", 0))
                with col3:
                    st.metric("Élèves non placés", len(result.unplaced))
                
                if result.is_complete():
                    st.success("🎉 Tous les élèves ont été placés!")
                else:
                    st.warning(f"⚠️ Solution partielle: {len(result.unplaced)} élève(s) non placé(s)")
                
            except ParseError as e:
                st.error(f"❌ Erreur de parsing CSV: {e}")
            except Exception as e:
                st.error(f"❌ Erreur: {e}")
                import traceback
                st.code(traceback.format_exc())
    
    # Display results if available
    if 'schedule_result' in st.session_state:
        st.divider()
        st.header("📅 Résultats")
        
        result = st.session_state.schedule_result
        
        # Schedule display
        st.subheader("Planning Hebdomadaire")
        
        # Group by day
        days_order = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi"]
        schedule_by_day = {day: [] for day in days_order}
        
        for cls in result.schedule:
            schedule_by_day[cls.slot.day].append(cls)
        
        # Display each day
        for day in days_order:
            classes = schedule_by_day[day]
            if not classes:
                continue
            
            with st.expander(f"**{day.capitalize()}** ({len(classes)} cours)", expanded=True):
                for cls in sorted(classes, key=lambda c: c.slot.start_time):
                    status_icon = {"locked": "🔒", "proposed": "✅", "needs_validation": "⚠️"}.get(cls.status.value, "❓")
                    st.write(
                        f"{status_icon} **{cls.slot.start_time.strftime('%H:%M')}-{cls.slot.end_time.strftime('%H:%M')}** "
                        f"- {', '.join(cls.students)} ({len(cls.students)} élèves)"
                    )
        
        # Warnings and Optimizations
        if result.warnings:
            st.subheader("⚠️ Avertissements et Optimisations Possibles")
            st.info(
                f"💡 {len(result.warnings)} créneau(x) peut/peuvent être optimisé(s) "
                f"en ajoutant d'autres étudiants disponibles."
            )
            
            for warning in result.warnings:
                if warning["type"] == "single_student_recurring":
                    with st.expander(f"🔍 Créneau à optimiser : {warning['slot']}"):
                        st.write(f"**Étudiant actuel :** {warning['student']}")
                        st.warning(warning['message'])
                        
                        if warning.get("suggestions"):
                            st.write("**Suggestions d'optimisation :**")
                            for suggestion in warning["suggestions"]:
                                st.write(f"- {suggestion}")
        
        # Unplaced students
        if result.unplaced:
            st.subheader("⚠️ Élèves Non Placés")
            
            # Show overall stats if students available
            if 'students' in st.session_state:
                students_list = st.session_state.students
                total_requested = sum(s.sessions_per_week for s in students_list)
                total_placed_sessions = len(result.schedule)
                st.caption(f"📊 Cours placés : {total_placed_sessions} / {total_requested} demandés ({total_placed_sessions/total_requested*100:.0f}%)")
            
            for unplaced in result.unplaced:
                with st.expander(f"**{unplaced.student}** - {unplaced.reason}"):
                    # Show requested sessions for context
                    if 'students' in st.session_state:
                        student_obj = next((s for s in st.session_state.students if s.name == unplaced.student), None)
                        if student_obj:
                            st.info(f"📌 Demandait **{student_obj.sessions_per_week} cours/semaine**")
                    
                    if unplaced.conflicts:
                        st.write("**Conflits:**")
                        for conflict in unplaced.conflicts:
                            st.write(f"- {conflict}")
                    
                    if unplaced.suggestions:
                        st.write("**Suggestions:**")
                        for suggestion in unplaced.suggestions:
                            st.write(f"- {suggestion}")
        
        # Download buttons
        st.divider()
        st.subheader("💾 Télécharger les Résultats")
        
        col1, col2 = st.columns(2)
        
        with col1:
            json_data = to_json(result)
            import json
            st.download_button(
                label="📥 Télécharger JSON",
                data=json.dumps(json_data, indent=2, ensure_ascii=False),
                file_name=f"planning_{availability_file.name.replace('.csv', '')}.json",
                mime="application/json"
            )
        
        with col2:
            markdown_data = to_markdown(result)
            st.download_button(
                label="📥 Télécharger Markdown",
                data=markdown_data,
                file_name=f"planning_{availability_file.name.replace('.csv', '')}.md",
                mime="text/markdown"
            )


if __name__ == "__main__":
    main()
