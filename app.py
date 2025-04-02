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

# Initialize Spotify Client
def initialize_spotify():
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

# System Controls
def execute_command(command: str) -> str:
    """Executes a shell command and returns a success message."""
    try:
        subprocess.run(command, shell=True, capture_output=True, text=True)
        return f"Executed: {command}"
    except Exception as e:
        return f"Error: {str(e)}"

# def set_brightness(level: int) -> str:
#     return execute_command(f"xrandr --output eDP-1 --brightness {level / 100}")

def set_brightness(level: int) -> str:
    """Sets the system brightness level (Linux)."""
    try:
        if not 0 <= level <= 100:
            return "Brightness must be between 0 and 100."
        
        backlight_paths = ["/sys/class/backlight/intel_backlight/", "/sys/class/backlight/amdgpu_bl0/"]
        backlight_path = next((p for p in backlight_paths if os.path.exists(p)), None)

        if not backlight_path:
            return "Brightness control not found."

        with open(f"{backlight_path}max_brightness", "r") as f:
            max_brightness = int(f.read().strip())

        target_brightness = int((level / 100) * max_brightness)
        cmd = f"echo {target_brightness} | sudo tee {backlight_path}brightness"
        
        subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return f"Brightness set to {level}%"
    
    except Exception as e:
        return f"Error setting brightness: {str(e)}"


def set_volume(level: int) -> str:
    return execute_command(f"pactl set-sink-volume @DEFAULT_SINK@ {level}%")

def toggle_wifi(status: str) -> str:
    return execute_command(f"nmcli radio wifi {status}")

def toggle_dark_mode(status: str) -> str:
    theme = 'Adwaita-dark' if status == 'on' else 'Adwaita'
    return execute_command(f"gsettings set org.gnome.desktop.interface gtk-theme {theme}")

def lock_screen() -> str:
    return execute_command("gnome-screensaver-command -l")

def shutdown_system() -> str:
    return execute_command("shutdown -h now")

def restart_system() -> str:
    return execute_command("reboot")

def open_application(app_name: str) -> str:
    apps = {
        "vscode": "code",
        "chrome": "google-chrome",
        "firefox": "firefox",
        "terminal": "gnome-terminal",
        "files": "nautilus",
        "spotify": "spotify",
        "telegram": "telegram-desktop",
        "intellij": "idea"
    }
    command = apps.get(app_name.lower())
    return execute_command(command) if command else f"Application '{app_name}' not supported."

# Mood Detection & Music Recommendation
MOOD_PLAYLISTS = {
    "happy": "37i9dQZF1DXdPec7aLTmlC",
    "sad": "37i9dQZF1DX64Y3ftTBfaN",
    "stressed": "37i9dQZF1DWU0ScTcjJBdj",
    "neutral": "37i9dQZF1DX0XUsuxWHRQd",
    "angry": "37i9dQZF1DX2DCrI7t4mmy"
}

def detect_mood(text: str) -> str:
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    if polarity > 0.3:
        return "happy"
    elif polarity < -0.3:
        return "sad"
    return "neutral"

def recommend_music(mood: str) -> str:
    if not sp:
        return "Spotify integration not available."
    playlist_id = MOOD_PLAYLISTS.get(mood, MOOD_PLAYLISTS["neutral"])
    return f"🎵 Listen here: [Spotify Playlist](https://open.spotify.com/playlist/{playlist_id})"

# AI Assistant with Gemini
client = genai.Client(api_key=GEMINI_API_KEY)
config = GenerateContentConfig(
    system_instruction="You are an AI assistant that controls device settings, opens applications, and recommends music.",
    tools=[set_brightness, set_volume, toggle_wifi, toggle_dark_mode, lock_screen, shutdown_system, restart_system, open_application, detect_mood, recommend_music]
)

# Streamlit UI
st.title("🤖 Smart System Assistant")
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Ask me to adjust settings, open apps, or recommend music!")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    ai_response = ""
    if 'open' in user_input.lower():
        app_name = user_input.split("open")[-1].strip()
        ai_response = open_application(app_name)
    elif 'music' in user_input.lower():
        detected_mood = detect_mood(" ".join([msg["content"] for msg in st.session_state.messages if msg["role"] == "user"]))
        ai_response = recommend_music(detected_mood)
    else:
        r = client.models.generate_content(model="gemini-2.0-flash", config=config, contents=user_input)
        ai_response = r.text
    
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
    with st.chat_message("assistant"):
        st.markdown(ai_response)




# import os
# import streamlit as st
# import subprocess
# from dotenv import load_dotenv
# import spotipy
# from spotipy.oauth2 import SpotifyOAuth
# from textblob import TextBlob
# from google.genai.types import GenerateContentConfig
# from google import genai

# # Load environment variables
# load_dotenv()

# # API Keys & Config
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
# SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
# SPOTIFY_REDIRECT_URI = "http://localhost:8080"

# # Initialize Spotify Client
# def initialize_spotify():
#     try:
#         return spotipy.Spotify(auth_manager=SpotifyOAuth(
#             client_id=SPOTIFY_CLIENT_ID,
#             client_secret=SPOTIFY_CLIENT_SECRET,
#             redirect_uri=SPOTIFY_REDIRECT_URI,
#             scope="playlist-read-private"
#         ))
#     except Exception as e:
#         st.error(f"Spotify authentication failed: {e}")
#         return None

# sp = initialize_spotify()

# # System Controls
# def execute_command(command: str) -> str:
#     """Executes a shell command and returns a success message."""
#     try:
#         subprocess.run(command, shell=True, capture_output=True, text=True)
#         return f"Executed: {command}"
#     except Exception as e:
#         return f"Error: {str(e)}"

# # Set brightness
# def set_brightness(level: int) -> str:
#     """Sets the system brightness level (Linux)."""
#     try:
#         if not 0 <= level <= 100:
#             return "Brightness must be between 0 and 100."
        
#         backlight_paths = ["/sys/class/backlight/intel_backlight/", "/sys/class/backlight/amdgpu_bl0/"]
#         backlight_path = next((p for p in backlight_paths if os.path.exists(p)), None)

#         if not backlight_path:
#             return "Brightness control not found."

#         with open(f"{backlight_path}max_brightness", "r") as f:
#             max_brightness = int(f.read().strip())

#         target_brightness = int((level / 100) * max_brightness)
#         cmd = f"echo {target_brightness} | sudo tee {backlight_path}brightness"
        
#         subprocess.run(cmd, shell=True, capture_output=True, text=True)
#         return f"Brightness set to {level}%"
    
#     except Exception as e:
#         return f"Error setting brightness: {str(e)}"

# # Set volume
# def set_volume(level: int) -> str:
#     return execute_command(f"pactl set-sink-volume @DEFAULT_SINK@ {level}%")

# # Toggle Wi-Fi
# def toggle_wifi(status: str) -> str:
#     return execute_command(f"nmcli radio wifi {status}")

# # Toggle Dark Mode
# def toggle_dark_mode(status: str) -> str:
#     theme = 'Adwaita-dark' if status == 'on' else 'Adwaita'
#     return execute_command(f"gsettings set org.gnome.desktop.interface gtk-theme {theme}")

# # Lock screen
# def lock_screen() -> str:
#     return execute_command("gnome-screensaver-command -l")

# # Shutdown system
# def shutdown_system() -> str:
#     return execute_command("shutdown -h now")

# # Restart system
# def restart_system() -> str:
#     return execute_command("reboot")

# # Open applications
# def open_application(app_name: str) -> str:
#     apps = {
#         "vscode": "code",
#         "chrome": "google-chrome",
#         "firefox": "firefox",
#         "terminal": "gnome-terminal",
#         "files": "nautilus",
#         "spotify": "spotify",
#         "telegram": "telegram-desktop",
#         "intellij": "idea"
#     }
#     command = apps.get(app_name.lower())
#     return execute_command(command) if command else f"Application '{app_name}' not supported."

# # Mood Detection & Music Recommendation
# MOOD_PLAYLISTS = {
#     "happy": "37i9dQZF1DXdPec7aLTmlC",
#     "sad": "37i9dQZF1DX64Y3ftTBfaN",
#     "stressed": "37i9dQZF1DWU0ScTcjJBdj",
#     "neutral": "37i9dQZF1DX0XUsuxWHRQd",
#     "angry": "37i9dQZF1DX2DCrI7t4mmy"
# }

# def detect_mood(text: str) -> str:
#     analysis = TextBlob(text)
#     polarity = analysis.sentiment.polarity
#     if polarity > 0.3:
#         return "happy"
#     elif polarity < -0.3:
#         return "sad"
#     return "neutral"

# def recommend_music(mood: str) -> str:
#     if not sp:
#         return "Spotify integration not available."
#     playlist_id = MOOD_PLAYLISTS.get(mood, MOOD_PLAYLISTS["neutral"])
#     return f"🎵 Listen here: [Spotify Playlist](https://open.spotify.com/playlist/{playlist_id})"

# # AI Assistant with Gemini
# client = genai.Client(api_key=GEMINI_API_KEY)
# config = GenerateContentConfig(
#     system_instruction="You are an AI assistant that controls device settings, opens applications, and recommends music.",
#     tools=[set_brightness, set_volume, toggle_wifi, toggle_dark_mode, lock_screen, shutdown_system, restart_system, open_application, detect_mood, recommend_music]
# )

# # Streamlit UI
# st.set_page_config(page_title="Smart System Assistant", page_icon="🤖", layout="wide")

# # Title and Description
# st.title("🤖 Smart System Assistant")
# st.markdown("""
#     Welcome to the **Smart System Assistant**! You can control your system settings, open apps, and get music recommendations based on your mood.
#     Ask me anything and I'll assist you!
# """, unsafe_allow_html=True)

# # Sidebar for easy navigation and settings
# st.sidebar.title("Navigation")
# st.sidebar.markdown("""
#     - Adjust System Settings
#     - Get Music Recommendations
#     - Open Applications
#     - Control Brightness, Volume, and Wi-Fi
# """)

# # Messages Section
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # Display messages with better UI
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         if message["role"] == "user":
#             st.markdown(f"<div style='background-color:#f1f1f1;padding:10px;border-radius:5px;'><strong>{message['role'].capitalize()}:</strong> {message['content']}</div>", unsafe_allow_html=True)
#         else:
#             st.markdown(f"<div style='background-color:#e0f7fa;padding:10px;border-radius:5px;'><strong>{message['role'].capitalize()}:</strong> {message['content']}</div>", unsafe_allow_html=True)

# # User Input Section with enhanced design
# user_input = st.text_input("Your Request", "", placeholder="Type your command here...", label_visibility="collapsed")
# if user_input:
#     st.session_state.messages.append({"role": "user", "content": user_input})
    
#     # Show the user message
#     with st.chat_message("user"):
#         st.markdown(f"<div style='background-color:#f1f1f1;padding:10px;border-radius:5px;'>{user_input}</div>", unsafe_allow_html=True)

#     ai_response = ""
#     if 'open' in user_input.lower():
#         app_name = user_input.split("open")[-1].strip()
#         ai_response = open_application(app_name)
#     elif 'music' in user_input.lower():
#         detected_mood = detect_mood(" ".join([msg["content"] for msg in st.session_state.messages if msg["role"] == "user"]))
#         ai_response = recommend_music(detected_mood)
#     else:
#         r = client.models.generate_content(model="gemini-2.0-flash", config=config, contents=user_input)
#         ai_response = r.text
    
#     st.session_state.messages.append({"role": "assistant", "content": ai_response})
#     with st.chat_message("assistant"):
#         st.markdown(f"<div style='background-color:#e0f7fa;padding:10px;border-radius:5px;'>{ai_response}</div>", unsafe_allow_html=True)
