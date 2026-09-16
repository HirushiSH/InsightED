import pandas as pd
import joblib

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix
)


# ============================================================
# LOAD TEST DATA
# ============================================================

X_test = pd.read_csv(
    "dataset/X_test.csv"
)

y_test = pd.read_csv(
    "dataset/y_test.csv"
).iloc[:, 0].astype(int)


print("=" * 80)
print("FINAL MODEL COMPARISON - UCI STUDENT PERFORMANCE (PORTUGUESE)")
print("=" * 80)

print(f"Test samples: {len(y_test)}")
print(f"Test features: {X_test.shape[1]}")
print()


# ============================================================
# LOAD PREPROCESSOR
# ============================================================

preprocessor = joblib.load(
    "models/features.pkl"
)


# ============================================================
# PREPROCESS TEST DATA
# ============================================================

X_test_processed = preprocessor.transform(
    X_test
)


# ============================================================
# LOAD MODELS
# ============================================================

models = {

    "Logistic Regression":
        joblib.load(
            "models/logistic_regression_model.pkl"
        ),

    "Random Forest":
        joblib.load(
            "models/random_forest_model.pkl"
        ),

    "XGBoost":
        joblib.load(
            "models/xgboost_model.pkl"
        )
}


# ============================================================
# EVALUATE MODELS
# ============================================================

results = []


for name, model in models.items():

    # --------------------------------------------------------
    # Predictions
    # --------------------------------------------------------

    y_pred = model.predict(
        X_test_processed
    )

    # --------------------------------------------------------
    # Probabilities
    # --------------------------------------------------------

    y_probability = model.predict_proba(
        X_test_processed
    )[:, 1]

    # --------------------------------------------------------
    # Metrics
    # --------------------------------------------------------

    accuracy = accuracy_score(
        y_test,
        y_pred
    )

    precision = precision_score(
        y_test,
        y_pred,
        zero_division=0
    )

    recall = recall_score(
        y_test,
        y_pred,
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        y_pred,
        zero_division=0
    )

    roc_auc = roc_auc_score(
        y_test,
        y_probability
    )

    cm = confusion_matrix(
        y_test,
        y_pred
    )

    results.append({
        "Model": name,
        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1 Score": f1,
        "ROC-AUC": roc_auc
    })

    # --------------------------------------------------------
    # Display individual model results
    # --------------------------------------------------------

    print("-" * 80)
    print(name)
    print("-" * 80)

    print(f"Accuracy : {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall   : {recall:.4f}")
    print(f"F1 Score : {f1:.4f}")
    print(f"ROC-AUC  : {roc_auc:.4f}")

    print()
    print("Confusion Matrix:")
    print(cm)

    print()
    print(
        "Predicted classes:",
        pd.Series(y_pred).value_counts().sort_index().to_dict()
    )

    print(
        "Actual classes:",
        y_test.value_counts().sort_index().to_dict()
    )

    print()


# ============================================================
# FINAL COMPARISON TABLE
# ============================================================

results_df = pd.DataFrame(
    results
)


print("=" * 80)
print("FINAL MODEL COMPARISON")
print("=" * 80)

print(
    results_df.to_string(
        index=False,
        formatters={
            "Accuracy": "{:.4f}".format,
            "Precision": "{:.4f}".format,
            "Recall": "{:.4f}".format,
            "F1 Score": "{:.4f}".format,
            "ROC-AUC": "{:.4f}".format
        }
    )
)


# ============================================================
# BEST MODEL
# ============================================================

best_model = results_df.loc[
    results_df["ROC-AUC"].idxmax()
]

print()
print("=" * 80)
print("BEST MODEL")
print("=" * 80)

print(
    f"Best model based on ROC-AUC: "
    f"{best_model['Model']}"
)

print(
    f"ROC-AUC: "
    f"{best_model['ROC-AUC']:.4f}"
)

print("=" * 80)