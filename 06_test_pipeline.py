import pandas as pd
import numpy as np
import os
import joblib
from src.translator import InsightEDTranslator
from lime.lime_tabular import LimeTabularExplainer

print("📋 Testing System Translation Pipeline Core...")

# 1. Load Data, Model, and Pipeline Artifacts
X_test = pd.read_csv(os.path.join("dataset", "X_test_processed.csv"))
y_test = pd.read_csv(os.path.join("dataset", "y_test_processed.csv")).values.ravel()
X_train_bal = pd.read_csv(os.path.join("dataset", "X_train_balanced.csv"))

model = joblib.load(os.path.join("models", "logistic_regression_model.pkl"))

# 2. Re-initialize LIME dynamically to prevent pickling constraints
explainer_lime = LimeTabularExplainer(
    training_data=np.array(X_train_bal),
    feature_names=X_train_bal.columns.tolist(),
    class_names=['Safe', 'At-Risk'],
    mode='classification',
    random_state=42
)

# Let's find an actual 'At-Risk' student record from the test set to examine!
at_risk_indices = np.where(y_test == 1)[0]
if len(at_risk_indices) == 0:
    target_idx = 0  # Fallback to index 0 if none found
else:
    target_idx = at_risk_indices[0]

print(f"🎯 Selected At-Risk Student Row Index for Test: {target_idx}")
student_features = X_test.iloc[target_idx].values

# 3. Generate Predictions
risk_probability = model.predict_proba([student_features])[0][1]
prediction_label = model.predict([student_features])[0]
status_string = "🚨 AT-RISK" if prediction_label == 1 else "✅ SAFE"

print(f"📊 Model Prediction: {status_string} | Risk Probability: {risk_probability:.2%}")

# 4. Extract LIME local features
exp = explainer_lime.explain_instance(
    data_row=student_features,
    predict_fn=model.predict_proba,
    num_features=3
)

# 5. Translate via our custom OOP engine
print("\n=======================================================")
print("🖥️      INSIGHTED LECTURER INTERFACE DATA CARD          ")
print("=======================================================")
print(f"STUDENT RECORD ID: TEST_ROW_{target_idx}")
print(f"PREDICTIVE STATUS: {status_string} ({risk_probability:.1%}-Risk Factor)")
print("-------------------------------------------------------")
print("💡 TOP DETECTED RISK REASONS & JUSTIFICATIONS:")

for rule_text, weight in exp.as_list():
    # Only pull features driving the risk upward or relevant to performance
    translated_title = InsightEDTranslator.translate_feature_name(rule_text)
    pedagogy_text = InsightEDTranslator.get_actionable_recommendation(rule_text, weight)
    
    print(f"\n🔹 Feature: {translated_title}")
    print(f"   Reason:  {pedagogy_text['reason']}")
    print(f"   Action:  {pedagogy_text['action']}")

print("=======================================================\n")