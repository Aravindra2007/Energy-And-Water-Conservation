# src/recommendations.py
from twilio_alerts import send_sms_alert

# Cut-off limits
ENERGY_LIMIT = 3000  # Wh
WATER_LIMIT = 150     # liters

# Track which appliances have been alerted (avoid duplicate SMS)
sent_energy_alerts = set()
sent_water_alerts = set()

def get_energy_recommendations(df, max_tips=10):
    tips = []
    for _, row in df.iterrows():
        key = (row['appliance'], row['date'])
        if row.get('predicted_energy', 0) > ENERGY_LIMIT and key not in sent_energy_alerts:
            # Recommendation for dashboard
            tip = f"⚠️ {row['appliance']} exceeded energy target ({row['predicted_energy']:.0f} Wh > {ENERGY_LIMIT} Wh) on {row['date']}."
            tips.append(tip)
            # SMS notification
            try:
                send_sms_alert(f"Energy Alert! {row['appliance']} crossed {ENERGY_LIMIT} Wh on {row['date']}.")
                sent_energy_alerts.add(key)
            except:
                pass
        if len(tips) >= max_tips:
            break
    return tips

def get_water_recommendations(df, max_tips=10):
    tips = []
    for _, row in df.iterrows():
        key = (row['appliance'], row['date'])
        if row.get('water_liters', 0) > WATER_LIMIT and key not in sent_water_alerts:
            tip = f"⚠️ {row['appliance']} exceeded water target ({row['water_liters']:.0f} L > {WATER_LIMIT} L) on {row['date']}."
            tips.append(tip)
            try:
                send_sms_alert(f"Water Alert! {row['appliance']} crossed {WATER_LIMIT} L on {row['date']}.")
                sent_water_alerts.add(key)
            except:
                pass
        if len(tips) >= max_tips:
            break
    return tips

