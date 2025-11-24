import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ------------------------------------
# Load Data
# ------------------------------------
data = pd.read_csv("delhi_aqi_5_years.csv")
data.columns = [c.strip().lower() for c in data.columns]

data["date"] = pd.to_datetime(data["date"])
data["year"] = data["date"].dt.year
data["month"] = data["date"].dt.month
data["day"] = data["date"].dt.day_name()

def season(month):
    if month in [12,1,2]: return "Winter"
    if month in [3,4,5]: return "Summer"
    if month in [6,7,8,9]: return "Monsoon"
    return "Autumn"

data["season"] = data["month"].apply(season)

pollutants = ["co aqi value", "ozone aqi value", "no2 aqi value", "pm2.5 aqi value"]

# ------------------------------------
# Streamlit Page Settings
# ------------------------------------
st.set_page_config(page_title="Delhi AQI Dashboard", layout="wide")
st.title("🌫️ Delhi Air Quality Dashboard — 5 Years Interactive View")

# ------------------------------------
# Sidebar Filters
# ------------------------------------
st.sidebar.header("🔍 Filters")

year_f = st.sidebar.multiselect(
    "Select Year", sorted(data["year"].unique()),
    default=sorted(data["year"].unique())
)
season_f = st.sidebar.multiselect(
    "Select Season", ["Winter","Summer","Monsoon","Autumn"],
    default=["Winter","Summer","Monsoon","Autumn"]
)
month_f = st.sidebar.slider("Month Range", 1, 12, (1, 12))
pollutant_f = st.sidebar.selectbox("Select Pollutant", pollutants)
aqi_range = st.sidebar.slider("Filter AQI Range", 
                              int(data["aqi value"].min()),
                              int(data["aqi value"].max()),
                              (int(data["aqi value"].min()),
                               int(data["aqi value"].max())))
day_f = st.sidebar.multiselect(
    "Select Day", 
    ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
    default=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
)

df = data[
    (data["year"].isin(year_f)) &
    (data["season"].isin(season_f)) &
    (data["month"].between(month_f[0], month_f[1])) &
    (data["aqi value"].between(aqi_range[0], aqi_range[1])) &
    (data["day"].isin(day_f))
]

# ------------------------------------
# KPI Metrics
# ------------------------------------
st.subheader("📌 Summary Metrics")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Avg AQI", round(df["aqi value"].mean(),2))
c2.metric("Max AQI", round(df["aqi value"].max(),2))
c3.metric("Min AQI", round(df["aqi value"].min(),2))
c4.metric("Records", len(df))

# ------------------------------------
# TABS
# ------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["📈 Trends", "🧪 Pollutants", "🌦 Seasonal", "🔥 Advanced", "📊 Matrix"]
)

# ------------------------------------
# TAB 1: TRENDS
# ------------------------------------
with tab1:
    st.subheader("📈 AQI Trends")

    # AQI Timeline
    fig = px.line(df, x="date", y="aqi value", color="year", markers=True,
                  title="AQI Trend Over Time")
    st.plotly_chart(fig, use_container_width=True)

    # Calendar Heatmap
    st.subheader("🗓️ Calendar Heatmap (Month vs Year)")
    cal = df.groupby(["year","month"])["aqi value"].mean().reset_index()
    fig2 = px.density_heatmap(cal, x="month", y="year", z="aqi value",
                              title="AQI Heatmap by Month and Year",
                              text_auto=True)
    st.plotly_chart(fig2, use_container_width=True)

    # Daily Pattern
    st.subheader("📅 Day of Week Pattern")
    daily = df.groupby("day")["aqi value"].mean().reindex(
        ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    )
    fig3 = px.bar(daily, title="AQI by Day of Week", text_auto=True)
    st.plotly_chart(fig3, use_container_width=True)

# ------------------------------------
# TAB 2: POLLUTANTS
# ------------------------------------
with tab2:
    st.subheader("🧪 Pollutant Trends")

    # Selected Pollutant Trend
    fig4 = px.line(df, x="date", y=pollutant_f, color="season",
                   title=f"{pollutant_f.upper()} Trend Over Time")
    st.plotly_chart(fig4, use_container_width=True)

    # Violin Plot
    st.subheader("📦 Pollutant Distribution")
    fig5 = px.violin(df, y=pollutants, box=True, points="all",
                     title="Pollutant Distribution (Violin Plot)")
    st.plotly_chart(fig5, use_container_width=True)

    # Radar Chart for Pollutant Strength
    st.subheader("🧭 Pollutant Radar Chart")
    avg = df[pollutants].mean()
    radar = go.Figure(data=go.Scatterpolar(
        r=avg.values,
        theta=[p.upper() for p in pollutants],
        fill='toself'
    ))
    radar.update_layout(title="Pollutant Strength Radar Plot")
    st.plotly_chart(radar, use_container_width=True)

# ------------------------------------
# TAB 3: SEASONAL
# ------------------------------------
with tab3:
    st.subheader("🌦 Seasonal AQI Analysis")

    seasonal = df.groupby("season")["aqi value"].mean().reset_index()
    fig6 = px.bar(seasonal, x="season", y="aqi value", text_auto=True,
                  title="AQI by Season")
    st.plotly_chart(fig6, use_container_width=True)

    # Seasonal Pollutant Line Chart
    st.subheader("🧪 Seasonal Pollutant Levels")
    sp = df.groupby("season")[pollutants].mean().reset_index()
    fig7 = px.line(sp, x="season", y=pollutants, markers=True,
                   title="Pollutant Levels Across Seasons")
    st.plotly_chart(fig7, use_container_width=True)

    # Sunburst
    st.subheader("🌸 Sunburst: Year → Season → Month")
    fig8 = px.sunburst(df, path=["year","season","month"], 
                       values="aqi value",
                       title="AQI Sunburst Breakdown")
    st.plotly_chart(fig8, use_container_width=True)

# ------------------------------------
# TAB 4: ADVANCED VISUALIZATIONS
# ------------------------------------
with tab4:
    st.subheader("🔥 Advanced Visuals")

    # Animated AQI Bubble Chart
    fig_bubble = px.scatter(df, x="no2 aqi value", y="aqi value",
                      animation_frame="year", size="pm2.5 aqi value",
                      color="season",
                      title="Animated AQI Bubble Chart")
    fig_bubble.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 2100  
    fig_bubble.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 1000

    st.plotly_chart(fig_bubble, use_container_width=True)

    # 3D Scatter Plot
    st.subheader("🌀 3D Visualization (NO2 vs AQI vs PM2.5)")
    fig10 = px.scatter_3d(
        df, x="no2 aqi value", y="aqi value", z="pm2.5 aqi value",
        color="season", title="3D AQI Visualization",
        height=600
    )
    
    st.plotly_chart(fig10, use_container_width=True)

# ------------------------------------
# TAB 5: MATRIX & CORRELATION
# ------------------------------------
with tab5:
    st.subheader("📊 Correlation Matrix")

    fig11 = px.imshow(df[["aqi value"] + pollutants].corr(),
                      text_auto=True,
                      title="AQI Correlation Heatmap")
    st.plotly_chart(fig11, use_container_width=True)

    st.subheader("🔍 Scatter Matrix")
    fig12 = px.scatter_matrix(df, dimensions=["aqi value"] + pollutants,
                              color="season",
                              title="Scatter Matrix")
    st.plotly_chart(fig12, use_container_width=True)
