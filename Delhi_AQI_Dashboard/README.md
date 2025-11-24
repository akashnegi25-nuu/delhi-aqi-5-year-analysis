🌫️ Delhi Air Quality Dashboard — 5 Years Analysis

An interactive Streamlit dashboard built using Python, Pandas, Plotly, and Streamlit to analyze and visualize Delhi AQI (Air Quality Index) trends over the last 5 years.
The dashboard provides deep insights into pollutant levels, seasonal patterns, daily trends, and advanced visualizations.

📌 Project Overview

This project reads a CSV containing Delhi AQI data for the past 5 years and provides:

✔ Interactive filters (Year, Season, Month, Pollutant, AQI Range, Day)
✔ AQI trend analysis
✔ Pollutant-level comparison
✔ Seasonal impact study
✔ Animated visuals & 3D charts
✔ Correlation heatmaps and scatter matrices

🛠️ Tech Stack

Python 3.8+

Streamlit (Dashboard Framework)

Pandas & NumPy (Data Manipulation)

Plotly Express & Graph Objects (Interactive Visuals)

📂 Project Structure
📁 delhi-aqi-dashboard/
│-- delhi_aqi_5_years.csv
│-- app.py
│-- README.md
│-- requirements.txt

📥 Dataset

The project uses a 5-year AQI dataset for Delhi with columns:

date

aqi value

co aqi value

ozone aqi value

no2 aqi value

pm2.5 aqi value

lat, lng

Derived columns: year, month, day, season

🚀 How to Run Locally
1. Clone the Repository
git clone https://github.com/your-username/delhi-aqi-dashboard.git
cd delhi-aqi-dashboard

2. Install Dependencies

Create virtual environment (optional but recommended):

pip install -r requirements.txt


If you don’t have a requirements.txt, use:

pip install streamlit pandas numpy plotly

3. Run the Streamlit App
streamlit run app.py


Your dashboard will open in the browser. 🎉

✨ Features & Visualizations
📈 Tab 1 – Trends

Daily AQI line chart

Month-Year heatmap

Day-wise AQI pattern

🧪 Tab 2 – Pollutants

Pollutant-specific trend lines

Violin distribution chart

Radar plot for pollutant strength

🌦 Tab 3 – Seasonal Analysis

AQI by season

Seasonal pollutant comparison

Sunburst chart (Year → Season → Month)

🔥 Tab 4 – Advanced Visualizations

Animated AQI bubble chart

3D pollutant scatter plot

📊 Tab 5 – Matrix

Correlation heatmap

Scatter matrix (multivariate analysis)

📸 Screenshots

(Add screenshots here once uploaded to GitHub)

📦 requirements.txt

Use the following dependencies:

streamlit
pandas
numpy
plotly

💡 Future Enhancements

Add machine learning prediction model (AQI forecasting)

Add real-time AQI API integration

Add download/export buttons

🙌 Author

Akash Negi
Data Analyst | Python | SQL | Visualization

Feel free to connect on LinkedIn or contribute to this project!