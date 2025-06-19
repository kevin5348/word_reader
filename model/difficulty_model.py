import os
import numpy as np
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

def train_model(df):
    df["log_count"] = np.log1p(df["count"])
    features = ["log_count", "syllables", "is_homophone","pronunciation_count"]
    X = df[features]
    y = df["user_difficulty_test"]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = LogisticRegression()
    model.fit(X_scaled, y)

    return model, scaler

def save_model(model, scaler, model_path="model/difficulty_model.pkl", scaler_path="model/scaler.pkl"):
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    os.makedirs(os.path.dirname(scaler_path), exist_ok=True)

    joblib.dump(model, model_path)
    joblib.dump(scaler, scaler_path)


def load_model(model_path="/home/kevin/repos/word_reader/models/difficulty_model.pkl", scaler_path="/home/kevin/repos/word_reader/models/scaler.pkl"):
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    return model, scaler

def predict_difficulty(df, model, scaler):
    df["log_count"] = np.log1p(df["count"])
    X = df[["log_count", "syllables","is_homophone","pronunciation_count"]]
    df["predicted_difficulty"] = model.predict(scaler.transform(X))
    return df
