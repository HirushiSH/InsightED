import pandas as pd
import numpy as np
import os
import joblib
import matplotlib.pyplot as plt
import shap
from lime.lime_tabular import LimeTabularExplainer

print("🔍 Initializing Explainable AI (XAI) Matrix Process...")

# Load processed data matrices
X_train = pd.read_csv(os.path.join("dataset", "X_train_balanced.csv"))
X_test = pd.read_csv(os.path.join("dataset", "X_test_processed.csv"))
feature_names = X_train.columns.tolist()

# Load the trained Logistic Regression model
model_path = os.path.join("models", "logistic_regression_model.pkl")
if not os.path.exists(model_path):
    raise FileNotFoundError("Trained model file missing in 'models/'. Please run step 4 first.")
    
model = joblib.load(model_path)

# 1. Compute SHAP Global Interpretability
print("📊 Computing Global SHAP values for the model...")
explainer_shap = shap.LinearExplainer(model, shap.maskers.Independent(X_train, max_samples=100))
shap_values = explainer_shap(X_test)

# Generate and save the SHAP Global Summary Plot for your thesis report
plt.figure(figsize=(10, 6))
shap.summary_plot(shap_values, X_test, feature_names=feature_names, show=False)
plt.title("InsightED Thesis Figure: SHAP Global Feature Importance Summary", fontsize=12, fontweight='bold', pad=20)
plt.tight_layout()

shap_plot_path = os.path.join("models", "shap_global_importance.png")
plt.savefig(shap_plot_path, dpi=300)
plt.close()
print(f"📈 SHAP Global Importance graph saved to: '{shap_plot_path}'")

# 2. Build the LIME Explainer for Localized Validation
print("🎯 Initializing LIME Tabular Explainer for individual student tracking...")
explainer_lime = LimeTabularExplainer(
    training_data=np.array(X_train),
    feature_names=feature_names,
    class_names=['Safe', 'At-Risk'],
    mode='classification',
    kernel_width=3.0,
    random_state=42
)

print("🧪 Running verification test for local explanation on Student Index 0...")
student_row_array = X_test.iloc[0].values

exp = explainer_lime.explain_instance(
    data_row=student_row_array,
    predict_fn=model.predict_proba,
    num_features=5
)

# Extract and display the local drivers to the terminal screen
local_rules = exp.as_list()
print("\n📌 --- LOCAL RISK DRIVERS EXTRACTED FOR STUDENT 0 ---")
for feature, weight in local_rules:
    print(f"Variable Rule: {feature.ljust(30)} | Predictive Weight Vector: {weight:+.4f}")
print("------------------------------------------------------\n")

# 3. Serialize and save the SHAP Explainer
joblib.dump(explainer_shap, os.path.join("models", "explainer_shap.pkl"))

print("💾 Step 4 Complete: XAI extractors configured and artifacts cached safely inside 'models/'.")