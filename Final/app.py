import streamlit as st
import pandas as pd
#import plotly.express as px
from src.analyze_usage import analyze_usage
from src.recommendations import get_energy_recommendations, get_water_recommendations
from src.recommendations import ENERGY_LIMIT, WATER_LIMIT

st.set_page_config(page_title="🌿 EcoSenseAI Dashboard", layout="wide")
st.title("🌿 EcoSenseAI: Energy & Water Conservation")

# Load data
df = pd.read_csv("data/appliance_usage.csv")
df['date'] = pd.to_datetime(df['date'])

# Keep last 7 days
last_7_days = df['date'].max() - pd.Timedelta(days=6)
df = df[df['date'] >= last_7_days]

# Analyze
df_analyzed = analyze_usage(df)

# Recommendations (top 10) + SMS alerts triggered
energy_tips = get_energy_recommendations(df_analyzed, max_tips=10)
water_tips = get_water_recommendations(df_analyzed, max_tips=10)

# Filter alerts for dashboard display
df_energy_alerts = df_analyzed[df_analyzed['predicted_energy'] > ENERGY_LIMIT]
df_water_alerts = df_analyzed[df_analyzed['water_liters'] > WATER_LIMIT]

# Sidebar navigation
page = st.sidebar.selectbox("Select Page", ["Dashboard", "Daily Usage Graph", "Alerts"])

# --- Dashboard ---
if page == "Dashboard":
    st.subheader("📊 Daily Energy and Water Usage (Last 7 Days)")

    # Energy graph
    daily_energy = df_analyzed.groupby('date')['predicted_energy'].sum().reset_index()
    fig_energy = px.line(daily_energy, x='date', y='predicted_energy', markers=True,
                         title='Daily Energy Usage (Wh)')
    fig_energy.add_hline(y=ENERGY_LIMIT, line_dash="dash", line_color="red",
                         annotation_text="Energy Target", annotation_position="top right")
    st.plotly_chart(fig_energy, use_container_width=True)

    # Water graph
    daily_water = df_analyzed.groupby('date')['water_liters'].sum().reset_index()
    fig_water = px.line(daily_water, x='date', y='water_liters', markers=True,
                        title='Daily Water Usage (Liters)')
    fig_water.add_hline(y=WATER_LIMIT, line_dash="dash", line_color="red",
                        annotation_text="Water Target", annotation_position="top right")
    st.plotly_chart(fig_water, use_container_width=True)

    # Show all appliance usage with highlight
    st.subheader("🔹 Appliance Usage (Last 7 Days)")

    def highlight_cutoff(row):
        style = []
        style.append('background-color: #ff9999' if row['predicted_energy'] > ENERGY_LIMIT else '')
        style.append('background-color: #99ccff' if row['water_liters'] > WATER_LIMIT else '')
        return style

    df_display = df_analyzed[['date', 'appliance', 'predicted_energy', 'water_liters']].copy()
    styled_df = df_display.style.apply(
        lambda x: ['background-color: #ff9999' if x['predicted_energy'] > ENERGY_LIMIT else ''
                   for _ in x], axis=1
    ).apply(
        lambda x: ['background-color: #99ccff' if x['water_liters'] > WATER_LIMIT else ''
                   for _ in x], axis=1
    )
    st.dataframe(styled_df, height=400)

    # --- Alerts Section ---
    st.subheader("⚠️ Alerts")

    if not df_energy_alerts.empty:
        st.write("### Energy Alerts")
        for _, row in df_energy_alerts.iterrows():
            st.warning(f"{row['appliance']} consumed {row['predicted_energy']:.0f} Wh on {row['date']} (Target: {ENERGY_LIMIT} Wh)")
    else:
        st.success("No energy alerts!")

    if not df_water_alerts.empty:
        st.write("### Water Alerts")
        for _, row in df_water_alerts.iterrows():
            st.warning(f"{row['appliance']} consumed {row['water_liters']:.0f} L on {row['date']} (Target: {WATER_LIMIT} L)")
    else:
        st.success("No water alerts!")

    # --- Recommendations ---
    st.subheader("💡 Energy Recommendations (Top 10)")
    for tip in energy_tips:
        st.write(tip)

    st.subheader("💧 Water Recommendations (Top 10)")
    for tip in water_tips:
        st.write(tip)

