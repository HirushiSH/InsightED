import pandas as pd
import numpy as np
import os
import joblib
import matplotlib.pyplot as plt

# Import our 3 baseline and primary algorithms
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

# Import evaluation metrics
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score, roc_curve, auc

# Suppress minor data frame warnings to keep output clean
import warnings
warnings.filterwarnings('ignore', category=UserWarning)

print("🏋️‍♂️ Loading balanced and processed data matrices...")
# Load data files generated in Step 2
X_train = pd.read_csv(os.path.join("dataset", "X_train_balanced.csv"))
y_train = pd.read_csv(os.path.join("dataset", "y_train_balanced.csv")).values.ravel()
X_test = pd.read_csv(os.path.join("dataset", "X_test_processed.csv"))
y_test = pd.read_csv(os.path.join("dataset", "y_test_processed.csv")).values.ravel()

# 1. Initialize our three proposal models
models = {
    "Logistic Regression (Baseline)": LogisticRegression(max_iter=1000, random_state=42),
    "Random Forest (Robust Baseline)": RandomForestClassifier(n_estimators=100, random_state=42),
    "XGBoost (Primary Engine)": XGBClassifier(n_estimators=100, random_state=42, eval_metric='logloss')
}

# Setup dictionaries to capture metrics and graph components
performance_summary = []
plt.figure(figsize=(8, 6))

print("\n🚀 Training models and executing evaluation loop...")

for name, model in models.items():
    # Fit the model on balanced training vectors
    model.fit(X_train, y_train)
    
    # Generate predictions on the unseen test set
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]
    
    # Calculate performance metrics
    acc = accuracy_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred) # Crucial academic metric for student safety
    prec = precision_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    
    # Save metrics to our summary list
    performance_summary.append({
        "Model Name": name,
        "Accuracy": f"{acc:.2%}",
        "Recall (Sensitivity)": f"{rec:.2%}",
        "Precision": f"{prec:.2%}",
        "F1-Score": f"{f1:.2%}"
    })
    
    # Serialize and save each model file to models/ directory
    model_filename = name.lower().replace(" (baseline)", "").replace(" (robust baseline)", "").replace(" (primary engine)", "").replace(" ", "_") + "_model.pkl"
    joblib.dump(model, os.path.join("models", model_filename))
    
    # Compute ROC Curve lines for our diagram
    fpr, tpr, _ = roc_curve(y_test, y_proba)
    roc_auc = auc(fpr, tpr)
    plt.plot(fpr, tpr, label=f'{name} (AUC = {roc_auc:.2f})', lw=2)

# 2. Display a beautiful comparison table directly in the terminal
df_results = pd.DataFrame(performance_summary)
print("\n📊 --- THESIS PERFORMANCE EVALUATION MATRIX ---")
print(df_results.to_string(index=False))
print("------------------------------------------------\n")

# 3. Finalize and save our academic performance graph
plt.plot([0, 1], [0, 1], color='navy', linestyle='--', label='Random Guessing Baseline')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate (1 - Specificity)', fontsize=10, labelpad=10)
plt.ylabel('True Positive Rate (Sensitivity / Recall)', fontsize=10)
plt.title('InsightED Thesis Figure: Receiver Operating Characteristic (ROC) Curve', fontsize=12, fontweight='bold', pad=15)
plt.legend(loc="lower right")
plt.grid(alpha=0.4)
plt.tight_layout()

plot_path = os.path.join("models", "model_comparison_roc_curve.png")
plt.savefig(plot_path, dpi=300)
plt.close()

print(f"📈 Performance chart successfully saved to: '{plot_path}'")
print("💾 Step 3 Complete: Models trained, metrics evaluated, and serialized inside 'models/'.")