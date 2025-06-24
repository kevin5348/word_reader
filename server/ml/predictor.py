import numpy as np
import os
import joblib
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

def load_model(model_path="difficulty_model.pkl", scaler_path="scaler.pkl"):
    model_path = os.path.join(os.path.dirname(__file__), "difficulty_model.pkl")
    scaler_path = os.path.join(os.path.dirname(__file__), "scaler.pkl")
 
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    return model, scaler

def predict_difficulty(df, model, scaler):
    df["log_count"] = np.log1p(df["count"])
    X = df[["log_count", "syllables","is_homophone","pronunciation_count"]]
    df["predicted_difficulty"] = model.predict(scaler.transform(X))
    return df