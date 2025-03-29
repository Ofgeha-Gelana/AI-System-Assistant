import streamlit as st
import google.generativeai as genai
import os
import time
import re
import pygame
from datetime import datetime
from dotenv import load_dotenv

# Load API keys from .env file
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Function to ask Gemini to confirm alarm
def confirm_alarm(user_input):
    prompt = f"User wants to set an alarm for {user_input}. Confirm the time and format as HH:MM AM/PM."
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text.strip()

# Function to extract and correctly format time
def extract_time(response_text):
    match = re.search(r"(\d{1,2}):(\d{2}) ?(AM|PM)?", response_text)
    if match:
        hour, minute = int(match.group(1)), int(match.group(2))
        period = match.group(3)  # Extract AM or PM if present

        if period:
            return f"{hour}:{minute:02d} {period}"  # Already in correct 12-hour format
        else:
            # Convert 24-hour format to 12-hour format
            period = "AM" if hour < 12 else "PM"
            hour = hour if 1 <= hour <= 12 else hour - 12
            return f"{hour}:{minute:02d} {period}"
    return None  # Handle extraction failure

# Function to play alarm sound
def play_alarm():
    pygame.mixer.init()
    pygame.mixer.music.load("Astu.mp3")  # Ensure you have 'alarm.mp3'
    pygame.mixer.music.play()

# Streamlit UI
st.title("🔔 AI-Powered Alarm Clock (Linux)")

# User inputs time for alarm
alarm_time = st.text_input("Enter alarm time (e.g., 7:30 AM):")

if st.button("Set Alarm"):
    if alarm_time:
        confirmed_time = extract_time(confirm_alarm(alarm_time))

        if confirmed_time:
            st.success(f"Alarm set for {confirmed_time}")

            # Convert to 24-hour time for checking
            alarm_datetime = datetime.strptime(confirmed_time, "%I:%M %p").time()

            st.write("Waiting for alarm time...")

            while True:
                now = datetime.now().time()
                if now.hour == alarm_datetime.hour and now.minute == alarm_datetime.minute:
                    play_alarm()
                    break
                time.sleep(10)  # Check every 10 seconds

            # Ask if user wants to shut down PC
            shutdown_confirm = st.radio("Do you want to shut down the PC after the alarm?", ["No", "Yes"])
            if shutdown_confirm == "Yes":
                st.warning("Shutting down PC...")
                os.system("shutdown now")  # Linux shutdown command
        else:
            st.error("Failed to extract a valid time. Please try again.")
    else:
        st.error("Please enter a valid alarm time.")
