# import os
# import streamlit as st
# import subprocess
# from dotenv import load_dotenv
# import google.generativeai as gen_ai

# # Load environment variables
# load_dotenv()

# # Configure Streamlit page settings
# st.set_page_config(
#     page_title="Chat with Gemini-Pro!",
#     page_icon=":brain:",
#     layout="centered",
# )

# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# # Set up Google Gemini-Pro AI model
# gen_ai.configure(api_key=GOOGLE_API_KEY)
# model = gen_ai.GenerativeModel('gemini-1.5-flash')

# # Brightness control function with sudo prompt
# def set_brightness(percentage):
#     """
#     Adjust screen brightness on Ubuntu by percentage (0-100) using sudo
#     """
#     try:
#         if not 0 <= percentage <= 100:
#             raise ValueError("Brightness must be between 0 and 100")

#         backlight_path = "/sys/class/backlight/intel_backlight/"
#         if not os.path.exists(backlight_path):
#             backlight_path = "/sys/class/backlight/amdgpu_bl0/"
        
#         if not os.path.exists(backlight_path):
#             return "Could not find backlight control path"

#         with open(f"{backlight_path}max_brightness", "r") as f:
#             max_brightness = int(f.read().strip())

#         target_brightness = int((percentage / 100) * max_brightness)
        
#         cmd = f"echo {target_brightness} | sudo tee {backlight_path}brightness"
#         result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
#         if result.returncode == 0:
#             return f"Brightness set to {percentage}%"
#         else:
#             return f"Failed: {result.stderr or 'Unknown error'}"

#     except Exception as e:
#         return f"Error: {str(e)}"

# # Get current brightness
# def get_current_brightness():
#     try:
#         backlight_path = "/sys/class/backlight/intel_backlight/"
#         if not os.path.exists(backlight_path):
#             backlight_path = "/sys/class/backlight/amdgpu_bl0/"
        
#         if not os.path.exists(backlight_path):
#             return 50

#         with open(f"{backlight_path}max_brightness", "r") as f:
#             max_brightness = int(f.read().strip())
#         with open(f"{backlight_path}brightness", "r") as f:
#             current = int(f.read().strip())
        
#         return int((current / max_brightness) * 100)
#     except:
#         return 50

# # Volume control function with sudo prompt
# def set_volume(percentage):
#     """
#     Adjust system volume on Ubuntu by percentage (0-100) using amixer
#     """
#     try:
#         if not 0 <= percentage <= 100:
#             raise ValueError("Volume must be between 0 and 100")

#         cmd = f"amixer -q sset Master {percentage}%"
#         result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
#         if result.returncode == 0:
#             return f"Volume set to {percentage}%"
#         else:
#             cmd = f"echo '{percentage}' | sudo tee /proc/self/fd/0 | amixer -q sset Master $(cat -)%"
#             result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
#             if result.returncode == 0:
#                 return f"Volume set to {percentage}%"
#             else:
#                 return f"Failed: {result.stderr or 'Unknown error'}"

#     except Exception as e:
#         return f"Error: {str(e)}"

# # Get current volume
# def get_current_volume():
#     try:
#         cmd = "amixer sget Master"
#         result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
#         if result.returncode == 0:
#             for line in result.stdout.splitlines():
#                 if "Playback" in line and "%" in line:
#                     percentage = int(line.split("[")[1].split("%")[0])
#                     return percentage
#         return 50
#     except:
#         return 50

# # Command handler for brightness and volume
# def handle_command(prompt):
#     prompt_lower = prompt.lower()
    
#     # Brightness commands
#     if "increase brightness" in prompt_lower:
#         current_brightness = get_current_brightness()
#         new_brightness = min(current_brightness + 10, 100)
#         return set_brightness(new_brightness)
    
#     elif "decrease brightness" in prompt_lower:
#         current_brightness = get_current_brightness()
#         new_brightness = max(current_brightness - 10, 0)
#         return set_brightness(new_brightness)
    
#     elif "give me my brightness" in prompt_lower:
#         current_brightness = get_current_brightness()
#         return f"Your current brightness is {current_brightness}%"
    
#     elif "set brightness to" in prompt_lower:
#         try:
#             percentage = int(prompt_lower.split("set brightness to")[1].strip().replace("%", ""))
#             return set_brightness(percentage)
#         except (ValueError, IndexError):
#             return "Please specify a valid percentage (e.g., 'set brightness to 75')"
    
#     # Volume commands
#     elif "increase volume" in prompt_lower:
#         current_volume = get_current_volume()
#         new_volume = min(current_volume + 10, 100)
#         return set_volume(new_volume)
    
#     elif "decrease volume" in prompt_lower:
#         current_volume = get_current_volume()
#         new_volume = max(current_volume - 10, 0)
#         return set_volume(new_volume)
    
#     elif "give me my volume" in prompt_lower:
#         current_volume = get_current_volume()
#         return f"Your current volume is {current_volume}%"
    
#     elif "set volume to" in prompt_lower:
#         try:
#             percentage = int(prompt_lower.split("set volume to")[1].strip().replace("%", ""))
#             return set_volume(percentage)
#         except (ValueError, IndexError):
#             return "Please specify a valid percentage (e.g., 'set volume to 50')"
    
#     return None

# # Translate roles for Streamlit
# def translate_role_for_streamlit(user_role):
#     return "assistant" if user_role == "model" else user_role

# # Initialize chat session
# if "chat_session" not in st.session_state:
#     st.session_state.chat_session = model.start_chat(history=[])

# # Display title
# st.title("🤖 Gemini Pro - ChatBot")

# # Display chat history
# for message in st.session_state.chat_session.history:
#     with st.chat_message(translate_role_for_streamlit(message.role)):
#         st.markdown(message.parts[0].text)

# # Input field for user's message
# user_prompt = st.chat_input("Ask Gemini-Pro... (Try 'give me my brightness', 'set brightness to 75', 'increase volume', etc.)")
# if user_prompt:
#     # Add user's message to chat
#     st.chat_message("user").markdown(user_prompt)

#     # Check for commands
#     command_response = handle_command(user_prompt)
#     if command_response:
#         with st.chat_message("assistant"):
#             st.markdown(f"{command_response} ")
#     else:
#         # Fallback to Gemini-Pro response
#         gemini_response = st.session_state.chat_session.send_message(user_prompt)
#         with st.chat_message("assistant"):
#             st.markdown(gemini_response.text)

# # Sidebar note
# st.sidebar.markdown("**Note:** Brightness and volume commands may prompt for your password in the terminal.")






import os
import streamlit as st
import subprocess
from dotenv import load_dotenv
import google.generativeai as gen_ai
from textblob import TextBlob
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime

# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Chat with Gemini-Pro!",
    page_icon=":brain:",
    layout="centered",
)




GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = "http://localhost:8080"

# Mood-based Spotify Playlist IDs
MOOD_PLAYLISTS = {
    "happy": "spotify:playlist:37i9dQZF1DXdPec7aLTmlC",    # Happy Hits!
    "sad": "spotify:playlist:37i9dQZF1DX64Y3ftTBfaN",      # Sad Bops
    "stressed": "spotify:playlist:37i9dQZF1DWU0ScTcjJBdj",  # Stress Relief
    "neutral": "spotify:playlist:37i9dQZF1DX0XUsuxWHRQd",   # Chill Hits
    "angry": "spotify:playlist:37i9dQZF1DX2DCrI7t4mmy"      # Angry Punk
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

# Brightness control function with sudo prompt
def set_brightness(percentage):
    """
    Adjust screen brightness on Ubuntu by percentage (0-100) using sudo
    """
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

# Get current brightness
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

# Volume control function with sudo prompt
def set_volume(percentage):
    """
    Adjust system volume on Ubuntu by percentage (0-100) using amixer
    """
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

# Get current volume
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

# Function to detect mood based on text sentiment and keywords
def detect_mood(text: str) -> str:
    """Analyzes sentiment and keywords to determine mood."""
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    text_lower = text.lower()

    # Keyword-based overrides
    if "angry" in text_lower or "mad" in text_lower or "hit" in text_lower:
        return "angry"
    elif "happy" in text_lower or "great" in text_lower or "joy" in text_lower:
        return "happy"
    elif "sad" in text_lower or "down" in text_lower or "depressed" in text_lower:
        return "sad"
    elif "stressed" in text_lower or "anxious" in text_lower or "overwhelmed" in text_lower:
        return "stressed"
    elif "music" in text_lower or "playlist" in text_lower or "song" in text_lower:
        return "music"
    
    # Fallback to polarity
    if polarity > 0.3:
        return "happy"
    elif polarity < -0.3:
        return "sad"
    elif -0.3 <= polarity <= 0.3:
        return "neutral"
    else:
        return "stressed"

# Function to suggest a playlist based on mood
def suggest_playlist(mood: str) -> tuple[str, str]:
    """Suggests a Spotify playlist based on the mood and returns its name and link."""
    if not sp:
        return "Spotify not available", ""
    
    playlist_uri = MOOD_PLAYLISTS.get(mood, MOOD_PLAYLISTS["neutral"])
    try:
        playlist = sp.playlist(playlist_uri, market="US")
        playlist_name = playlist["name"]
        playlist_link = playlist["external_urls"]["spotify"]
        return playlist_name, playlist_link
    except Exception as e:
        return "Fallback Playlist", f"https://open.spotify.com/playlist/{playlist_uri.split(':')[-1]}"

# Command handler for brightness, volume, and music
def handle_command(prompt):
    prompt_lower = prompt.lower()
    
    # Brightness commands
    if "increase brightness" in prompt_lower:
        current_brightness = get_current_brightness()
        new_brightness = min(current_brightness + 10, 100)
        return set_brightness(new_brightness)
    
    elif "decrease brightness" in prompt_lower:
        current_brightness = get_current_brightness()
        new_brightness = max(current_brightness - 10, 0)
        return set_brightness(new_brightness)
    
    elif "give me my brightness" in prompt_lower:
        current_brightness = get_current_brightness()
        return f"Your current brightness is {current_brightness}%"
    
    elif "set brightness to" in prompt_lower:
        try:
            percentage = int(prompt_lower.split("set brightness to")[1].strip().replace("%", ""))
            return set_brightness(percentage)
        except (ValueError, IndexError):
            return "Please specify a valid percentage (e.g., 'set brightness to 75')"
    
    # Volume commands
    elif "increase volume" in prompt_lower:
        current_volume = get_current_volume()
        new_volume = min(current_volume + 10, 100)
        return set_volume(new_volume)
    
    elif "decrease volume" in prompt_lower:
        current_volume = get_current_volume()
        new_volume = max(current_volume - 10, 0)
        return set_volume(new_volume)
    
    elif "give me my volume" in prompt_lower:
        current_volume = get_current_volume()
        return f"Your current volume is {current_volume}%"
    
    elif "set volume to" in prompt_lower:
        try:
            percentage = int(prompt_lower.split("set volume to")[1].strip().replace("%", ""))
            return set_volume(percentage)
        except (ValueError, IndexError):
            return "Please specify a valid percentage (e.g., 'set volume to 50')"
    
    # Music commands
    elif any(keyword in prompt_lower for keyword in ["play music", "suggest song", "recommend music", "i need music"]):
        mood = detect_mood(prompt)
        playlist_name, playlist_link = suggest_playlist(mood)
        return f"Based on your mood ({mood}), I recommend this playlist: {playlist_name}. You can listen here: {playlist_link}"
    
    return None

# Translate roles for Streamlit
def translate_role_for_streamlit(user_role):
    return "assistant" if user_role == "model" else user_role

# Initialize chat session
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Display title
st.title("🤖 Gemini Pro - ChatBot")

# Display chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Input field for user's message
user_prompt = st.chat_input("Ask Gemini-Pro... (Try 'give me my brightness', 'set brightness to 75', 'I need music', etc.)")
if user_prompt:
    # Add user's message to chat
    st.chat_message("user").markdown(user_prompt)

    # Check for commands
    command_response = handle_command(user_prompt)
    if command_response:
        with st.chat_message("assistant"):
            st.markdown(f"{command_response} ")
    else:
        # Fallback to Gemini-Pro response
        gemini_response = st.session_state.chat_session.send_message(user_prompt)
        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)

# Sidebar note
st.sidebar.markdown("**Note:**")
st.sidebar.markdown("- Brightness/volume commands may prompt for your password in the terminal.")
st.sidebar.markdown("- Music recommendations require Spotify credentials in .env file.")