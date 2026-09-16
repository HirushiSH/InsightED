import streamlit as st


def render_home():

    # A keyed container lets layout.py scope the "equal height/width
    # card" CSS to just this page, without affecting other pages.
    with st.container(key="home_page"):

        # =========================================================
        # HERO
        # =========================================================

        st.markdown(
            "##### AI-POWERED ACADEMIC DECISION SUPPORT"
        )

        st.title("Understand student risk. Take meaningful action.")

        st.write(
            "InsightED helps lecturers identify students who may require "
            "academic support, understand the factors behind each prediction, "
            "and translate model insights into actionable pedagogical "
            "interventions."
        )

        

        # =========================================================
        # GET STARTED 
        # =========================================================
        
        
        st.subheader("Ready to analyse a class?")
        
        st.markdown(
            '<div class="get-started-desc">'
            'Open <strong>Data Management</strong> page '
            'to load student data and begin analysis.'
            '</div>',
            unsafe_allow_html=True,
        )
        
        st.markdown("")
        
        left_col, _, _ = st.columns([1, 1, 1])
        
        with left_col:
            if st.button(
                "Get Started",
                key="home_start_data_management",
                type="primary",
                use_container_width=True,
            ):
                st.session_state["navigate_to"] = "Data Management"
                st.rerun()

        st.markdown("---")

        # =========================================================
        # ABOUT
        # =========================================================

        st.caption("ABOUT INSIGHTED")

        st.header("A decision-support system for student success")

        st.write(
            "From prediction to explanation to intervention — InsightED "
            "connects the complete academic risk-analysis workflow."
        )

        st.markdown("")

        about_cards = [
            (
                "📊",
                "Predict Academic Risk",
                "Machine learning analyses student academic characteristics "
                "to identify students who may require additional support.",
            ),
            (
                "🧠",
                "Explain Predictions",
                "Explainable AI identifies the factors that contributed "
                "to an individual student's predicted academic risk.",
            ),
            (
                "🎯",
                "Recommend Interventions",
                "Model explanations are translated into practical "
                "pedagogical actions that lecturers can evaluate and apply.",
            ),
        ]

        cols = st.columns(3)

        for col, (icon, title, description) in zip(cols, about_cards):
            with col:
                st.markdown(
                    f'<div class="feature-card">'
                    f'<div class="feature-card-icon">{icon}</div>'
                    f'<div class="feature-card-title">{title}</div>'
                    f'<div class="feature-card-desc">{description}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

        st.markdown("")
        st.markdown("---")

        # =========================================================
        # WORKFLOW
        # =========================================================

        st.caption("DECISION WORKFLOW")

        st.header("From student data to intervention")

        st.write(
            "InsightED follows a structured decision-support pipeline."
        )

        st.markdown("")

        workflow = [
            (
                "01",
                "Student Data",
                "Academic and behavioural indicators are provided to the system.",
            ),
            (
                "02",
                "ML Prediction",
                "The trained model estimates the probability of academic risk.",
            ),
            (
                "03",
                "XAI Explanation",
                "Important contributing factors are identified and explained.",
            ),
            (
                "04",
                "Intervention",
                "Recommendations are presented for lecturer review.",
            ),
        ]

        cols = st.columns(4)

        for col, (number, title, description) in zip(cols, workflow):
            with col:
                st.markdown(
                    f'<div class="workflow-card">'
                    f'<div class="workflow-step-number">STEP {number}</div>'
                    f'<div class="workflow-card-title">{title}</div>'
                    f'<div class="workflow-card-desc">{description}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

        st.markdown("")
        st.markdown("---")

        # =========================================================
        # SYSTEM STATUS
        # =========================================================

        st.markdown("SYSTEM STATUS")

        st.header("InsightED components")

        st.write(
            "Current application services available in the "
            "decision-support workflow."
        )

        st.markdown("")

        status_items = [
            (
                "ML Prediction Engine",
                "Logistic Regression · Random Forest · XGBoost",
            ),
            (
                "Explainable AI",
                "LIME-based local student explanations",
            ),
            (
                "Recommendation Engine",
                "Explanation-to-action translation",
            ),
            (
                "Human Feedback",
                "Lecturer evaluation and feedback adaptation",
            ),
        ]

        cols = st.columns(4)

        for col, (title, description) in zip(cols, status_items):
            with col:
                st.markdown(
                    f'<div class="status-pill-card">'
                    f'<div class="status-pill-title">'
                    f'<span class="status-pill-dot"></span>{title}'
                    f'</div>'
                    f'<div class="status-pill-desc">{description}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

        st.markdown("")
        st.markdown("---")

        