import pandas as pd
import numpy as np
import joblib
import os
from imblearn.over_sampling import SMOTE

from src.data_preprocessor import InsightEDDataPreprocessor

# --- EXECUTION CODE BLOCK ---
if __name__ == "__main__":
    print("🔄 Loading split dataset fractions for preprocessing...")
    
    # Load data files generated in Step 1
    X_train = pd.read_csv(os.path.join("dataset", "X_train.csv"))
    X_test = pd.read_csv(os.path.join("dataset", "X_test.csv"))
    y_train = pd.read_csv(os.path.join("dataset", "y_train.csv")).values.ravel()
    y_test = pd.read_csv(os.path.join("dataset", "y_test.csv")).values.ravel()

    # Initialize and train our pipeline instance
    preprocessor = InsightEDDataPreprocessor()
    preprocessor.fit(X_train)

    # Transform both splits to create identical feature structures
    X_train_proc = preprocessor.transform(X_train)
    X_test_proc = preprocessor.transform(X_test)
    
    print(f"📐 Features dimensions expanded via encoding -> From {X_train.shape[1]} to {X_train_proc.shape[1]} columns.")

    # Apply SMOTE to fix class imbalance on the training dataset
    print(f"⚖️ Applying SMOTE. Original Train Target Breakdown -> Safe: {np.sum(y_train==0)}, At-Risk: {np.sum(y_train==1)}")
    
    smote_engine = SMOTE(random_state=42)
    X_train_balanced, y_train_balanced = smote_engine.fit_resample(X_train_proc, y_train)
    
    print(f"✅ SMOTE Applied successfully! Balanced Train Target Breakdown -> Safe: {np.sum(y_train_balanced==0)}, At-Risk: {np.sum(y_train_balanced==1)}")

    # Save the processed data matrices back to the dataset directory for modeling
    X_train_balanced.to_csv(os.path.join("dataset", "X_train_balanced.csv"), index=False)
    X_test_proc.to_csv(os.path.join("dataset", "X_test_processed.csv"), index=False)
    pd.DataFrame(y_train_balanced, columns=['Target']).to_csv(os.path.join("dataset", "y_train_balanced.csv"), index=False)
    pd.DataFrame(y_test, columns=['Target']).to_csv(os.path.join("dataset", "y_test_processed.csv"), index=False)

    # Save the pipeline object to models directory so the Streamlit dashboard can reload it instantly
    joblib.dump(preprocessor, os.path.join("models", "features.pkl"))
    print("💾 Step 2 Complete: Preprocessing artifacts and pipeline object serialized inside 'models/'.")