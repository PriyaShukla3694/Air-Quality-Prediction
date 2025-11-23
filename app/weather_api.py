import streamlit as st
import requests

st.title("🌤 Weather API Test")

API_KEY = 'be9729cc69e5ab9c3894be8650135b7f'

city = st.text_input("Enter city name", "Delhi")

if st.button("Get Weather"):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        st.success("API Working Successfully!")

        st.write("### 🌡 Temperature:", data['main']['temp'], "°C")
        st.write("### 💧 Humidity:", data['main']['humidity'], "%")
        st.write("### 🌬 Wind Speed:", data['wind']['speed'], "m/s")
        st.write("### 📍 Location Coordinates:", data['coord'])
        st.write("### 🌥 Weather Description:", data['weather'][0]['description'].title())

    else:
        st.error("API Error: " + str(response.status_code))
