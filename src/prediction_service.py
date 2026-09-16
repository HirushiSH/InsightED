import os
import joblib
import pandas as pd
import numpy as np

from lime.lime_tabular import LimeTabularExplainer


class InsightEDPredictionService:
    """
    InsightED Prediction Service

    Pipeline:

        Raw student data
                ↓
        Data preparation
                ↓
        Feature engineering
                ↓
        Missing-value handling
                ↓
        Trained preprocessing
                ↓
        Logistic Regression
                ↓
        Risk prediction
                ↓
        LIME explanation
    """

    # ============================================================
    # INITIALIZATION
    # ============================================================

    def __init__(self):

        # --------------------------------------------------------
        # PROJECT ROOT
        # --------------------------------------------------------

        self.project_root = os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )

        # --------------------------------------------------------
        # MODEL PATH
        # --------------------------------------------------------

        model_path = os.path.join(
            self.project_root,
            "models",
            "logistic_regression_model.pkl"
        )

        # --------------------------------------------------------
        # PREPROCESSOR PATH
        # --------------------------------------------------------

        preprocessor_path = os.path.join(
            self.project_root,
            "models",
            "features.pkl"
        )

        # --------------------------------------------------------
        # TRAINING DATA FOR LIME
        # --------------------------------------------------------

        training_path = os.path.join(
            self.project_root,
            "dataset",
            "X_train_balanced.csv"
        )

        # --------------------------------------------------------
        # CHECK REQUIRED FILES
        # --------------------------------------------------------

        if not os.path.exists(model_path):

            raise FileNotFoundError(
                f"ML model not found:\n{model_path}"
            )

        if not os.path.exists(preprocessor_path):

            raise FileNotFoundError(
                f"Preprocessor not found:\n{preprocessor_path}"
            )

        if not os.path.exists(training_path):

            raise FileNotFoundError(
                f"LIME training data not found:\n{training_path}"
            )

        # --------------------------------------------------------
        # LOAD MODEL
        # --------------------------------------------------------

        self.model = joblib.load(
            model_path
        )

        # --------------------------------------------------------
        # LOAD TRAINED PREPROCESSOR
        # --------------------------------------------------------

        self.preprocessor = joblib.load(
            preprocessor_path
        )

        # --------------------------------------------------------
        # LOAD TRAINING DATA
        # --------------------------------------------------------

        self.X_train_balanced = pd.read_csv(
            training_path
        )

        # --------------------------------------------------------
        # MODEL FEATURE NAMES
        # --------------------------------------------------------

        self.model_feature_names = (
            self.X_train_balanced.columns.tolist()
        )

        # --------------------------------------------------------
        # CREATE LIME EXPLAINER
        # --------------------------------------------------------

        self.lime_explainer = LimeTabularExplainer(

            training_data=self.X_train_balanced.values,

            feature_names=self.model_feature_names,

            class_names=[
                "Safe",
                "At-Risk"
            ],

            mode="classification",

            random_state=42
        )

    # ============================================================
    # CLEAN MISSING VALUES
    # ============================================================

    def clean_missing_values(self, data):
        """
        Safely handle missing values.

        Numeric columns:
            Missing values are replaced with the column median.

        Categorical columns:
            Missing values are replaced with the most frequent value.

        This method does NOT call itself recursively.
        """

        data = data.copy()

        # --------------------------------------------------------
        # NUMERIC COLUMNS
        # --------------------------------------------------------

        numeric_columns = data.select_dtypes(
            include=[np.number]
        ).columns

        for column in numeric_columns:

            if data[column].isna().any():

                median_value = data[column].median()

                # If the entire column is NaN,
                # use zero as a safe fallback.
                if pd.isna(median_value):

                    median_value = 0

                data[column] = data[column].fillna(
                    median_value
                )

        # --------------------------------------------------------
        # CATEGORICAL COLUMNS
        # --------------------------------------------------------

        categorical_columns = data.select_dtypes(
            exclude=[np.number]
        ).columns

        for column in categorical_columns:

            if data[column].isna().any():

                mode_values = data[column].mode()

                if not mode_values.empty:

                    fill_value = mode_values.iloc[0]

                else:

                    fill_value = "unknown"

                data[column] = data[column].fillna(
                    fill_value
                )

        return data

    # ============================================================
    # PREPARE UPLOADED DATA
    # ============================================================

    def prepare_uploaded_data(self, df):
        """
        Prepare raw student data for the trained preprocessing
        pipeline.

        Important:
        - Student ID is removed from ML input.
        - G3 is removed because it is the target/future outcome.
        - Grade_Momentum is generated from G2 - G1.
        - Only features expected by the trained preprocessor
          are retained.
        - Missing values are handled safely.
        """

        if not isinstance(df, pd.DataFrame):

            raise TypeError(
                "Input must be a pandas DataFrame."
            )

        # --------------------------------------------------------
        # COPY INPUT
        # --------------------------------------------------------

        data = df.copy()

        # --------------------------------------------------------
        # REMOVE TARGET
        # --------------------------------------------------------

        if "G3" in data.columns:

            data = data.drop(
                columns=["G3"]
            )

        # --------------------------------------------------------
        # REMOVE STUDENT ID
        # --------------------------------------------------------

        if "Student ID" in data.columns:

            data = data.drop(
                columns=["Student ID"]
            )

        # --------------------------------------------------------
        # CREATE GRADE MOMENTUM
        # --------------------------------------------------------

        if (
            "G1" in data.columns
            and "G2" in data.columns
        ):

            data["Grade_Momentum"] = (

                pd.to_numeric(
                    data["G2"],
                    errors="coerce"
                )

                -

                pd.to_numeric(
                    data["G1"],
                    errors="coerce"
                )
            )

        # --------------------------------------------------------
        # EXPECTED RAW FEATURES
        # --------------------------------------------------------

        required_columns = (
            list(self.preprocessor.num_cols)
            +
            list(self.preprocessor.cat_cols)
        )

        # --------------------------------------------------------
        # CHECK FOR MISSING COLUMNS
        # --------------------------------------------------------

        missing_columns = [

            column

            for column in required_columns

            if column not in data.columns
        ]

        if missing_columns:

            raise ValueError(
                "The uploaded dataset is missing required "
                "features: "
                + str(missing_columns)
            )

        # --------------------------------------------------------
        # KEEP ONLY REQUIRED FEATURES
        # --------------------------------------------------------

        data = data[
            required_columns
        ].copy()

        # --------------------------------------------------------
        # CONVERT NUMERIC FEATURES
        # --------------------------------------------------------

        for column in self.preprocessor.num_cols:

            if column in data.columns:

                data[column] = pd.to_numeric(
                    data[column],
                    errors="coerce"
                )

        # --------------------------------------------------------
        # CLEAN MISSING VALUES
        # --------------------------------------------------------

        data = self.clean_missing_values(
            data
        )

        # --------------------------------------------------------
        # FINAL NaN CHECK
        # --------------------------------------------------------

        if data.isna().any().any():

            nan_columns = data.columns[
                data.isna().any()
            ].tolist()

            raise ValueError(
                "NaN values remain after cleaning: "
                + str(nan_columns)
            )

        return data

    # ============================================================
    # PREPROCESS
    # ============================================================

    def preprocess(self, df):
        """
        Apply the exact preprocessing pipeline used during
        model training.
        """

        # --------------------------------------------------------
        # PREPARE RAW DATA
        # --------------------------------------------------------

        prepared_data = self.prepare_uploaded_data(
            df
        )

        # --------------------------------------------------------
        # APPLY TRAINED PREPROCESSOR
        # --------------------------------------------------------

        processed_data = self.preprocessor.transform(
            prepared_data
        )

        # --------------------------------------------------------
        # CONVERT TO DATAFRAME IF NECESSARY
        # --------------------------------------------------------

        if isinstance(
            processed_data,
            pd.DataFrame
        ):

            processed_df = processed_data.copy()

        else:

            # Try to obtain feature names from the
            # trained preprocessor.

            try:

                feature_names = (
                    self.preprocessor.feature_names_out
                )

            except AttributeError:

                feature_names = self.model_feature_names

            processed_df = pd.DataFrame(
                processed_data,
                columns=feature_names,
                index=prepared_data.index
            )

        # --------------------------------------------------------
        # CHECK FOR NaN
        # --------------------------------------------------------

        if processed_df.isna().any().any():

            nan_columns = processed_df.columns[
                processed_df.isna().any()
            ].tolist()

            raise ValueError(
                "The preprocessing pipeline produced NaN "
                "values in: "
                + str(nan_columns)
            )

        # --------------------------------------------------------
        # CHECK FEATURE COUNT
        # --------------------------------------------------------

        if processed_df.shape[1] != len(
            self.model_feature_names
        ):

            raise ValueError(
                "Feature count mismatch.\n"
                f"Preprocessor produced "
                f"{processed_df.shape[1]} features, "
                f"but the trained model expects "
                f"{len(self.model_feature_names)}."
            )

        # --------------------------------------------------------
        # FORCE EXACT MODEL FEATURE ORDER
        # --------------------------------------------------------

        missing_model_features = [

            column

            for column in self.model_feature_names

            if column not in processed_df.columns
        ]

        if missing_model_features:

            raise ValueError(
                "Processed data is missing model features: "
                + str(missing_model_features)
            )

        processed_df = processed_df[
            self.model_feature_names
        ].copy()

        return processed_df

    # ============================================================
    # PREDICT
    # ============================================================

    def predict(self, df):
        """
        Generate ML predictions and At-Risk probabilities.

        Returns the original input DataFrame with:

            AI_Prediction
            Risk_Probability
            AI_Status
        """

        # --------------------------------------------------------
        # COPY ORIGINAL DATA
        # --------------------------------------------------------

        result = df.copy()

        # --------------------------------------------------------
        # PREPROCESS
        # --------------------------------------------------------

        processed_data = self.preprocess(
            df
        )

        # --------------------------------------------------------
        # PREDICTIONS
        # --------------------------------------------------------

        predictions = self.model.predict(
            processed_data
        )

        # --------------------------------------------------------
        # PROBABILITIES
        # --------------------------------------------------------

        probabilities = self.model.predict_proba(
            processed_data
        )[:, 1]

        # --------------------------------------------------------
        # ADD RESULTS
        # --------------------------------------------------------

        result["AI_Prediction"] = predictions

        result["Risk_Probability"] = probabilities

        result["AI_Status"] = np.where(
            predictions == 1,
            "At-Risk",
            "Safe"
        )

        return result

    # ============================================================
    # PREDICT ONE STUDENT
    # ============================================================

    def predict_student(self, df):
        """
        Convenience method for predicting a single student.
        """

        if len(df) != 1:

            raise ValueError(
                "predict_student() expects exactly one student."
            )

        return self.predict(
            df
        )

    # ============================================================
    # LIME EXPLANATION
    # ============================================================

    def explain_student(self, df, index=0):
        """
        Generate a LIME explanation for one student.

        Parameters
        ----------
        df : pandas.DataFrame
            Raw student data.

        index : int
            Row position of the student to explain.

        Returns
        -------
        lime.explanation.Explanation
            LIME explanation object.
        """

        # --------------------------------------------------------
        # PREPROCESS
        # --------------------------------------------------------

        processed_data = self.preprocess(
            df
        )

        # --------------------------------------------------------
        # VALIDATE INDEX
        # --------------------------------------------------------

        if index < 0 or index >= len(
            processed_data
        ):

            raise IndexError(
                f"Student index {index} is outside "
                f"the valid range "
                f"0-{len(processed_data) - 1}."
            )

        # --------------------------------------------------------
        # GET SELECTED STUDENT
        # --------------------------------------------------------

        student_row = processed_data.iloc[
            index
        ].values.astype(float)

        # --------------------------------------------------------
        # LIME PREDICTION WRAPPER
        # --------------------------------------------------------

        def lime_predict_proba(X):

            X_df = pd.DataFrame(
                X,
                columns=self.model_feature_names
            )

            return self.model.predict_proba(
                X_df
            )

        # --------------------------------------------------------
        # GENERATE EXPLANATION
        # --------------------------------------------------------

        explanation = (
            self.lime_explainer.explain_instance(

                student_row,

                lime_predict_proba,

                num_features=5
            )
        )

        return explanation

    # ============================================================
    # GET LIME EXPLANATION AS LIST
    # ============================================================

    def get_explanation_list(
        self,
        df,
        index=0
    ):
        """
        Return the LIME explanation as a simple list:

            [
                (feature_rule, weight),
                ...
            ]
        """

        explanation = self.explain_student(
            df,
            index
        )

        return explanation.as_list()

    # ============================================================
    # GET RISK PROBABILITY
    # ============================================================

    def get_risk_probability(self, df):
        """
        Return At-Risk probabilities.
        """

        result = self.predict(
            df
        )

        return result[
            "Risk_Probability"
        ].values

    # ============================================================
    # GET RISK LEVEL
    # ============================================================

    @staticmethod
    def get_risk_level(probability):
        """
        Convert model probability into a lecturer-friendly
        risk level.
        """

        probability = float(
            probability
        )

        if probability >= 0.70:

            return "High attention"

        elif probability >= 0.40:

            return "Moderate attention"

        else:

            return "Lower attention"