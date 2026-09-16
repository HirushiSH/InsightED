import streamlit as st
import pandas as pd

from src.prediction_service import InsightEDPredictionService


@st.cache_resource
def get_required_upload_columns():
    """Return raw CSV columns required by the existing prediction service."""

    prediction_service = InsightEDPredictionService()

    required_columns = (
        list(prediction_service.preprocessor.num_cols)
        + list(prediction_service.preprocessor.cat_cols)
    )

    # The prediction service derives this feature from G1 and G2.
    return tuple(
        column
        for column in required_columns
        if column != "Grade_Momentum"
    )


def get_missing_required_columns(df):
    required_columns = get_required_upload_columns()

    return [
        column
        for column in required_columns
        if column not in df.columns
    ]


def render_data_management():

    # ============================================================
    # PAGE HEADER
    # ============================================================

    st.caption("DATA MANAGEMENT")

    st.title("Prepare student data for analysis")

    st.write(
        "Upload your student information to begin."
    )

    st.divider()

    # ============================================================
    # CHECK FOR EXISTING DATASET
    # ============================================================

    existing_dataset = st.session_state.get(
        "uploaded_dataset"
    )

    # ============================================================
    # EXISTING DATASET
    # ============================================================

    if existing_dataset is not None:

        df = existing_dataset

        st.subheader("Student Dataset")

        st.success(
            "A student dataset is already loaded in InsightED."
        )

        st.write(
            "Your dataset is available across the InsightED "
            "analysis workflow."
        )

        # --------------------------------------------------------
        # DATASET SUMMARY
        # --------------------------------------------------------

        st.divider()

        st.caption("DATASET SUMMARY")

        st.subheader("Your student data")

        total_students = len(df)

        total_features = len(df.columns)

        missing_values = int(
            df.isnull().sum().sum()
        )

        duplicate_rows = int(
            df.duplicated().sum()
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Students",
                f"{total_students:,}"
            )

        with col2:
            st.metric(
                "Information fields",
                f"{total_features:,}"
            )

        with col3:
            st.metric(
                "Missing information",
                f"{missing_values:,}"
            )

        with col4:
            st.metric(
                "Duplicate records",
                f"{duplicate_rows:,}"
            )

        # --------------------------------------------------------
        # DATA CHECK
        # --------------------------------------------------------

        st.divider()

        st.caption("DATA CHECK")

        if missing_values == 0 and duplicate_rows == 0:

            st.success(
                "Your student data looks good."
            )

            st.write(
                "The uploaded data has been checked and "
                "is ready to analyse."
            )

        elif missing_values > 0 and duplicate_rows == 0:

            st.warning(
                "Some student information is missing."
            )

            st.write(
                "The data can still be reviewed before "
                "continuing."
            )

        elif missing_values == 0 and duplicate_rows > 0:

            st.warning(
                "Some duplicate student records were found."
            )

            st.write(
                "Please review the uploaded data before "
                "continuing."
            )

        else:

            st.warning(
                "Some missing information and duplicate "
                "records were found."
            )

            st.write(
                "Please review the uploaded data before "
                "continuing."
            )

        # --------------------------------------------------------
        # DATA PREVIEW
        # --------------------------------------------------------

        st.divider()

        st.caption("DATA PREVIEW")

        st.subheader("Student records")

        st.write(
            "Here is a preview of the student information "
            "currently loaded in InsightED."
        )

        max_rows = min(
            10,
            total_students
        )

        st.dataframe(
            df.head(max_rows),
            use_container_width=True,
            hide_index=True
        )

        # --------------------------------------------------------
        # CHANGE DATASET
        # --------------------------------------------------------

        st.divider()

        st.caption("CHANGE DATASET")

        st.write(
            "If you want to analyse a different class, "
            "you can replace the current dataset."
        )

        replace_file = st.file_uploader(
            "Upload a different CSV file",
            type=["csv"],
            help="This will replace the currently loaded dataset.",
            key="replace_dataset"
        )

        if replace_file is not None:

            try:

                replace_file.seek(0)

                new_df = pd.read_csv(
                    replace_file,
                    sep=";"
                )

                # Support comma-separated CSV files
                if len(new_df.columns) <= 2:

                    replace_file.seek(0)

                    new_df = pd.read_csv(
                        replace_file
                    )

            except Exception:

                st.error(
                    "We couldn't read this file. "
                    "Please check that it is a valid CSV file."
                )

                return

            if new_df.empty:

                st.error(
                    "The uploaded file does not contain "
                    "any student records."
                )

                return

            missing_columns = get_missing_required_columns(
                new_df
            )

            if missing_columns:

                st.error(
                    "The uploaded dataset is missing required "
                    "columns: "
                    + ", ".join(missing_columns)
                )

                return

            # ----------------------------------------------------
            # CREATE STABLE ANONYMOUS IDs
            # ----------------------------------------------------

            if "Student ID" not in new_df.columns:

                new_df.insert(
                    0,
                    "Student ID",
                    [
                        f"STU-{i + 1:03d}"
                        for i in range(len(new_df))
                    ]
                )

            # Replace stored dataset
            st.session_state["uploaded_dataset"] = new_df

            # Reset analysis state for new dataset
            st.session_state["data_ready"] = False

            st.success(
                "The new student dataset has been loaded."
            )

            st.rerun()

        return

    # ============================================================
    # NO DATASET YET
    # ============================================================

    st.subheader("Student Dataset")

    st.write(
        "Upload a CSV file containing student information."
    )

    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=["csv"],
        help="Upload a CSV file containing student records.",
        key="initial_dataset"
    )

    if uploaded_file is None:

        st.info(
            "No dataset uploaded yet. "
            "Choose a CSV file above to get started."
        )

        st.caption(
            "Supported format: CSV • Maximum file size: 200 MB"
        )

        return

    # ============================================================
    # READ DATASET
    # ============================================================

    try:

        uploaded_file.seek(0)

        df = pd.read_csv(
            uploaded_file,
            sep=";"
        )

        # Support comma-separated CSV files
        if len(df.columns) <= 2:

            uploaded_file.seek(0)

            df = pd.read_csv(
                uploaded_file
            )

    except Exception:

        st.error(
            "We couldn't read this file. "
            "Please check that it is a valid CSV file."
        )

        return

    # ============================================================
    # EMPTY DATASET
    # ============================================================

    if df.empty:

        st.error(
            "The uploaded file does not contain "
            "any student records."
        )

        return

    missing_columns = get_missing_required_columns(df)

    if missing_columns:

        st.error(
            "The uploaded dataset is missing required columns: "
            + ", ".join(missing_columns)
        )

        return

    # ============================================================
    # CREATE STABLE ANONYMOUS STUDENT ID
    # ============================================================

    if "Student ID" not in df.columns:

        df.insert(
            0,
            "Student ID",
            [
                f"STU-{i + 1:03d}"
                for i in range(len(df))
            ]
        )

    # ============================================================
    # SAVE DATASET
    # ============================================================

    st.session_state["uploaded_dataset"] = df

    st.session_state["data_ready"] = True

    # ============================================================
    # REFRESH PAGE
    # ============================================================

    st.rerun()
