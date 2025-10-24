# src/analyze_usage.py
import pandas as pd
import pickle

# Load models
with open('models/anomaly_detector.pkl', 'rb') as f:
    anomaly_model = pickle.load(f)
with open('models/energy_predictor.pkl', 'rb') as f:
    energy_model = pickle.load(f)

def analyze_usage(df):
    X = df[['hours_used', 'power_watts']]
    
    # Anomaly Detection
    df['anomaly'] = anomaly_model.predict(X)
    df['anomaly'] = df['anomaly'].apply(lambda x: True if x == -1 else False)
    
    # Energy Prediction
    df['predicted_energy'] = energy_model.predict(X)
    
    return df
