import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import os

# Create project sub-directories structurally if not present
os.makedirs("dataset", exist_ok=True)
os.makedirs("models", exist_ok=True)

# 1. Point to the localized raw data path
raw_data_path = os.path.join("dataset", "student-por.csv")

if not os.path.exists(raw_data_path):
    raise FileNotFoundError("Missing 'student-por.csv' inside your 'dataset/' folder. Please drop a copy there.")

# Read the raw semi-colon separated data file
df = pd.read_csv(raw_data_path, sep=";")
print(f"Fresh Project State - Raw Rows: {df.shape[0]} | Raw Columns: {df.shape[1]}")

# 2. Academic Feature Selection
# Domain-informed feature selection:
# Remove attributes considered less relevant to the
# academic-risk prediction and lecturer intervention task.
columns_to_drop = ['school', 'nursery', 'romantic', 'reason', 'guardian', 'famsup', 'higher', 'paid']
df_filtered = df.drop(columns=columns_to_drop)
print(f"Filtered out {len(columns_to_drop)} unnecessary noise columns. Retained: {df_filtered.shape[1]} attributes.")

# 3. Custom Feature Engineering (Proposal Metric R12)
# Calculate the performance trend vector between evaluation periods
df_filtered['Grade_Momentum'] = df_filtered['G2'] - df_filtered['G1']
print("Successfully calculated and added 'Grade_Momentum' (G2 - G1).")

# 4. Construct Features (X) and Binary Target Matrix (y)
# Proposal Target: If Final Mark G3 is less than 10, the student is 'At-Risk' (1), else 'Safe' (0)
X = df_filtered.drop(columns=['G3'])
y = (df_filtered['G3'] < 10).astype(int)

print(f"Dataset Balance Evaluation -> Safe (0): {np.sum(y==0)} | At-Risk (1): {np.sum(y==1)}")

# 5. Stratified 80/20 Splitting to preserve risk class proportions
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, stratify=y, random_state=42
)

# Cache data files cleanly into your dataset partition pool
X_train.to_csv(os.path.join("dataset", "X_train.csv"), index=False)
X_test.to_csv(os.path.join("dataset", "X_test.csv"), index=False)
y_train.to_csv(os.path.join("dataset", "y_train.csv"), index=False)
y_test.to_csv(os.path.join("dataset", "y_test.csv"), index=False)

print("Step 1 Complete: Clean dataset fractions generated and saved to 'dataset/'.")