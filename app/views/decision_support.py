import streamlit as st
import pandas as pd
import os

from src.prediction_service import InsightEDPredictionService
from app.recommendation_engine import get_xai_recommendation

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

DECISION_LOG_FILE = os.path.join(
    PROJECT_ROOT,
    "lecturer_decision_log.csv"
)

# ============================================================
# CENTRALIZED ML + XAI SERVICE
# ============================================================

prediction_service = InsightEDPredictionService()


def render_decision_support():

    # ============================================================
    # PAGE HEADER
    # ============================================================

    st.caption("DECISION SUPPORT")

    st.title("Understand student risk and take action")

    st.write(
        "Review a student's academic situation, understand the "
        "main factors behind the result, and decide on an "
        "appropriate support action."
    )

    st.divider()

    # ============================================================
    # CHECK DATASET
    # ============================================================

    if "uploaded_dataset" not in st.session_state:

        st.info(
            "No student data is available yet. "
            "Please upload a dataset from Data Management first."
        )

        return

    df = st.session_state["uploaded_dataset"].copy()

    if df.empty:

        st.info(
            "There are no student records available."
        )

        return

    # SELECT STUDENT =======================================

    st.caption("STUDENT")

    st.subheader("Select a student")

    student_ids = (
        df["Student ID"]
        .astype(str)
        .tolist()
    )

    # Student selected from Classroom Overview
    classroom_student = st.session_state.get(
        "selected_student_id"
    )

    # Use classroom-selected student only when arriving here
    if classroom_student in student_ids:

        default_index = student_ids.index(
            classroom_student
        )

    else:

        default_index = 0

    selected_id = st.selectbox(
        "Student",
        student_ids,
        index=default_index,
        key="decision_support_student"
    )

    student = df[
        df["Student ID"].astype(str) == selected_id
    ].iloc[0]

    student_label = selected_id


    # STUDENT OVERVIEW
    # ============================================================

    st.divider()

    st.caption("STUDENT OVERVIEW")

    st.subheader(student_label)

    col1, col2, col3 = st.columns(3)

    with col1:

        if "G1" in df.columns:

            st.metric(
                "Earlier grade",
                f"{student['G1']:.1f}"
            )

        else:

            st.metric(
                "Earlier grade",
                "N/A"
            )

    with col2:

        if "G2" in df.columns:

            st.metric(
                "Recent grade",
                f"{student['G2']:.1f}"
            )

        else:

            st.metric(
                "Recent grade",
                "N/A"
            )

    with col3:

        if "G3" in df.columns:

            st.metric(
                "Final grade",
                f"{student['G3']:.1f}"
            )

        else:

            st.metric(
                "Final grade",
                "N/A"
            )


    # ============================================================
    # RISK STATUS — ACTUAL ML MODEL
    # ============================================================

    st.divider()

    st.caption("RISK STATUS")

    # ============================================================
    # CENTRALIZED ML PREDICTION
    # ============================================================

    # ============================================================
    # PREPARE SINGLE-STUDENT INPUT FOR ML PREDICTION
    # ============================================================

    student_input = student.to_frame().T.copy()

    # Keep Student ID only for display/tracking.
    # prediction_service removes it before ML processing.

    # Force numeric ML columns to numeric values
    numeric_columns = [
        "age",
        "Medu",
        "Fedu",
        "traveltime",
        "studytime",
        "failures",
        "famrel",
        "freetime",
        "goout",
        "Dalc",
        "Walc",
        "health",
        "absences",
        "G1",
        "G2",
        "G3"
    ]

    for column in numeric_columns:

        if column in student_input.columns:

            student_input[column] = pd.to_numeric(
                student_input[column],
                errors="coerce"
            )

    # Run the SAME centralized prediction pipeline
    prediction_result = prediction_service.predict(
        student_input
    )

    risk_probability = float(
        prediction_result["Risk_Probability"].iloc[0]
    )

    prediction_status = prediction_result[
        "AI_Status"
    ].iloc[0]

    # Convert probability into risk category
    if risk_probability >= 0.70:

        risk_level = "High attention"

        st.error(
            f"High attention — "
            f"{risk_probability:.1%} predicted risk"
        )

        risk_message = (
            "The trained machine-learning model predicts a high "
            "probability of academic risk."
        )

    elif risk_probability >= 0.40:

        risk_level = "Moderate attention"

        st.warning(
            f"Moderate attention — "
            f"{risk_probability:.1%} predicted risk"
        )

        risk_message = (
            "The trained machine-learning model identifies a "
            "moderate probability of academic risk."
        )

    else:

        risk_level = "Lower attention"

        st.success(
            f"Lower attention — "
            f"{risk_probability:.1%} predicted risk"
        )

        risk_message = (
            "The trained machine-learning model predicts a lower "
            "probability of academic risk."
        )

    st.write(risk_message)

    #st.caption(
    #    f"Model: Logistic Regression | "
    #    f"Predicted At-Risk probability: {risk_probability:.1%}"
    #)

    # EXPLAINABLE AI — LECTURER-FRIENDLY EXPLANATION
    # ============================================================

    st.divider()

    st.caption("EXPLAINABLE AI")

    st.subheader("Why is this student at risk?")

    st.write(
        "Identified the following factors as the "
        "main contributors to this student's predicted risk."
    )

    
    # CENTRALIZED LIME EXPLANATION
    
    # Use the original selected student input.
    # The prediction service performs preprocessing internally.
    lime_explanation = prediction_service.explain_student(
        student_input.copy(),
        0
    )

    explanation_list = lime_explanation.as_list()


    # ============================================================
    # HELPER — CONVERT TECHNICAL FEATURES TO SIMPLE LANGUAGE
    # ============================================================

    def make_lecturer_friendly(rule, weight, student):

        # Grade 2
        if "G2" in rule:

            if student["G2"] < 10:
                message = (
                    f"Recent academic performance is low "
                    f"(grade {student['G2']:.1f})."
                )

            elif student["G2"] < student["G1"]:
                message = (
                    f"Recent performance has declined from "
                    f"{student['G1']:.1f} to {student['G2']:.1f}."
                )

            else:
                message = (
                    f"Recent academic performance is "
                    f"{student['G2']:.1f}."
                )

        # Grade 1
        elif "G1" in rule:

            message = (
                f"Earlier academic performance was "
                f"{student['G1']:.1f}."
            )

        # Age
        elif "age" in rule.lower():

            message = (
                f"Student age ({student['age']}) "
                f"contributed to the assessment."
            )

        # Mother's job
        elif "Mjob" in rule:

            message = (
                "Family background information contributed "
                "slightly to the prediction."
            )

        # Generic fallback
        else:

            message = (
                "This student characteristic contributed "
                "to the prediction."
            )

        return message


    # ============================================================
    # DISPLAY TOP CONTRIBUTING FACTORS
    # ============================================================

    positive_factors = [
        (rule, weight)
        for rule, weight in explanation_list
        if weight > 0
    ]

    negative_factors = [
        (rule, weight)
        for rule, weight in explanation_list
        if weight < 0
    ]
    
    # ============================================================
    
    def render_xai_card(message, weight, positive=True):

        impact = abs(weight)

        if impact >= 0.35:
            strength = "Strong influence"
        elif impact >= 0.15:
            strength = "Moderate influence"
        else:
            strength = "Small influence"

        if positive:
            icon = '<i class="fa-solid fa-arrow-up" style="color:#D32F2F;"></i>'
            sign = ""
        else:
            icon = '<i class="fa-solid fa-arrow-down" style="color:#2E7D32;"></i>'
            sign = ""

        with st.container(border=True):

            col1, col2 = st.columns([5, 1])

            with col1:

                st.markdown(
                    f"""
                    <div style="font-weight: 700;">
                        {icon} {message}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                #st.caption("MODEL IMPACT")

                st.progress(
                    min(int(impact * 100), 100)
                )

                st.caption(
                    f"{strength}  •  {sign}{impact:.2f} influence"
                )

            with col2:

                st.markdown(
                    f"""
                    <div style="
                        text-align:right;
                        font-size:1.25rem;
                        font-weight:800;
                        margin-top:8px;
                    ">
                        {sign}{weight:.2f}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    # ============================================================
    # DISPLAY XAI CARDS
    # ============================================================

    risk_col, protective_col = st.columns(2)

    # ------------------------------------------------------------
    # INCREASING RISK
    # ------------------------------------------------------------

    with risk_col:

        st.markdown(
            '<h3 class="increasing-risk">Increasing Risk</h3>',
            unsafe_allow_html=True
        )
        if positive_factors:

            for rule, weight in positive_factors[:3]:

                message = make_lecturer_friendly(
                    rule,
                    weight,
                    student
                )

                render_xai_card(
                    message,
                    weight,
                    positive=True
                )

        else:

            st.success(
                "No major factors were identified as increasing risk."
            )


    # ------------------------------------------------------------
    # REDUCING RISK
    # ------------------------------------------------------------

    with protective_col:

        st.markdown(
            '<h3 class="reducing-risk">Reducing Risk</h3>',
            unsafe_allow_html=True
        )

        if negative_factors:

            for rule, weight in negative_factors[:3]:

                message = make_lecturer_friendly(
                    rule,
                    weight,
                    student
                )

                render_xai_card(
                    message,
                    weight,
                    positive=False
                )

        else:

            st.info(
                "No major factors were identified as reducing risk."
            )

# ============================================================
# INTERPRETATION
# ============================================================

    st.info(
        "💡 **How to interpret:** Factors in red increased "
        "the predicted risk, while factors in green reduced it. "
        "A larger impact indicates a stronger influence on the "
        "individual prediction."
    )

    #st.caption(
    #    "Explanation generated using LIME to identify factors "
    #    "influencing this individual prediction."
    #)

        
# -------XAI-DRIVEN RECOMMENDED SUPPORT ------

    st.divider()

    st.caption("RECOMMENDED SUPPORT")

    st.subheader("Suggested action")

    if risk_probability >= 0.40:

        recommendation = get_xai_recommendation(
            explanation_list
        )

    else:

        recommendation = (
            "No immediate intervention is indicated. "
            "Continue monitoring the student's academic progress."
        )

    with st.container(border=True):

        st.markdown(
            '<h3 style="font-size:1.05rem; font-weight:600; color:#2f6db3; margin-bottom:0.3rem;">'
            'AI-Generated Recommendation</h3>',
            unsafe_allow_html=True,
        )

        st.write(recommendation)

    #st.caption(
    #    "Recommendation generated from the student's "
    #    "local LIME explanation."
    #)

    # ============================================================
    # LECTURER DECISION
    # ============================================================

    st.divider()

    st.caption("LECTURER DECISION")

    st.subheader("What would you like to do?")

    selected_action = st.selectbox(
        "Support action",
        [
            recommendation,
            "Targeted academic support",
            "Monitor student progress",
            "Individual student follow-up",
            "No action at this time"
        ]
    )

    lecturer_note = st.text_area(
        "Lecturer note (optional)",
        placeholder=(
            "Add a short note about this student's situation..."
        )
    )

    if st.button(
        "Save Lecturer Decision",
        type="primary",
        use_container_width=True,
        key="save_lecturer_decision"
    ):

        decision_record = {
            "Timestamp": pd.Timestamp.now(),
            "Student_ID": student_label,
            "AI_Status": prediction_status,
            "Risk_Probability": risk_probability,
            "Risk_Level": risk_level,
            "Lecturer_Action": selected_action,
            "Lecturer_Note": lecturer_note,
        }

        try:

            pd.DataFrame(
                [decision_record]
            ).to_csv(
                DECISION_LOG_FILE,
                mode="a",
                header=not os.path.exists(DECISION_LOG_FILE),
                index=False
            )

            st.session_state["decision_record"] = decision_record

            st.success("Lecturer decision saved successfully.")

        except Exception as e:

            st.error("Unable to save the lecturer decision.")
            st.caption(str(e))

    # ============================================================
    # RECORDED DECISION
    # ============================================================

    if "decision_record" in st.session_state:

        st.divider()

        st.caption("RECORDED DECISION")

        record = st.session_state["decision_record"]

        record_df = pd.DataFrame(
            [record]
        )

        st.dataframe(
            record_df,
            use_container_width=True,
            hide_index=True
        )

    # ============================================================
    # LECTURER FEEDBACK
    # ============================================================

    st.divider()

    st.caption("LECTURER FEEDBACK")

    st.subheader(
        "Was the recommendation useful?"
    )

    st.write(
        "Your feedback helps evaluate whether the suggested "
        "intervention is appropriate for the student."
    )

    feedback = st.radio(
        "Your assessment",
        [
            "Useful",
            "Partially useful",
            "Not useful"
        ],
        horizontal=True
    )

    feedback_action = st.selectbox(
        "What should happen to the recommendation?",
        [
            "Accept recommendation",
            "Modify recommendation",
            "Reject recommendation",
            "No action required"
        ]
    )

    feedback_comment = st.text_area(
        "Lecturer comment",
        placeholder=(
            "Explain why the recommendation was useful, "
            "partially useful, or not suitable..."
        )
    )

    if st.button(
        "Submit lecturer feedback",
        type="primary",
        use_container_width=True,
        key="submit_lecturer_feedback"
    ):

        feedback_record = {
            "Timestamp": pd.Timestamp.now(),
            "Student_ID": student_label,
            "Recommendation": recommendation,
            "Lecturer_Feedback": feedback,
            "Feedback_Action": feedback_action,
            "Lecturer_Comment": feedback_comment,
            "Feedback_Processed": False
        }

        # Save permanently
        feedback_file = os.path.join(
            PROJECT_ROOT,
            "feedback_log.csv"
        )

        new_feedback_df = pd.DataFrame(
            [feedback_record]
        )

        new_feedback_df.to_csv(
            feedback_file,
            mode="a",
            header=not os.path.exists(feedback_file),
            index=False
        )

        # Update human-in-the-loop weights
        from app.recommendation_engine import (
            update_weights_from_feedback
        )

        update_weights_from_feedback()

        # Keep visible in current session
        if "lecturer_feedback" not in st.session_state:
            st.session_state["lecturer_feedback"] = []

        st.session_state["lecturer_feedback"].append(
            feedback_record
        )

        st.success(
            "Lecturer feedback has been recorded "
            "and the recommendation engine has been updated."
        )

    # ============================================================
    # FEEDBACK HISTORY
    # ============================================================

    if "lecturer_feedback" in st.session_state:

        feedback_records = st.session_state[
            "lecturer_feedback"
        ]

        if feedback_records:

            st.divider()

            st.caption("FEEDBACK HISTORY")

            st.subheader(
                "Recorded lecturer feedback"
            )

            feedback_df = pd.DataFrame(
                feedback_records
            )

            st.dataframe(
                feedback_df,
                use_container_width=True,
                hide_index=True
            )

    # ============================================================
    # RESEARCH NOTE
    # ============================================================

    #st.divider()

    #st.caption("EXPLAINABLE DECISION SUPPORT")

    #st.write(
    #    "InsightED connects academic-risk predictions with "
    #    "understandable explanations, actionable pedagogical "
    #    "recommendations, and lecturer feedback."
    #)
