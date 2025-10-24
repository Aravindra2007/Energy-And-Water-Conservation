# src/simulate_data.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def simulate_data(num_days=10):
    appliances = ['AC', 'Heater', 'Fridge', 'Washing Machine', 'Lights', 'Shower', 'Tap']
    data = []

    start_date = datetime.now() - timedelta(days=num_days)

    for i in range(num_days):
        day = start_date + timedelta(days=i)
        for appliance in appliances:
            hours_used = np.random.uniform(0, 10)  # Usage in hours
            power = np.random.uniform(50, 2000)    # Power in watts
            # Water usage for relevant appliances
            if appliance in ['Washing Machine', 'Shower', 'Tap']:
                water_liters = np.random.uniform(10, 100)
            else:
                water_liters = 0
            data.append([day.date(), appliance, round(hours_used,2), round(power,2), round(water_liters,2)])

    df = pd.DataFrame(data, columns=['date', 'appliance', 'hours_used', 'power_watts', 'water_liters'])
    df.to_csv('data/appliance_usage.csv', index=False)
    print("Simulated data saved to data/appliance_usage.csv")

if __name__ == "__main__":
    simulate_data()
