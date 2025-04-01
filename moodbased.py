import os
import streamlit as st
import subprocess
from dotenv import load_dotenv
import google.generativeai as gen_ai
from textblob import TextBlob
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime
import random
from difflib import get_close_matches

# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Mood-Based Music Assistant",
    page_icon="🎵",
    layout="centered",
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = "http://localhost:8080"

# Expanded Mood-based Spotify Playlist IDs
MOOD_PLAYLISTS = {
    "happy": [
        "spotify:playlist:37i9dQZF1DXdPec7aLTmlC",  # Happy Hits!
        "spotify:playlist:37i9dQZF1DX9u7XXOp0l5L",  # Mood Booster
        "spotify:playlist:37i9dQZF1DX1H4LbvY4OJi"   # Happy Pop
    ],
    "sad": [
        "spotify:playlist:37i9dQZF1DX64Y3ftTBfaN",  # Sad Bops
        "spotify:playlist:37i9dQZF1DX7qK8ma5wgG1",  # Sad Songs
        "spotify:playlist:37i9dQZF1DWVrtsSlLKzro"   # Heartbreak Hotel
    ],
    "stressed": [
        "spotify:playlist:37i9dQZF1DWU0ScTcjJBdj",  # Stress Relief
        "spotify:playlist:37i9dQZF1DWZqd5JICZI0u",  # Peaceful Piano
        "spotify:playlist:37i9dQZF1DX8mWv7JDZ0Ht"   # Chill + Atmospheric
    ],
    "neutral": [
        "spotify:playlist:37i9dQZF1DX0XUsuxWHRQd",  # Chill Hits
        "spotify:playlist:37i9dQZF1DX4WYpdgoIcn6",  # Chill Hits
        "spotify:playlist:37i9dQZF1DX4SBhb3fqCJd"   # Relax & Unwind
    ],
    "angry": [
        "spotify:playlist:37i9dQZF1DX2DCrI7t4mmy",  # Angry Punk
        "spotify:playlist:37i9dQZF1DX3LDIBRoaCDQ",  # Metal Essentials
        "spotify:playlist:37i9dQZF1DX6GwdWRQMQpq"   # Feel Good Rock
    ],
    "energetic": [
        "spotify:playlist:37i9dQZF1DX0vHZ8elq0UK",  # Energy Booster
        "spotify:playlist:37i9dQZF1DX76Wlfdnj7AP",  # Beast Mode
        "spotify:playlist:37i9dQZF1DX1lVhptIYRda"   # Hot Hits
    ]
}

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-1.5-flash')

# Initialize Spotify client
try:
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope="playlist-read-private"
    ))
except Exception as e:
    st.error(f"Spotify authentication failed: {e}")
    sp = None

# Brightness control function
def set_brightness(percentage):
    try:
        if not 0 <= percentage <= 100:
            raise ValueError("Brightness must be between 0 and 100")

        backlight_path = "/sys/class/backlight/intel_backlight/"
        if not os.path.exists(backlight_path):
            backlight_path = "/sys/class/backlight/amdgpu_bl0/"
        
        if not os.path.exists(backlight_path):
            return "Could not find backlight control path"

        with open(f"{backlight_path}max_brightness", "r") as f:
            max_brightness = int(f.read().strip())

        target_brightness = int((percentage / 100) * max_brightness)
        
        cmd = f"echo {target_brightness} | sudo tee {backlight_path}brightness"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            return f"Brightness set to {percentage}%"
        else:
            return f"Failed: {result.stderr or 'Unknown error'}"
    except Exception as e:
        return f"Error: {str(e)}"

def get_current_brightness():
    try:
        backlight_path = "/sys/class/backlight/intel_backlight/"
        if not os.path.exists(backlight_path):
            backlight_path = "/sys/class/backlight/amdgpu_bl0/"
        
        if not os.path.exists(backlight_path):
            return 50

        with open(f"{backlight_path}max_brightness", "r") as f:
            max_brightness = int(f.read().strip())
        with open(f"{backlight_path}brightness", "r") as f:
            current = int(f.read().strip())
        
        return int((current / max_brightness) * 100)
    except:
        return 50

# Volume control function
def set_volume(percentage):
    try:
        if not 0 <= percentage <= 100:
            raise ValueError("Volume must be between 0 and 100")

        cmd = f"amixer -q sset Master {percentage}%"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            return f"Volume set to {percentage}%"
        else:
            cmd = f"echo '{percentage}' | sudo tee /proc/self/fd/0 | amixer -q sset Master $(cat -)%"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                return f"Volume set to {percentage}%"
            else:
                return f"Failed: {result.stderr or 'Unknown error'}"
    except Exception as e:
        return f"Error: {str(e)}"

def get_current_volume():
    try:
        cmd = "amixer sget Master"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            for line in result.stdout.splitlines():
                if "Playback" in line and "%" in line:
                    percentage = int(line.split("[")[1].split("%")[0])
                    return percentage
        return 50
    except:
        return 50

# Enhanced mood detection from chat history
def detect_mood_from_history(chat_history):
    """Analyzes entire chat history for mood detection"""
    if not chat_history:
        return "neutral"
    
    full_text = " ".join([msg.parts[0].text for msg in chat_history if msg.role == "user"])
    
    # Enhanced keyword analysis with weights
    mood_keywords = {
        "happy": {"joy": 2, "happy": 2, "great": 1, "wonderful": 1, "awesome": 1, "excited": 1, "love": 1},
        "sad": {"sad": 2, "depressed": 2, "down": 1, "lonely": 1, "cry": 1, "miss": 1, "hurt": 1},
        "angry": {"angry": 2, "mad": 2, "furious": 1, "annoyed": 1, "hate": 1, "upset": 1},
        "stressed": {"stressed": 2, "anxious": 2, "overwhelmed": 1, "pressure": 1, "tense": 1, "nervous": 1},
        "energetic": {"energetic": 2, "pumped": 1, "workout": 1, "exercise": 1, "run": 1, "active": 1},
        "relaxed": {"relax": 2, "calm": 1, "peaceful": 1, "chill": 1, "zen": 1, "mellow": 1}
    }
    
    # Count weighted keyword matches
    mood_scores = {mood: 0 for mood in mood_keywords}
    for mood, keywords in mood_keywords.items():
        for keyword, weight in keywords.items():
            mood_scores[mood] += full_text.lower().count(keyword) * weight
    
    # Get dominant mood
    dominant_mood = max(mood_scores.items(), key=lambda x: x[1])[0]
    
    # Only use sentiment analysis if no strong keyword matches
    if mood_scores[dominant_mood] <= 2:
        analysis = TextBlob(full_text)
        polarity = analysis.sentiment.polarity
        subjectivity = analysis.sentiment.subjectivity
        
        if polarity > 0.3:
            if subjectivity > 0.6:
                return "happy"
            else:
                return "neutral"
        elif polarity < -0.3:
            if subjectivity > 0.6:
                return "sad" if random.random() > 0.3 else "angry"
            else:
                return "neutral"
        else:
            if subjectivity > 0.6:
                return "relaxed" if random.random() > 0.5 else "stressed"
            else:
                return "neutral"
    
    return dominant_mood

# Improved playlist suggestion
def suggest_playlist(mood: str) -> tuple[str, str]:
    """Suggests a Spotify playlist based on mood with multiple options"""
    if not sp:
        return "Spotify not available", ""
    
    options = MOOD_PLAYLISTS.get(mood, MOOD_PLAYLISTS["neutral"])
    playlist_uri = random.choice(options)
    
    try:
        playlist = sp.playlist(playlist_uri, market="US")
        playlist_name = playlist["name"]
        playlist_link = playlist["external_urls"]["spotify"]
        return playlist_name, playlist_link
    except Exception as e:
        return "Recommended Playlist", f"https://open.spotify.com/playlist/{playlist_uri.split(':')[-1]}"

# Fuzzy command matching
def fuzzy_command_match(prompt, commands):
    prompt_lower = prompt.lower()
    for cmd in commands:
        if cmd in prompt_lower:
            return True
        # Check for close matches of first word
        if get_close_matches(cmd.split()[0], prompt_lower.split(), n=1, cutoff=0.7):
            return True
    return False

# Command handler with improved natural language understanding
def handle_command(prompt):
    prompt_lower = prompt.lower()
    commands = {
        "brightness": [
            "brightness",
            "screen light",
            "display brightness",
            "make brighter",
            "make darker"
        ],
        "volume": [
            "volume",
            "sound level",
            "turn up sound",
            "turn down sound",
            "mute"
        ],
        "music": [
            "play music",
            "suggest song",
            "recommend music",
            "i need music",
            "what should i listen to"
        ]
    }
    
    # Brightness commands
    if fuzzy_command_match(prompt_lower, commands["brightness"]):
        if "increase" in prompt_lower or "up" in prompt_lower or "brighter" in prompt_lower:
            current = get_current_brightness()
            new_val = min(current + 20, 100)
            return set_brightness(new_val)
        elif "decrease" in prompt_lower or "down" in prompt_lower or "darker" in prompt_lower:
            current = get_current_brightness()
            new_val = max(current - 20, 0)
            return set_brightness(new_val)
        elif "set" in prompt_lower:
            try:
                parts = prompt_lower.split()

                percentage = next((int(s.replace('%', '')) for s in parts if s.replace('%', '').isdigit()))
                return set_brightness(percentage)
            except:
                return "Please specify a percentage (e.g., 'set brightness to 75%')"
        else:
            return f"Current brightness is {get_current_brightness()}%"
    
    # Volume commands
    elif fuzzy_command_match(prompt_lower, commands["volume"]):
        if "increase" in prompt_lower or "up" in prompt_lower or "louder" in prompt_lower:
            current = get_current_volume()
            new_val = min(current + 20, 100)
            return set_volume(new_val)
        elif "decrease" in prompt_lower or "down" in prompt_lower or "quieter" in prompt_lower:
            current = get_current_volume()
            new_val = max(current - 20, 0)
            return set_volume(new_val)
        elif "mute" in prompt_lower:
            return set_volume(0)
        elif "set" in prompt_lower:
            try:
                parts = prompt_lower.split()
                percentage = next((int(s.replace('%', '')) for s in parts if s.replace('%', '').isdigit()))
                return set_volume(percentage)
            except:
                return "Please specify a percentage (e.g., 'set volume to 50%')"
        else:
            return f"Current volume is {get_current_volume()}%"
    
    # Music commands
    elif fuzzy_command_match(prompt_lower, commands["music"]):
        mood = detect_mood_from_history(st.session_state.chat_session.history)
        playlist_name, playlist_link = suggest_playlist(mood)
        return f"Based on your recent mood ({mood}), I recommend: {playlist_name} - {playlist_link}"
    
    return None

# Translate roles for Streamlit
def translate_role_for_streamlit(user_role):
    return "assistant" if user_role == "model" else user_role

# Initialize chat session
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Initialize mood history
if "mood_history" not in st.session_state:
    st.session_state.mood_history = []

# Display title
st.title("🎵 Mood-Based Music Assistant")

# Display chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Input field for user's message
user_prompt = st.chat_input("Chat with me... (Try 'I'm feeling down', 'Play some music', or 'Increase brightness')")
if user_prompt:
    # Add user's message to chat
    st.chat_message("user").markdown(user_prompt)

    # Update mood history
    current_mood = detect_mood_from_history(st.session_state.chat_session.history)
    st.session_state.mood_history.append({
        "time": datetime.now(),
        "mood": current_mood,
        "message": user_prompt
    })

    # Check for commands
    command_response = handle_command(user_prompt)
    if command_response:
        with st.chat_message("assistant"):
            st.markdown(command_response)
    else:
        # Get Gemini response
        gemini_response = st.session_state.chat_session.send_message(user_prompt)
        
        # Decide if we should suggest music (30% chance or if mood is strong)
        mood_strength = sum(1 for entry in st.session_state.mood_history if entry["mood"] == current_mood)
        should_suggest_music = (
            "music" in user_prompt.lower() or 
            random.random() < 0.3 or 
            mood_strength > 2
        )
        
        if should_suggest_music and current_mood in MOOD_PLAYLISTS:
            playlist_name, playlist_link = suggest_playlist(current_mood)
            music_suggestion = (
                f"\n\nBased on your mood, you might enjoy: [{playlist_name}]({playlist_link})"
            )
        else:
            music_suggestion = ""
            
        with st.chat_message("assistant"):
            st.markdown(f"{gemini_response.text}{music_suggestion}")

# Sidebar with mood insights
with st.sidebar:
    st.subheader("Your Mood Insights")
    if st.session_state.mood_history:
        latest_mood = st.session_state.mood_history[-1]["mood"]
        st.metric("Current Mood", latest_mood.capitalize())
        
        # Mood history chart
        mood_counts = {}
        for entry in st.session_state.mood_history:
            mood_counts[entry["mood"]] = mood_counts.get(entry["mood"], 0) + 1
        
        if mood_counts:
            st.write("**Mood Distribution**")
            for mood, count in mood_counts.items():
                st.progress(count / len(st.session_state.mood_history), text=f"{mood.capitalize()}: {count}")
    
    st.write("---")
    st.write("**Try saying:**")
    st.write("- I'm feeling stressed today")
    st.write("- Play something happy")
    st.write("- Adjust the brightness")
    st.write("- I need relaxing music")