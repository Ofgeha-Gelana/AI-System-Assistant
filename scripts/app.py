import streamlit as st
import google.generativeai as genai
import requests
import os
from dotenv import load_dotenv

# Load API keys from .env file
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Function to get weather from OpenWeather API
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temp = data["main"]["temp"]
        return temp
    else:
        return None

# Streamlit UI
st.title("AI-Powered Weather & PC Control")

# Get city input
city = st.text_input("Enter city name:", "New York")

if st.button("Check Weather"):
    temp = get_weather(city)
    if temp is not None:
        st.write(f"Current Temperature in {city}: **{temp}°C**")
        
        # Ask user for shutdown confirmation
        shutdown_confirm = st.radio("Do you want to switch off the PC?", ["No", "Yes"])
        
        if shutdown_confirm == "Yes":
            st.warning("Switching off PC...")
            os.system("shutdown /s /t 0")  # Windows shutdown command
        else:
            st.success("PC will remain ON.")
    else:
        st.error("Failed to fetch weather data.")
