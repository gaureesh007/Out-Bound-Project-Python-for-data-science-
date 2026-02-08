# =======================  ENHANCED STREAMLIT AIR QUALITY DASHBOARD  =======================
import streamlit as st
import requests
import sqlite3
import pandas as pd
import plotly.express as px
from datetime import datetime

DB_PATH = "air_quality_03.db"
CITIES = {
    "Delhi": (28.6139, 77.2090),
    "Mumbai": (19.0760, 72.8777),
    "Kolkata": (22.5726, 88.3639),
    "Chennai": (13.0827, 80.2707),
    "Lucknow": (26.8467, 80.9462),
    "Bengaluru": (12.9716, 77.5946),
    "Hyderabad": (17.3850, 78.4867),
    "Ahmedabad": (23.0225, 72.5714),
    "Varanasi": (25.3176, 82.9739),

}

# -------------------- DATABASE FUNCTIONS --------------------
def init_db(path=DB_PATH):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS air_quality_03 (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        city TEXT,
        timestamp TEXT,
        aqi INTEGER,
        aqi_label TEXT,
        co REAL,
        no REAL,
        no2 REAL,
        o3 REAL,
        so2 REAL,
        pm2_5 REAL,
        pm10 REAL,
        nh3 REAL
    )
    ''')
    conn.commit()
    return conn


@st.cache_data
def load_df_from_db(path=DB_PATH):
    conn = sqlite3.connect(path)
    df = pd.read_sql_query("SELECT * FROM air_quality_03 ORDER BY timestamp", conn)
    if not df.empty:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df


def insert_reading(conn, city, ts, aqi_value, aqi_label, components):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO air_quality_03 (city, timestamp, aqi, aqi_label, co, no, no2, o3, so2, pm2_5, pm10, nh3)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        city, ts, aqi_value, aqi_label, components.get('co'), components.get('no'), components.get('no2'),
        components.get('o3'), components.get('so2'), components.get('pm2_5'), components.get('pm10'),
        components.get('nh3')
    ))
    conn.commit()


# -------------------- API FUNCTION --------------------
def fetch_city_air(api_key, lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    
    return resp.json()


# -------------------- STREAMLIT UI --------------------
st.set_page_config(page_title="Air Quality Dashboard", layout="wide")
st.title("🌍 Air Quality Dashboard")

st.sidebar.header("Settings")
api_key = st.sidebar.text_input("Paste your OpenWeather API Key")
fetch_now = st.sidebar.button("Fetch current data for all cities")

conn = init_db()

# -------------------- AQI CATEGORY MAPS --------------------
AQI_NUMERIC_MAP = {1: 50, 2: 100, 3: 150, 4: 200, 5: 300}
AQI_LABEL_MAP = {1: "Good", 2: "Fair", 3: "Moderate", 4: "Poor", 5: "Very Poor"}

# -------------------- DATA FETCHING --------------------
if fetch_now:
    if not api_key:
        st.sidebar.error("Please enter your API key.")
    else:
        for city, (lat, lon) in CITIES.items():
            try:
                result = fetch_city_air(api_key, lat, lon)
                aqi_cat = result['list'][0]['main']['aqi']
                aqi_value = AQI_NUMERIC_MAP.get(aqi_cat, 0)  #  convert to 0–500 range
                aqi_label = AQI_LABEL_MAP.get(aqi_cat, "Unknown")
                comp = result['list'][0]['components']
                ts = datetime.utcnow().isoformat()
                insert_reading(conn, city, ts, aqi_value, aqi_label, comp)
            except Exception as e:
                st.sidebar.error(f"Failed to fetch {city}: {e}")
        st.sidebar.success("✅ Data fetched and stored successfully!")

df = load_df_from_db()

if df.empty:
    st.warning("⚠️ No data yet. Fetch data from sidebar.")
    st.stop()

# -------------------- OVERVIEW --------------------
latest = df.sort_values('timestamp').groupby('city').last().reset_index()
st.subheader("📊 Current AQI by City")
fig_aqi = px.bar(
    latest, 
    x='city', y='aqi', 
    text='aqi_label',  #  show AQI label ("Good", etc.)
    color='aqi',
    color_continuous_scale='YlOrRd',
    title='Latest AQI per City (with Category Labels)'
)
st.plotly_chart(fig_aqi, use_container_width=True)

# -------------------- POLLUTANT PIE --------------------
pollutant_cols = ['co', 'no2', 'o3', 'so2', 'pm2_5', 'pm10', 'nh3']
avg_pollutants = df[pollutant_cols].mean().reset_index()
avg_pollutants.columns = ['Pollutant', 'Value']
st.subheader("🧪 Average Pollutant Contribution")
st.plotly_chart(px.pie(avg_pollutants, names='Pollutant', values='Value', title='Average Pollutant Share'), use_container_width=True)

# -------------------- CITY COMPARISON --------------------
st.markdown("---")
st.header("🏙️ City Comparison Section")

colA, colB = st.columns(2)
with colA:
    city1 = st.selectbox("Select first city", options=df['city'].unique(), index=0)
with colB:
    city2 = st.selectbox("Select second city", options=df['city'].unique(), index=1)

if city1 and city2:
    compare_df = latest[latest['city'].isin([city1, city2])]
    fig_comp = px.bar(
        compare_df, x='city',
        y=['aqi', 'pm2_5', 'pm10', 'so2', 'no2', 'co', 'o3', 'nh3'],
        title=f"Pollutant Comparison: {city1} vs {city2}",
        barmode='group'
    )
    st.plotly_chart(fig_comp, use_container_width=True)

    hist_df = df[df['city'].isin([city1, city2])]
    fig_trend = px.line(hist_df, x='timestamp', y='aqi', color='city', title="AQI Trend Comparison (Numeric Scale)", markers=True)
    st.plotly_chart(fig_trend, use_container_width=True)

# -------------------- POLLUTANT ANALYSIS --------------------
st.markdown("---")
st.header("🔬 Individual Pollutant Analysis")

selected_pollutant = st.selectbox("Select a pollutant", pollutant_cols, index=4)
poll_df = df.groupby('city')[selected_pollutant].mean().reset_index().sort_values(selected_pollutant, ascending=False)

fig_poll_bar = px.bar(
    poll_df, x='city', y=selected_pollutant,
    title=f"Average {selected_pollutant.upper()} Levels by City",
    color='city', text=selected_pollutant
)
st.plotly_chart(fig_poll_bar, use_container_width=True)

st.subheader("Top & Bottom Cities")
col1, col2 = st.columns(2)
with col1:
    st.write("### 🏆 Top 3 Cities")
    st.dataframe(poll_df.head(3))
with col2:
    st.write("### ⚙️ Bottom 3 Cities")
    st.dataframe(poll_df.tail(3))

# -------------------- INSIGHTS --------------------
st.markdown("---")
st.subheader("💡 Automated Insights")
most_polluted = latest.loc[latest['aqi'].idxmax()]
cleanest = latest.loc[latest['aqi'].idxmin()]
st.write(f"**Most Polluted City:** {most_polluted['city']} — AQI {most_polluted['aqi']} ({most_polluted['aqi_label']})")
st.write(f"**Cleanest City:** {cleanest['city']} — AQI {cleanest['aqi']} ({cleanest['aqi_label']})")

st.caption("Tip: Fetch new data periodically to build a time history.")
