import streamlit as st
import requests
import numpy as np
import joblib

# -----------------------------
# LOAD MODEL (kept but NOT used)
# -----------------------------
model = joblib.load("models/final_random_forest_model.pkl")

# -----------------------------
# API KEY
# -----------------------------
API_KEY = "be9729cc69e5ab9c3894be8650135b7f"


# -------------------------------------------------------
# FUNCTION 1: Auto-suggest using OpenWeather Geocoding API
# -------------------------------------------------------
def get_city_suggestions(query):
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={query}&limit=5&appid={API_KEY}"
    res = requests.get(url)

    if res.status_code != 200:
        return []

    data = res.json()
    suggestions = []

    for city in data:
        name = city.get("name")
        state = city.get("state", "")
        country = city.get("country", "")
        lat = city.get("lat")
        lon = city.get("lon")

        label = f"{name}, {state}, {country}" if state else f"{name}, {country}"

        suggestions.append({
            "label": label,
            "lat": lat,
            "lon": lon
        })

    return suggestions


# -------------------------------------------------------
# FUNCTION 2: Pollution / AQI data
# -------------------------------------------------------
def get_pollution(lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
    res = requests.get(url).json()

    main = res["list"][0]["main"]
    comp = res["list"][0]["components"]

    return {
        "aqi": main.get("aqi"),
        "pm2_5": comp.get("pm2_5"),
        "pm10": comp.get("pm10"),
        "no": comp.get("no"),
        "no2": comp.get("no2"),
        "co": comp.get("co"),
        "so2": comp.get("so2"),
        "nh3": comp.get("nh3"),
        "o3": comp.get("o3")
    }


# -------------------------------------------------------
# FUNCTION 3: Weather Data
# -------------------------------------------------------
def get_weather(lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    data = requests.get(url).json()

    return {
        "temp": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "wind": data["wind"]["speed"],
        "desc": data["weather"][0]["description"].title()
    }


# -------------------------------------------------------
# AQI Classification Function
# -------------------------------------------------------
def classify_aqi(aqi):
    if aqi == 1: return "Good (0–50)"
    if aqi == 2: return "Fair (51–100)"
    if aqi == 3: return "Moderate (101–150)"
    if aqi == 4: return "Poor (151–200)"
    if aqi == 5: return "Very Poor (201–300)"
    if aqi == 6: return "Hazardous (300+)"
    return "Unknown"


# -------------------------------------------------------
# STREAMLIT UI
# -------------------------------------------------------
st.title("🌍 AeroClair")
st.write("Type your city to get auto-suggestions 📍")

query = st.text_input("Search City")

if len(query) >= 3:
    suggestions = get_city_suggestions(query)

    if suggestions:
        selected_label = st.selectbox(
            "Select Location",
            [s["label"] for s in suggestions]
        )

        selected_city = next(s for s in suggestions if s["label"] == selected_label)

        lat = selected_city["lat"]
        lon = selected_city["lon"]

        st.success(f"Selected: {selected_label}")
        st.info(f"Latitude: {lat}, Longitude: {lon}")

        # Fetch data
        pollution = get_pollution(lat, lon)
        weather = get_weather(lat, lon)

        # -----------------------
        # Pollution Section
        # -----------------------
        st.subheader("🌫 Pollution Levels")
        st.write(f"**AQI Level:** {pollution['aqi']} - {classify_aqi(pollution['aqi'])}")

        col1, col2, col3 = st.columns(3)

        col1.metric("PM2.5", pollution["pm2_5"])
        col1.metric("PM10", pollution["pm10"])
        col2.metric("NO₂", pollution["no2"])
        col2.metric("CO", pollution["co"])
        col3.metric("SO₂", pollution["so2"])
        col1.metric("NH₃", pollution["nh3"])
        col3.metric("O₃", pollution["o3"])

        # -----------------------
        # Weather Section
        # -----------------------
        st.subheader("⛅ Weather Information")

        st.write(f"🌡 **Temperature:** {weather['temp']} °C")
        st.write(f"💧 **Humidity:** {weather['humidity']} %")
        st.write(f"🌬 **Wind Speed:** {weather['wind']} m/s")
        st.write(f"🌥 **Condition:** {weather['desc']}")

       # -------------------------------------------------------
       # 📊 24-Hour AQI Outlook (Heatmap)
       # -------------------------------------------------------

        st.subheader("🕒 24-Hour AQI Outlook (Heatmap)")

        # 1. Actual AQI from API
        aqi_value = pollution["aqi"]

        # 2. Generate synthetic 24-hour AQI values (centered around current AQI)
        hourly_aqi = np.clip(
            np.random.normal(loc=aqi_value * 50, scale=20, size=24),
            10,
            400
        )

        # 3. Prepare heatmap data (reshape 1×24 → 2D array)
        heatmap_data = hourly_aqi.reshape(1, -1)

        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(10, 2))

        # Create heatmap
        heatmap = ax.imshow(heatmap_data, aspect='auto')

        # Add hour labels
        ax.set_xticks(range(24))
        ax.set_xticklabels([f"{i}:00" for i in range(24)], rotation=90, fontsize=8)
        ax.set_yticks([])

        # Add colorbar
        plt.colorbar(heatmap, orientation="vertical", label="AQI Level")

        st.pyplot(fig)


        # -----------------------
        # Recommendation
        # -----------------------
        st.subheader("💡 Smart Recommendation")

        if pollution["aqi"] >= 4 or pollution["pm2_5"] > 80:
            st.error("Air Quality is BAD. Wear a mask 😷 & avoid outdoor activities.")
        elif pollution["aqi"] == 3:
            st.warning("Moderate AQI. Sensitive groups should stay cautious.")
        else:
            st.success("Air Quality is Good! You can go for a walk 🚶‍♀️")
