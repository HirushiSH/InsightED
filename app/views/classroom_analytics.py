import streamlit as st
import pandas as pd
import os
import joblib
import matplotlib.pyplot as plt

# ============================================================
# MODEL PATHS
# ============================================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

PREPROCESSOR_PATH = os.path.join(
    PROJECT_ROOT,
    "models",
    "features.pkl"
)

MODEL_PATH = os.path.join(
    PROJECT_ROOT,
    "models",
    "logistic_regression_model.pkl"
)


# ============================================================
# LOAD MODEL
# ============================================================

preprocessor = joblib.load(PREPROCESSOR_PATH)
model = joblib.load(MODEL_PATH)


# ============================================================
# CLASSROOM ANALYTICS
# ============================================================

def render_classroom_analytics():

    # ========================================================
    # PAGE HEADER
    # ========================================================

    st.caption("CLASSROOM OVERVIEW")

    st.title("Understand your class at a glance")

    st.write(
        "Review overall class performance and identify "
        "students who may need additional attention "
        "using the trained machine-learning model."
    )

    st.divider()


    # ========================================================
    # CHECK DATASET
    # ========================================================

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


    # ========================================================
    # GENERATE ML PREDICTIONS FOR WHOLE CLASS
    # ========================================================

    try:

        # ----------------------------------------------------
        # Prepare student data
        # ----------------------------------------------------

        prediction_input = df.drop(
            columns=["Student ID", "G3"],
            errors="ignore"
        ).copy()


        # ----------------------------------------------------
        # Create Grade Momentum
        # Same feature used by Decision Support
        # ----------------------------------------------------

        if (
            "G1" in prediction_input.columns
            and "G2" in prediction_input.columns
        ):

            prediction_input["Grade_Momentum"] = (
                prediction_input["G2"]
                - prediction_input["G1"]
            )


        # ----------------------------------------------------
        # Apply SAME preprocessing pipeline
        # ----------------------------------------------------

        X_class = preprocessor.transform(
            prediction_input
        )


        # ----------------------------------------------------
        # ML probability
        # ----------------------------------------------------

        risk_probabilities = model.predict_proba(
            X_class
        )[:, 1]


        # ----------------------------------------------------
        # ML predicted class
        # ----------------------------------------------------

        predictions = model.predict(
            X_class
        )


        # ----------------------------------------------------
        # Add ML results to classroom dataframe
        # ----------------------------------------------------

        students = df.copy()

        students["Risk Probability"] = (
            risk_probabilities
        )

        students["ML Prediction"] = predictions


        # ----------------------------------------------------
        # Convert probability into attention level
        # ----------------------------------------------------

        def determine_attention(probability):

            if probability >= 0.70:

                return "High attention"

            elif probability >= 0.40:

                return "Moderate attention"

            else:

                return "Lower attention"


        students["Attention"] = (
            students["Risk Probability"]
            .apply(determine_attention)
        )


    except Exception as e:

        st.error(
            "Unable to generate classroom ML predictions."
        )

        st.exception(e)

        return


    # ========================================================
    # BASIC INFORMATION
    # ========================================================

    total_students = len(students)


    # ========================================================
    # CLASS PERFORMANCE
    # ========================================================

    if "G3" in students.columns:

        performance_column = "G3"

    elif "G2" in students.columns:

        performance_column = "G2"

    else:

        performance_column = None


    if performance_column:

        class_average = students[
            performance_column
        ].mean()

    else:

        class_average = None


    # ========================================================
    # ML RISK COUNTS
    # ========================================================

    high_attention_count = (
        students["Attention"] == "High attention"
    ).sum()

    moderate_attention_count = (
        students["Attention"] == "Moderate attention"
    ).sum()

    students_needing_attention = (
        high_attention_count
        + moderate_attention_count
    )


    # ========================================================
    # CLASS SUMMARY
    # ========================================================

    st.caption("CLASS SUMMARY")

    st.subheader("Student overview")

    with st.container(border=True, key="cra_panel_summary"):

        col1, col2, col3, col4 = st.columns(4)


        # --------------------------------------------------------
        # TOTAL STUDENTS
        # --------------------------------------------------------

        with col1:

            st.metric(
                "Total students",
                f"{total_students:,}"
            )


        # --------------------------------------------------------
        # CLASS AVERAGE
        # --------------------------------------------------------

        with col2:

            if class_average is not None:

                st.metric(
                    "Class average",
                    f"{class_average:.1f}"
                )

            else:

                st.metric(
                    "Class average",
                    "N/A"
                )


        # --------------------------------------------------------
        # STUDENTS NEEDING ATTENTION
        # NOW BASED ON ML
        # --------------------------------------------------------

        with col3:

            st.metric(
                "Students needing attention",
                f"{students_needing_attention:,}"
            )


        # --------------------------------------------------------
        # OVERALL PERFORMANCE
        # --------------------------------------------------------

        with col4:

            if class_average is not None:

                if class_average >= 12:

                    overall_performance = "Strong"

                elif class_average >= 10:

                    overall_performance = "Moderate"

                else:

                    overall_performance = "Needs attention"

                st.metric(
                    "Overall performance",
                    overall_performance
                )

            else:

                st.metric(
                    "Overall performance",
                    "N/A"
                )


    # ========================================================
    # ML RISK SUMMARY
    # ========================================================

    st.divider()

    st.caption("MACHINE-LEARNING RISK OVERVIEW")

    st.subheader("Predicted student risk")

    risk_col1, risk_col2, risk_col3 = st.columns(3)


    with risk_col1:

        with st.container(border=True, key="cra_risk_high"):

            st.metric(
                "High attention",
                f"{high_attention_count:,}"
            )


    with risk_col2:

        with st.container(border=True, key="cra_risk_moderate"):

            st.metric(
                "Moderate attention",
                f"{moderate_attention_count:,}"
            )


    with risk_col3:

        lower_attention_count = (
            students["Attention"]
            == "Lower attention"
        ).sum()

        with st.container(border=True, key="cra_risk_low"):

            st.metric(
                "Lower attention",
                f"{lower_attention_count:,}"
            )

    
    # RISK DISTRIBUTION PIE CHART

    # ========================================================
    # CLASS PERFORMANCE + RISK DISTRIBUTION
    # ========================================================

    st.divider()

    left_col, right_col = st.columns(2)

    # ========================================================
    # LEFT — CLASS PERFORMANCE
    # ========================================================

    with left_col:

        with st.container(border=True, key="cra_panel_performance"):

            st.caption("PERFORMANCE OVERVIEW")
            st.subheader("Class performance")

            if performance_column:

                st.write(
                    f"Performance overview based on "
                    f"**{performance_column}**."
                )

                performance_data = (
                    students[performance_column]
                    .dropna()
                    .value_counts()
                    .sort_index()
                )

                st.bar_chart(
                    performance_data,
                    use_container_width=True
                )

            else:

                st.info(
                    "A performance measure such as G3 "
                    "is required."
                )


    # ========================================================
    # RIGHT — ML RISK DISTRIBUTION
    # ========================================================

    with right_col:

        with st.container(border=True, key="cra_panel_risk_dist"):

            st.caption("RISK DISTRIBUTION")
            st.subheader("Predicted student risk")

            risk_values = [
                high_attention_count,
                moderate_attention_count,
                lower_attention_count
            ]

            risk_labels = [
                "High attention",
                "Moderate attention",
                "Lower attention"
            ]

            risk_colors = [
                "#DC2626",
                "#D97706",
                "#16A34A",
            ]

            fig, ax = plt.subplots(figsize=(4.5, 4.5))

            fig.patch.set_alpha(0)
            ax.set_facecolor("none")

            ax.pie(
                risk_values,
                labels=risk_labels,
                colors=risk_colors,
                autopct="%1.1f%%",
                startangle=90,
                wedgeprops={"edgecolor": "white", "linewidth": 1.5},
                textprops={"fontsize": 9},
            )

            ax.set_title(
                "Predicted Student Risk Distribution",
                fontsize=11,
                fontweight="bold",
            )

            st.pyplot(
                fig,
                use_container_width=False,
                transparent=True,
            )

            plt.close(fig)

            st.caption(
                "Risk levels are generated using the trained "
                "Logistic Regression model."
            )

    # ========================================================
    # STUDENTS REQUIRING ATTENTION
    # ========================================================

    st.divider()

    st.caption("STUDENT RISK LIST")

    st.subheader(
        "Students requiring attention"
    )

    with st.container(border=True, key="cra_panel_student_list"):

        # ========================================================
        # FILTER
        # ========================================================

        filter_option = st.selectbox(
            "Student risk filter",
            [
                "All students",
                "High attention",
                "Moderate attention",
                "Lower attention"
            ],
            label_visibility="collapsed"
        )


        filtered_students = students.copy()


        if filter_option != "All students":

            filtered_students = students[
                students["Attention"] == filter_option
            ]


        # ========================================================
        # DISPLAY TABLE
        # ========================================================

        display_columns = []


        if "Student ID" in filtered_students.columns:

            display_columns.append(
                "Student ID"
            )


        display_columns.append(
            "Attention"
        )


        display_columns.append(
            "Risk Probability"
        )


        if "G1" in filtered_students.columns:

            display_columns.append("G1")


        if "G2" in filtered_students.columns:

            display_columns.append("G2")


        if "G3" in filtered_students.columns:

            display_columns.append("G3")


        display_df = filtered_students[
            display_columns
        ].copy()


        # ========================================================
        # FORMAT RISK PROBABILITY
        # ========================================================

        display_df["Risk Probability"] = (
            display_df["Risk Probability"]
            .apply(lambda x: f"{x:.1%}")
        )


        # ========================================================
        # RENAME COLUMNS
        # ========================================================

        display_df = display_df.rename(
            columns={
                "Risk Probability":
                    "Predicted Risk"
            }
        )


        # ========================================================
        # SHOW TABLE
        # ========================================================

        if display_df.empty:

            st.info(
                "No students match the selected "
                "risk level."
            )

        else:

            st.write(
                f"{len(display_df):,} student(s) shown."
            )


            event = st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True,
                on_select="rerun",
                selection_mode="single-row",
                key="classroom_student_table",
            )


            # ====================================================
            # OPEN DECISION SUPPORT
            # ====================================================

            if event.selection.rows:

                selected_row = (
                    event.selection.rows[0]
                )


                selected_student_id = str(
                    display_df.iloc[
                        selected_row
                    ]["Student ID"]
                )


                st.session_state[
                    "selected_student_id"
                ] = selected_student_id


                st.session_state[
                    "navigate_to"
                ] = "Decision Support"


                st.rerun()


    # ========================================================
    # FOOTNOTE
    # ========================================================

    st.divider()

    st.caption(
        "Risk levels are generated by the trained "
        "machine-learning model and are intended to "
        "support lecturer review rather than provide "
        "a final academic judgment."
    )