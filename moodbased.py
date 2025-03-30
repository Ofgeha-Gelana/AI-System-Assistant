import os
import random
import requests
import pyttsx3
import streamlit as st
from google.genai.types import GenerateContentConfig
from google import genai
from spotipy.oauth2 import SpotifyOAuth
import spotipy
from textblob import TextBlob

# Spotify Credentials (Set up your Spotify Developer Account and get these)
SPOTIFY_CLIENT_ID = "2d960f832ebd4b92aa2052637c52217d"
SPOTIFY_CLIENT_SECRET = "c3b86a96a47143bd829e39ed9f98beb2"
SPOTIFY_REDIRECT_URI = "http://localhost:8080"

# Authenticate Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope="user-modify-playback-state user-read-playback-state"
))

# Mood-based Spotify Playlist IDs
MOOD_PLAYLISTS = {
    "happy": "spotify:playlist:your_happy_playlist_id",
    "sad": "spotify:playlist:your_sad_playlist_id",
    "stressed": "spotify:playlist:your_stressed_playlist_id",
    "neutral": "spotify:playlist:your_chill_playlist_id"
}

# Function to detect mood based on text sentiment
def detect_mood(text: str) -> str:
    """Analyzes the sentiment of the input text and determines the mood."""
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    
    if polarity > 0.3:
        return "happy"
    elif polarity < -0.3:
        return "sad"
    elif -0.3 <= polarity <= 0.3:
        return "neutral"
    else:
        return "stressed"

# Function to play music based on mood
def play_music(mood: str):
    """Plays a Spotify playlist based on the detected mood."""
    playlist_uri = MOOD_PLAYLISTS.get(mood)
    if playlist_uri:
        devices = sp.devices()
        if devices['devices']:
            device_id = devices['devices'][0]['id']
            sp.start_playback(device_id=device_id, context_uri=playlist_uri)
            st.success(f"Playing {mood} playlist on Spotify!")
        else:
            st.error("No active Spotify device found!")
    else:
        st.warning("No playlist found for this mood!")

# Function to fetch a joke from Joke API or Gemini
def get_joke() -> str:
    """Fetches a joke from the API or Gemini."""
    joke = ""
    try:
        response = client.models.generate_content(
            model=model_id,
            config=config,
            contents="Tell me a programming joke."
        )
        joke = response.text  # Grab the joke from the response.
    except Exception as e:
        st.error(f"Error fetching joke from Gemini: {e}")
    return joke or "Oops! Couldn't fetch a joke."

# Function to read the joke aloud using text-to-speech
def tell_joke(joke: str):
    """Reads the joke aloud using text-to-speech."""
    tts = pyttsx3.init()
    tts.say("Here's a joke for you!")
    tts.say(joke)
    tts.runAndWait()

# Function to set the system volume
def set_volume(level: int):
    """Sets the system volume."""
    os.system(f"pactl set-sink-volume @DEFAULT_SINK@ {level}%")

# Initialize Gemini Client (replace with your API key)
API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)
model_id = "gemini-2.0-flash"  # You may need to adjust this based on your model.

# Define the model's configuration with callable references for the tools
config = GenerateContentConfig(
    system_instruction="You are a helpful assistant that can play mood-based music and tell jokes.",
    tools=[play_music, get_joke, detect_mood],  # Pass the actual function references here
)

def main():
    st.title("Mood-Based Music & Joke Assistant 🎵😂")

    user_input = st.text_input("How are you feeling today?")
    
    if st.button("Analyze Mood & Play Music"):
        # Use Gemini to analyze the mood or fall back to TextBlob.
        mood = detect_mood(user_input)
        st.write(f"Detected mood: {mood}")
        set_volume(50)
        play_music(mood)
        
        if mood in ["sad", "stressed"]:
            joke = get_joke()
            st.write("Joke:", joke)
            tell_joke(joke)

if __name__ == "__main__":
    main()
