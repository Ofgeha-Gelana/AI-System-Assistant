import os
import streamlit as st
import subprocess
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from textblob import TextBlob
from google.genai.types import GenerateContentConfig
from google import genai

# Load environment variables
load_dotenv()

# API Keys & Config
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = "http://localhost:8080"

# --- Initialize Spotify Client ---
def initialize_spotify():
    """Authenticates and returns a Spotify client instance."""
    try:
        return spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET,
            redirect_uri=SPOTIFY_REDIRECT_URI,
            scope="playlist-read-private"
        ))
    except Exception as e:
        st.error(f"Spotify authentication failed: {e}")
        return None

sp = initialize_spotify()

# --- Brightness Control ---
def set_brightness(level: int) -> str:
    """
    Sets the system brightness level.

    Args:
        level (int): Brightness percentage (0-100).
    """
    try:
        if not 0 <= level <= 100:
            raise ValueError("Brightness must be between 0 and 100.")

        backlight_path = "/sys/class/backlight/intel_backlight/"
        if not os.path.exists(backlight_path):
            backlight_path = "/sys/class/backlight/amdgpu_bl0/"

        if not os.path.exists(backlight_path):
            return "Could not find backlight control path."

        with open(f"{backlight_path}max_brightness", "r") as f:
            max_brightness = int(f.read().strip())

        target_brightness = int((level / 100) * max_brightness)

        cmd = f"echo {target_brightness} | sudo tee {backlight_path}brightness"
        subprocess.run(cmd, shell=True, capture_output=True, text=True)

        return f"Brightness set to {level}%"
    except Exception as e:
        return f"Error setting brightness: {str(e)}"

# --- Volume Control ---
def set_volume(level: int) -> str:
    """
    Sets the system volume.

    Args:
        level (int): Volume percentage (0-100).
    """
    os.system(f"pactl set-sink-volume @DEFAULT_SINK@ {level}%")
    return f"Volume set to {level}%"

# --- Mood Detection ---
def detect_mood(text: str) -> str:
    """
    Analyzes text and determines mood.

    Args:
        text (str): Input text.

    Returns:
        str: Detected mood ('happy', 'sad', 'stressed', 'neutral', 'angry').
    """
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    text_lower = text.lower()

    if "angry" in text_lower or "mad" in text_lower:
        return "angry"
    elif "happy" in text_lower or "joy" in text_lower:
        return "happy"
    elif "sad" in text_lower or "depressed" in text_lower:
        return "sad"
    elif "stressed" in text_lower or "anxious" in text_lower:
        return "stressed"

    return "happy" if polarity > 0.3 else "sad" if polarity < -0.3 else "neutral"

# --- Spotify Music Recommendation ---
MOOD_PLAYLISTS = {
    "happy": "spotify:playlist:37i9dQZF1DXdPec7aLTmlC",
    "sad": "spotify:playlist:37i9dQZF1DX64Y3ftTBfaN",
    "stressed": "spotify:playlist:37i9dQZF1DWU0ScTcjJBdj",
    "neutral": "spotify:playlist:37i9dQZF1DX0XUsuxWHRQd",
    "angry": "spotify:playlist:37i9dQZF1DX2DCrI7t4mmy"
}

def recommend_music(mood: str) -> str:
    """
    Recommends a Spotify playlist based on mood.

    Args:
        mood (str): User's detected mood.

    Returns:
        str: Playlist link.
    """
    if not sp:
        return "Spotify integration not available."

    playlist_uri = MOOD_PLAYLISTS.get(mood, MOOD_PLAYLISTS["neutral"])
    try:
        playlist = sp.playlist(playlist_uri, market="US")
        return f"Based on your mood, listen to: {playlist['name']} - {playlist['external_urls']['spotify']}"
    except Exception as e:
        return f"Error fetching playlist: {str(e)}"

# --- Integrating Gemini AI ---
# Create Gemini Client
client = genai.Client(api_key=GEMINI_API_KEY)

# Define the Model
model_id = "gemini-2.0-flash"

# Generation Config
config = GenerateContentConfig(
    system_instruction="You are a helpful assistant that controls device settings and recommends music based on mood.",
    tools=[set_brightness, set_volume, detect_mood, recommend_music],  # Define callable functions
)

# --- Streamlit Chat UI ---
st.title("💡 AI Assistant with Device Controls & Mood-Based Music")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
user_input = st.chat_input("Ask me to adjust settings or recommend music!")

if user_input:
    # Add user input to chat
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Process the AI response
    r = client.models.generate_content(
        model=model_id,
        config=config,
        contents=user_input
    )

    ai_response = r.text

    # Add AI response to chat
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
    with st.chat_message("assistant"):
        st.markdown(ai_response)
