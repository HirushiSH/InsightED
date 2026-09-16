import os
import pandas as pd


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

LOG_FILE = os.path.join(
    PROJECT_ROOT,
    "feedback_log.csv"
)

WEIGHTS_FILE = os.path.join(
    PROJECT_ROOT,
    "feature_weights.csv"
)


# ============================================================
# 1. DEFAULT FEATURE WEIGHTS
# ============================================================

DEFAULT_WEIGHTS = {
    "absences_weight": 1.0,
    "studytime_weight": 1.0,
    "G1_weight": 1.0,
    "G2_weight": 1.0,
    "Grade_Momentum_weight": 1.0,
    "failures_weight": 1.0,
    "freetime_weight": 1.0,
    "goout_weight": 1.0,
}


# ============================================================
# 2. INITIALIZE WEIGHTS
# ============================================================

def initialize_weights():

    if not os.path.exists(WEIGHTS_FILE):

        pd.DataFrame(
            [DEFAULT_WEIGHTS]
        ).to_csv(
            WEIGHTS_FILE,
            index=False
        )

        return

    try:

        weights_df = pd.read_csv(
            WEIGHTS_FILE
        )

    except Exception:

        weights_df = pd.DataFrame(
            [DEFAULT_WEIGHTS]
        )

        weights_df.to_csv(
            WEIGHTS_FILE,
            index=False
        )

        return

    changed = False

    # Make sure dataframe has at least one row
    if weights_df.empty:

        weights_df = pd.DataFrame(
            [DEFAULT_WEIGHTS]
        )

        changed = True

    # Add missing weight columns
    for column, value in DEFAULT_WEIGHTS.items():

        if column not in weights_df.columns:

            weights_df.loc[0, column] = value

            changed = True

    if changed:

        weights_df.to_csv(
            WEIGHTS_FILE,
            index=False
        )


# ============================================================
# 3. LOAD LEARNED WEIGHTS
# ============================================================

def load_weights():

    initialize_weights()

    try:

        weights_df = pd.read_csv(
            WEIGHTS_FILE
        )

        if weights_df.empty:

            return DEFAULT_WEIGHTS.copy()

        weights = weights_df.iloc[0].to_dict()

        # Make sure all expected weights exist
        for column, default_value in DEFAULT_WEIGHTS.items():

            if column not in weights:

                weights[column] = default_value

        return weights

    except Exception:

        return DEFAULT_WEIGHTS.copy()


# ============================================================
# 4. XAI → PEDAGOGICAL ACTION MAPPING
# ============================================================

RECOMMENDATION_MAP = {

    "G1": {
        "reason": (
            "The student's earlier academic performance "
            "is contributing to the predicted risk."
        ),
        "action": (
            "Schedule a foundational concept review session "
            "and provide targeted support for topics where "
            "the student performed poorly."
        ),
    },

    "G2": {
        "reason": (
            "The student's recent academic performance "
            "is contributing to the predicted risk."
        ),
        "action": (
            "Provide targeted remedial support and monitor "
            "the student's performance before the final assessment."
        ),
    },

    "Grade_Momentum": {
        "reason": (
            "The student's academic performance shows a "
            "negative or concerning change between assessment periods."
        ),
        "action": (
            "Schedule an individual progress review to identify "
            "the cause of the performance change and create "
            "a short-term improvement plan."
        ),
    },

    "absences": {
        "reason": (
            "Attendance-related behaviour is contributing "
            "to the predicted academic risk."
        ),
        "action": (
            "Schedule an attendance review and investigate "
            "whether personal, health, transport, or timetable "
            "issues are affecting attendance."
        ),
    },

    "studytime": {
        "reason": (
            "Low independent study time is contributing "
            "to the predicted academic risk."
        ),
        "action": (
            "Create a structured weekly study plan and recommend "
            "guided study sessions or an academic peer mentor."
        ),
    },

    "failures": {
        "reason": (
            "Previous academic failures are contributing "
            "to the predicted risk."
        ),
        "action": (
            "Provide weekly academic check-ins, progressive "
            "practice exercises, and targeted support in difficult subjects."
        ),
    },

    "freetime": {
        "reason": (
            "The student's free-time pattern is contributing "
            "to the predicted academic risk."
        ),
        "action": (
            "Discuss time-management strategies and help the "
            "student create a better balance between academic "
            "activities and leisure."
        ),
    },

    "goout": {
        "reason": (
            "Frequent social activities may be contributing "
            "to reduced academic engagement."
        ),
        "action": (
            "Provide time-management guidance and help the "
            "student establish protected study periods."
        ),
    },

    "age": {
        "reason": (
            "The student's age-related feature contributes "
            "to the model's prediction."
        ),
        "action": (
            "Monitor the student's academic engagement and "
            "provide additional academic support where required."
        ),
    },

    "Fedu": {
        "reason": (
            "The model identifies a relationship between "
            "parental education background and the prediction."
        ),
        "action": (
            "Use this only as a contextual signal and provide "
            "equal-access academic support based on the student's "
            "actual learning needs."
        ),
    },
}


# ============================================================
# 5. IDENTIFY FEATURE FROM LIME RULE
# ============================================================

def identify_feature_from_rule(rule):

    rule = str(rule)

    # Longest feature names first
    feature_names = sorted(
        RECOMMENDATION_MAP.keys(),
        key=len,
        reverse=True
    )

    for feature in feature_names:

        if feature in rule:

            return feature

    return None


# ============================================================
# 6. GENERATE XAI-DRIVEN RECOMMENDATION
# ============================================================

def get_xai_recommendation(explanation_list):
    """
    Convert positive LIME risk drivers into a pedagogical
    recommendation.

    Lecturer feedback weights are incorporated so that the
    human-in-the-loop mechanism can influence future
    recommendation prioritisation.
    """

    initialize_weights()

    # --------------------------------------------------------
    # No explanation
    # --------------------------------------------------------

    if not explanation_list:

        return (
            "Action Recommendation: "
            "No strong risk driver was identified. "
            "Continue monitoring the student's academic progress."
        )

    # --------------------------------------------------------
    # Load lecturer-adjusted weights
    # --------------------------------------------------------

    learned_weights = load_weights()

    # --------------------------------------------------------
    # Identify positive risk drivers
    # --------------------------------------------------------

    risk_drivers = []

    for rule, lime_weight in explanation_list:

        try:

            lime_weight = float(
                lime_weight
            )

        except Exception:

            continue

        # Only positive LIME contributions increase risk
        if lime_weight <= 0:

            continue

        feature = identify_feature_from_rule(
            rule
        )

        if feature is None:

            continue

        weight_column = (
            feature + "_weight"
        )

        learned_weight = float(
            learned_weights.get(
                weight_column,
                1.0
            )
        )

        # ----------------------------------------------------
        # Human-in-the-loop adjustment
        # ----------------------------------------------------

        adjusted_impact = (
            lime_weight
            * learned_weight
        )

        risk_drivers.append(
            {
                "feature": feature,
                "rule": str(rule),
                "lime_weight": lime_weight,
                "learned_weight": learned_weight,
                "adjusted_impact": adjusted_impact,
            }
        )

    # --------------------------------------------------------
    # No recognizable positive driver
    # --------------------------------------------------------

    if not risk_drivers:

        return (
            "Action Recommendation: "
            "The explanation does not show a strong positive "
            "risk driver. Continue monitoring the student's "
            "academic progress."
        )

    # --------------------------------------------------------
    # Select strongest driver
    # --------------------------------------------------------

    strongest_driver = max(
        risk_drivers,
        key=lambda item: item["adjusted_impact"]
    )

    feature = strongest_driver[
        "feature"
    ]

    recommendation = RECOMMENDATION_MAP.get(
        feature
    )

    if recommendation is None:

        return (
            "Action Recommendation: "
            "Monitor the student's academic engagement "
            "and provide targeted support."
        )

    # --------------------------------------------------------
    # Build final recommendation
    # --------------------------------------------------------

    return (
        "Action Recommendation: "
        + recommendation["action"]
        + " "
        + "Reason: "
        + recommendation["reason"]
    )


# ============================================================
# 7. UPDATE WEIGHTS FROM LECTURER FEEDBACK
# ============================================================

def update_weights_from_feedback():

    initialize_weights()

    # --------------------------------------------------------
    # No feedback file
    # --------------------------------------------------------

    if not os.path.exists(LOG_FILE):

        return

    try:

        feedback_df = pd.read_csv(
            LOG_FILE
        )

    except Exception:

        return

    if feedback_df.empty:

        return

    # --------------------------------------------------------
    # Load current weights
    # --------------------------------------------------------

    weights_df = pd.read_csv(
        WEIGHTS_FILE
    )

    if weights_df.empty:

        weights_df = pd.DataFrame(
            [DEFAULT_WEIGHTS]
        )

    # --------------------------------------------------------
    # Ensure required feedback columns exist
    # --------------------------------------------------------

    # ----------------------------------------------------
    # Ensure processing-status column exists
    # ----------------------------------------------------

    if "Feedback_Processed" not in feedback_df.columns:

        feedback_df["Feedback_Processed"] = "False"

    else:

        # CSV files store this column as text in some pandas
        # configurations. Keep the entire column consistently
        # as strings to avoid dtype assignment errors.
        feedback_df["Feedback_Processed"] = (
            feedback_df["Feedback_Processed"]
            .astype(str)
            .str.strip()
            .str.lower()
            .map({
                "true": "True",
                "false": "False",
                "1": "True",
                "0": "False",
                "nan": "False",
                "": "False"
            })
            .fillna("False")
        )

    # --------------------------------------------------------
    # Feature keywords
    # --------------------------------------------------------

    feature_keywords = {

        "absences_weight": [
            "attendance",
            "absence",
            "absences"
        ],

        "studytime_weight": [
            "study",
            "studytime",
            "mentor",
            "learning"
        ],

        "G1_weight": [
            "first-period",
            "earlier grade",
            "g1"
        ],

        "G2_weight": [
            "second-period",
            "recent grade",
            "g2"
        ],

        "Grade_Momentum_weight": [
            "performance change",
            "negative or concerning change",
            "progress review",
            "decline"
        ],

        "failures_weight": [
            "academic failures",
            "previous academic failures",
            "failed",
            "failure"
        ],

        "freetime_weight": [
            "free-time",
            "free time",
            "time-management"
        ],

        "goout_weight": [
            "social activities",
            "social activity",
            "goout"
        ],
    }

    # --------------------------------------------------------
    # Find unprocessed feedback
    # --------------------------------------------------------

    unprocessed_indices = feedback_df.index[
        feedback_df["Feedback_Processed"] != "True"
    ].tolist()

    if not unprocessed_indices:

        feedback_df.to_csv(
            LOG_FILE,
            index=False
        )

        return

    # ========================================================
    # PROCESS FEEDBACK
    # ========================================================

    for feedback_index in unprocessed_indices:

        feedback_row = feedback_df.loc[
            feedback_index
        ]

        feedback_type = str(
            feedback_row.get(
                "Lecturer_Feedback",
                ""
            )
        ).strip()

        feedback_action = str(
            feedback_row.get(
                "Feedback_Action",
                ""
            )
        ).strip()

        feedback_comment = str(
            feedback_row.get(
                "Lecturer_Comment",
                ""
            )
        ).strip()

        recommendation_text = str(
            feedback_row.get(
                "Recommendation",
                ""
            )
        ).lower()

        analysis_text = (
            recommendation_text
            + " "
            + feedback_comment.lower()
        )

        # ----------------------------------------------------
        # Feedback adjustment
        # ----------------------------------------------------

        if feedback_type == "Useful":

            adjustment = 0.05

        elif feedback_type == "Partially useful":

            adjustment = -0.05

        elif feedback_type.lower() == "not useful":

            adjustment = -0.15

        else:

            adjustment = 0.0

        # ----------------------------------------------------
        # Rejection strengthens negative adjustment
        # ----------------------------------------------------

        if feedback_action == "Reject recommendation":

            adjustment *= 2.0

        # ----------------------------------------------------
        # Identify affected features
        # ----------------------------------------------------

        matched_features = []

        for weight_column, keywords in feature_keywords.items():

            for keyword in keywords:

                if keyword in analysis_text:

                    matched_features.append(
                        weight_column
                    )

                    break

        # ----------------------------------------------------
        # Update weights
        # ----------------------------------------------------

        for feature_column in matched_features:

            current_weight = float(
                weights_df.loc[
                    0,
                    feature_column
                ]
            )

            new_weight = (
                current_weight
                + adjustment
            )

            # Keep within safe range
            new_weight = max(
                0.2,
                min(
                    2.0,
                    new_weight
                )
            )

            new_weight = round(
                new_weight,
                2
            )

            weights_df.loc[
                0,
                feature_column
            ] = new_weight

        # ----------------------------------------------------
        # Mark processed
        # ----------------------------------------------------

        feedback_df.loc[
            feedback_index,
            "Feedback_Processed"
        ] = "True"

    # ========================================================
    # SAVE
    # ========================================================

    weights_df.to_csv(
        WEIGHTS_FILE,
        index=False
    )

    feedback_df.to_csv(
        LOG_FILE,
        index=False
    )


# ============================================================
# 8. BACKWARD-COMPATIBLE DYNAMIC RECOMMENDATION
# ============================================================

def get_dynamic_recommendation(student_data):

    initialize_weights()

    weights = load_weights()

    abs_w = float(
        weights.get(
            "absences_weight",
            1.0
        )
    )

    study_w = float(
        weights.get(
            "studytime_weight",
            1.0
        )
    )

    try:

        absences = int(
            student_data.get(
                "absences",
                0
            )
        )

    except Exception:

        absences = 0

    try:

        studytime = int(
            student_data.get(
                "studytime",
                4
            )
        )

    except Exception:

        studytime = 4

    # --------------------------------------------------------
    # Calculate simple risk indicators
    # --------------------------------------------------------

    absences_risk = (
        absences / 15
    ) * abs_w

    study_risk = (
        1 / max(
            1,
            studytime
        )
    ) * study_w

    # --------------------------------------------------------
    # Recommendation
    # --------------------------------------------------------

    if (
        absences_risk > study_risk
        and absences_risk > 0.4
    ):

        return (
            "Action Recommendation: "
            "Attendance risk detected. "
            "Schedule an attendance review session."
        )

    elif (
        study_risk >= absences_risk
        and study_risk > 0.4
    ):

        return (
            "Action Recommendation: "
            "Study habits risk detected. "
            "Create a structured study plan or assign "
            "an academic peer mentor."
        )

    else:

        return (
            "Action Recommendation: "
            "Student performance stable. "
            "Maintain current academic support."
        )