import os
import requests
import pyttsx3
import streamlit as st
from google.genai.types import GenerateContentConfig
from google import genai
from spotipy.oauth2 import SpotifyOAuth
import spotipy
from textblob import TextBlob
from datetime import datetime

# Spotify Credentials
SPOTIFY_CLIENT_ID = "2d960f832ebd4b92aa2052637c52217d"
SPOTIFY_CLIENT_SECRET = "c3b86a96a47143bd829e39ed9f98beb2"
SPOTIFY_REDIRECT_URI = "http://localhost:8080"

# Mood-based Spotify Playlist IDs (Verified public playlists, March 2025)
MOOD_PLAYLISTS = {
    "happy": "spotify:playlist:37i9dQZF1DXdPec7aLTmlC",    # Happy Hits!
    "sad": "spotify:playlist:37i9dQZF1DX64Y3ftTBfaN",      # Sad Bops (new, verified)
    "stressed": "spotify:playlist:37i9dQZF1DWU0ScTcjJBdj",  # Stress Relief
    "neutral": "spotify:playlist:37i9dQZF1DX0XUsuxWHRQd",   # Chill Hits
    "angry": "spotify:playlist:37i9dQZF1DX2DCrI7t4mmy"      # Angry Punk (new, verified)
}

# Function to detect mood based on text sentiment and keywords
def detect_mood(text: str) -> str:
    """Analyzes sentiment and keywords to determine mood."""
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    text_lower = text.lower()

    # Keyword-based overrides
    if "angry" in text_lower or "mad" in text_lower or "hit" in text_lower:
        return "angry"
    elif "happy" in text_lower or "great" in text_lower:
        return "happy"
    elif "sad" in text_lower or "down" in text_lower:
        return "sad"
    elif "stressed" in text_lower or "anxious" in text_lower:
        return "stressed"
    
    # Fallback to polarity
    if polarity > 0.3:
        return "happy"
    elif polarity < -0.3:
        return "sad"
    elif -0.3 <= polarity <= 0.3:
        return "neutral"
    else:
        return "stressed"

# Function to fetch a joke
def get_joke() -> str:
    """Fetches a joke from Gemini."""
    try:
        response = client.models.generate_content(
            model=model_id,
            config=config,
            contents="Tell me a short, funny programming joke."
        )
        return response.text.strip()
    except Exception as e:
        st.error(f"Error fetching joke: {e}")
        return "Why do programmers prefer dark mode? Because the light attracts bugs."

# Function to suggest a playlist based on mood
def suggest_playlist(mood: str) -> tuple[str, str]:
    """Suggests a Spotify playlist based on the mood and returns its name and link."""
    playlist_uri = MOOD_PLAYLISTS.get(mood, MOOD_PLAYLISTS["neutral"])
    try:
        playlist = sp.playlist(playlist_uri, market="US")  # Specify market to avoid region issues
        playlist_name = playlist["name"]
        playlist_link = playlist["external_urls"]["spotify"]
        return playlist_name, playlist_link
    except Exception as e:
        st.error(f"Error fetching playlist: {e}")
        return "Fallback Playlist", f"https://open.spotify.com/playlist/{playlist_uri.split(':')[-1]}"

# Function to save playlist suggestion
def save_playlist(mood: str, playlist_name: str, playlist_link: str, description: str):
    """Saves the playlist suggestion and description to a file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] Mood: {mood}\nPlaylist: {playlist_name} ({playlist_link})\nDescription: {description}\n\n"
    with open("playlist_log.txt", "a") as file:
        file.write(entry)

# Function to set system volume (Linux-specific)
def set_volume(level: int):
    """Sets the system volume."""
    try:
        os.system(f"pactl set-sink-volume @DEFAULT_SINK@ {level}%")
    except Exception:
        st.warning("Volume adjustment not supported.")

# Function to read text aloud with better TTS handling
def tell_text(text: str):
    """Reads text aloud using text-to-speech with error handling."""
    try:
        tts = pyttsx3.init()
        tts.setProperty("rate", 150)
        tts.say(text)
        tts.runAndWait()
        tts.stop()  # Explicitly stop to prevent reference errors
        del tts     # Clean up the object
    except Exception as e:
        st.warning(f"Text-to-speech failed: {e}")

# Authenticate Spotify
try:
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope="playlist-read-private"
    ))
except Exception as e:
    st.error(f"Spotify authentication failed: {e}")

# Initialize Gemini Client
API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)
model_id = "gemini-2.0-flash"
config = GenerateContentConfig(
    system_instruction="You are a helpful assistant that enhances mood with music suggestions and humor.",
    tools=[detect_mood, get_joke]
)

# Streamlit UI
def main():
    st.title("🎵 Mood-Based Music & Joke Assistant 😂")
    st.write("Tell me how you’re feeling, and I’ll suggest a playlist to match your mood!")

    # Mood input
    user_input = st.text_input("How are you feeling today? (e.g., happy, sad, stressed)")

    if st.button("Get Music Suggestion"):
        if user_input:
            # Detect mood
            mood = detect_mood(user_input)
            st.write(f"Detected mood: **{mood}**")

            # Suggest playlist
            playlist_name, playlist_link = suggest_playlist(mood)
            description = f"Enjoy a {mood} vibe with '{playlist_name}'—open it in Spotify and let the music lift you!"
            st.write(f"**Suggested Playlist:** [{playlist_name}]({playlist_link})")
            st.write(f"**Description:** {description}")

            # Save suggestion
            save_playlist(mood, playlist_name, playlist_link, description)

            # Set volume and read description
            set_volume(50)
            
            # Add joke for sad, stressed, or angry moods
            if mood in ["sad", "stressed", "angry"]:
                joke = get_joke()
                st.write(f"**Here’s a joke to cheer you up:** {joke}")
                tell_text(f"Here’s a playlist suggestion for your {mood} mood: {description} Plus a joke: {joke}")
            else:
                tell_text(description)
        else:
            st.error("Please enter how you’re feeling!")

if __name__ == "__main__":
    main()