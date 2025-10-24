# src/train_models.py
import pandas as pd
import pickle
from sklearn.ensemble import IsolationForest, RandomForestRegressor
from sklearn.model_selection import train_test_split

# Load data
df = pd.read_csv('data/appliance_usage.csv')

# Feature engineering for energy
df['energy_consumed'] = df['hours_used'] * df['power_watts']
X = df[['hours_used', 'power_watts']]
y = df['energy_consumed']

# Train Anomaly Detection Model
iso_forest = IsolationForest(contamination=0.05, random_state=42)
iso_forest.fit(X)
with open('models/anomaly_detector.pkl', 'wb') as f:
    pickle.dump(iso_forest, f)
print("Anomaly detection model saved.")

# Train Energy Prediction Model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
regressor = RandomForestRegressor(n_estimators=100, random_state=42)
regressor.fit(X_train, y_train)
with open('models/energy_predictor.pkl', 'wb') as f:
    pickle.dump(regressor, f)
print("Energy prediction model saved.")
