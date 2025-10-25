# # src/analyze_usage.py
# import pandas as pd
# import pickle

# # Load models
# with open('models/anomaly_detector.pkl', 'rb') as f:
#     anomaly_model = pickle.load(f)
# with open('models/energy_predictor.pkl', 'rb') as f:
#     energy_model = pickle.load(f)

# def analyze_usage(df):
#     X = df[['hours_used', 'power_watts']]
    
#     # Anomaly Detection
#     df['anomaly'] = anomaly_model.predict(X)
#     df['anomaly'] = df['anomaly'].apply(lambda x: True if x == -1 else False)
    
#     # Energy Prediction
#     df['predicted_energy'] = energy_model.predict(X)
    
#     return df



# src/analyze_usage.py
import os
import pandas as pd
import pickle

# Dynamically get model paths (works locally + Streamlit Cloud)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, 'models')

anomaly_model_path = os.path.join(MODEL_DIR, 'anomaly_detector.pkl')
energy_model_path = os.path.join(MODEL_DIR, 'energy_predictor.pkl')

# Load models safely
with open(anomaly_model_path, 'rb') as f:
    anomaly_model = pickle.load(f)

with open(energy_model_path, 'rb') as f:
    energy_model = pickle.load(f)

def analyze_usage(df):
    X = df[['hours_used', 'power_watts']]
    
    # Anomaly Detection
    df['anomaly'] = anomaly_model.predict(X)
    df['anomaly'] = df['anomaly'].apply(lambda x: True if x == -1 else False)
    
    # Energy Prediction
    df['predicted_energy'] = energy_model.predict(X)

    return df


