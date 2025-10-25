import os
import streamlit as st
import pandas as pd
import plotly.express as px
from src.analyze_usage import analyze_usage
from src.recommendations import get_energy_recommendations, get_water_recommendations
from src.recommendations import ENERGY_LIMIT, WATER_LIMIT

# --- Streamlit setup ---
st.set_page_config(page_title="🌿 EcoSenseAI Dashboard", layout="wide")
st.title("🌿 EcoSenseAI: Energy & Water Conservation")

# --- Load data safely ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "appliance_usage.csv")

if not os.path.exists(DATA_PATH):
    st.error("❌ Data file not found: `data/appliance_usage.csv`\n\nPlease ensure the file exists in the `data/` folder.")
    st.stop()

df = pd.read_csv(DATA_PATH)

# --- Preprocess ---
if 'date' not in df.columns:
    st.error("❌ Missing 'date' column in CSV file.")
    st.stop()

df['date'] = pd.to_datetime(df['date'], errors='coerce')
df = df.dropna(subset=['date'])

# Keep last 7 days
last_7_days = df['date'].max() - pd.Timedelta(days=6)
df = df[df['date'] >= last_7_days]

# --- Analyze usage ---
df_analyzed = analyze_usage(df)

# --- Generate recommendations ---
energy_tips = get_energy_recommendations(df_analyzed, max_tips=10)
water_tips = get_water_recommendations(df_analyzed, max_tips=10)

# --- Alerts ---
df_energy_alerts = df_analyzed[df_analyzed['predicted_energy'] > ENERGY_LIMIT]
df_water_alerts = df_analyzed[df_analyzed['water_liters'] > WATER_LIMIT]

# --- Sidebar navigation ---
page = st.sidebar.selectbox("Select Page", ["Dashboard", "Daily Usage Graph", "Alerts"])

# --- DASHBOARD PAGE ---
if page == "Dashboard":
    st.subheader("📊 Daily Energy and Water Usage (Last 7 Days)")

    # Energy usage graph
    daily_energy = df_analyzed.groupby('date')['predicted_energy'].sum().reset_index()
    fig_energy = px.line(
        daily_energy, x='date', y='predicted_energy', markers=True,
        title='Daily Energy Usage (Wh)'
    )
    fig_energy.add_hline(
        y=ENERGY_LIMIT, line_dash="dash", line_color="red",
        annotation_text="Energy Target", annotation_position="top right"
    )
    st.plotly_chart(fig_energy, use_container_width=True)

    # Water usage graph
    daily_water = df_analyzed.groupby('date')['water_liters'].sum().reset_index()
    fig_water = px.line(
        daily_water, x='date', y='water_liters', markers=True,
        title='Daily Water Usage (Liters)'
    )
    fig_water.add_hline(
        y=WATER_LIMIT, line_dash="dash", line_color="red",
        annotation_text="Water Target", annotation_position="top right"
    )
    st.plotly_chart(fig_water, use_container_width=True)

    # Appliance usage table with highlights
    st.subheader("🔹 Appliance Usage (Last 7 Days)")
    df_display = df_analyzed[['date', 'appliance', 'predicted_energy', 'water_liters']].copy()

    def highlight_cutoff(row):
        color = ""
        if row['predicted_energy'] > ENERGY_LIMIT:
            color = 'background-color: #ff9999'  # red shade
        elif row['water_liters'] > WATER_LIMIT:
            color = 'background-color: #99ccff'  # blue shade
        return [color] * len(row)

    styled_df = df_display.style.apply(highlight_cutoff, axis=1)
    st.dataframe(styled_df, height=400)


    # Alerts section
    st.subheader("⚠️ Alerts")
    if not df_energy_alerts.empty:
        st.write("### Energy Alerts")
        for _, row in df_energy_alerts.iterrows():
            st.warning(f"⚡ {row['appliance']} consumed {row['predicted_energy']:.0f} Wh on {row['date'].date()} (Target: {ENERGY_LIMIT} Wh)")
    else:
        st.success("✅ No energy alerts!")

    if not df_water_alerts.empty:
        st.write("### Water Alerts")
        for _, row in df_water_alerts.iterrows():
            st.warning(f"🚰 {row['appliance']} consumed {row['water_liters']:.0f} L on {row['date'].date()} (Target: {WATER_LIMIT} L)")
    else:
        st.success("✅ No water alerts!")

    # Recommendations section
    st.subheader("💡 Energy Recommendations (Top 10)")
    for tip in energy_tips:
        st.write(f"• {tip}")

    st.subheader("💧 Water Recommendations (Top 10)")
    for tip in water_tips:
        st.write(f"• {tip}")


















