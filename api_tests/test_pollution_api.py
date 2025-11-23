from app.pollution_api import get_pollution_data

API_KEY = "be9729cc69e5ab9c3894be8650135b7f"

lat = 28.7041
lon = 77.1025

print(get_pollution_data(lat, lon, API_KEY))
