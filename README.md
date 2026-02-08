# Out-Bound-Project-Python-for-data-science-
The project i have created to submit in my college for summer training from IIT kanpur 
# 🌍 Air Quality Dashboard (India Cities)

An interactive **Air Quality Monitoring Dashboard** built with **Streamlit**, allowing users to fetch, store, analyze, and visualize air pollution data for major Indian cities.

The dashboard retrieves live air quality data from the **OpenWeather API**, stores it locally using SQLite, and presents insights using interactive charts.

---

## 🚀 Project Overview
This application helps users:

- Monitor air quality across cities
- Compare pollution levels
- Track AQI trends over time
- Analyze pollutant contributions
- Generate automatic pollution insights

Data is stored locally, allowing historical trend tracking.

---

## ✨ Features

### 📡 Live Data Fetching
- Fetch real-time air quality data
- Supports multiple cities
- Data stored locally for analysis

### 🏙 City AQI Overview
- Bar chart of latest AQI values
- Category labels: Good, Fair, Moderate, Poor, Very Poor

### 🧪 Pollutant Contribution
- Pie chart showing pollutant distribution
- Average pollutant contribution

### 🏙️ City Comparison
- Compare two cities across pollutants
- AQI trend comparison over time

### 🔬 Pollutant Analysis
- City-wise pollutant ranking
- Top & bottom polluted cities

### 💡 Automated Insights
- Most polluted city
- Cleanest city
- Dynamic recommendations

---

## 🧠 Technologies Used

| Component | Technology |
|-----------|-----------|
| Frontend Dashboard | Streamlit |
| Data Storage | SQLite |
| API Source | OpenWeather API |
| Data Handling | Pandas |
| Visualization | Plotly |
| Backend | Python |

---

2️⃣ Install dependencies
pip install streamlit requests pandas plotly

3️⃣ Get API Key
Create free API key at:
https://openweathermap.org/api

4️⃣ Run app
streamlit run app.py

📊 Dashboard Sections
Current AQI Overview
Displays latest AQI values per city.
Pollutant Share
Pie chart of pollutant concentration.
City Comparison
Compare pollutant levels and AQI trends.
Pollutant Ranking
City ranking per pollutant.
Automated Insights
Highlights cleanest and most polluted cities.

⏱ Workflow
API Fetch → Database Storage → Data Analysis → Visualization → Insights

📈 AQI Category Mapping
AQI Category	Numeric Scale
Good	50
Fair	100
Moderate	150
Poor	200
Very Poor	300
🔮 Future Improvements

Possible upgrades:
Forecast prediction using ML
Real-time auto updates
Map-based visualization
Health recommendations
Mobile-friendly layout
Pollution alerts
Export reports (PDF/CSV)

🎯 Learning Outcomes
This project demonstrates:
API integration
Data persistence
Dashboard creation
Data visualization
Time-series analysis
Python full-stack mini project

👨‍💻 Author
Gaureesh
B.Tech Computer Science Engineer

📄 License
Open-source for academic and educational use.

⭐ Contribution
Contributions and improvements are welcome.


