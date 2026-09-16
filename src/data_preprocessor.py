import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder


class InsightEDDataPreprocessor:

    def __init__(self):
        self.scaler = StandardScaler()
        self.encoder = OneHotEncoder(
            sparse_output=False,
            handle_unknown='ignore'
        )
        self.num_cols = []
        self.cat_cols = []
        self.feature_names_out = []

    def fit(self, X):

        self.num_cols = X.select_dtypes(
            include=['int64', 'float64']
        ).columns.tolist()

        self.cat_cols = X.select_dtypes(
            include=['object']
        ).columns.tolist()

        if self.cat_cols:
            self.encoder.fit(X[self.cat_cols])

        if self.num_cols:
            self.scaler.fit(X[self.num_cols])

        if self.cat_cols:
            encoded_cat_names = (
                self.encoder
                .get_feature_names_out(self.cat_cols)
                .tolist()
            )
        else:
            encoded_cat_names = []

        self.feature_names_out = (
            self.num_cols + encoded_cat_names
        )

        return self

    def transform(self, X):

        X_num_scaled = (
            self.scaler.transform(X[self.num_cols])
            if self.num_cols
            else np.empty((len(X), 0))
        )

        X_cat_encoded = (
            self.encoder.transform(X[self.cat_cols])
            if self.cat_cols
            else np.empty((len(X), 0))
        )

        X_combined = np.hstack(
            (X_num_scaled, X_cat_encoded)
        )

        return pd.DataFrame(
            X_combined,
            columns=self.feature_names_out
        )