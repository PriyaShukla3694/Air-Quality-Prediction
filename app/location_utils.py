import requests
import streamlit as st

OPENWEATHER_API_KEY = st.secrets["be9729cc69e5ab9c3894be8650135b7f"]

def get_location_suggestions(query):
    """Returns list of cities matching user input"""
    if len(query) < 2:
        return []

    url = f"http://api.openweathermap.org/geo/1.0/direct?q={query}&limit=5&appid={OPENWEATHER_API_KEY}"
    response = requests.get(url)

    if response.status_code != 200:
        return []

    locations = response.json()

    suggestions = [
        f"{loc['name']}, {loc['state'] if 'state' in loc else ''} {loc['country']}"
        for loc in locations
    ]
    return suggestions


def get_lat_lon_from_city(city_name):
    """Returns latitude & longitude of selected city"""
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={OPENWEATHER_API_KEY}"
    response = requests.get(url)

    if response.status_code != 200:
        return None, None

    loc = response.json()
    if len(loc) == 0:
        return None, None

    return loc[0]["lat"], loc[0]["lon"]
