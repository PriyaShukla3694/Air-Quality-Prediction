import requests
import streamlit as st

def get_pollution_data(lat, lon, api_key):
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch pollution data. Please check the coordinates or API key.")
        return None
