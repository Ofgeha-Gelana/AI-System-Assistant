import os
import streamlit as st
import subprocess
import requests
import json
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

# --- System Controls ---
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
    """Sets the system volume level (Linux)."""
    os.system(f"pactl set-sink-volume @DEFAULT_SINK@ {level}%")
    return f"Volume set to {level}%"

def toggle_wifi(status: str) -> str:
    """Turns Wi-Fi on or off."""
    if status.lower() not in ["on", "off"]:
        return "Invalid option. Use 'on' or 'off'."
    os.system(f"nmcli radio wifi {status}")
    return f"Wi-Fi turned {status}."

def toggle_dark_mode(status: str) -> str:
    """Toggles dark mode (GNOME-based Linux)."""
    if status.lower() not in ["on", "off"]:
        return "Invalid option. Use 'on' or 'off'."
    os.system(f"gsettings set org.gnome.desktop.interface gtk-theme {'Adwaita-dark' if status == 'on' else 'Adwaita'}")
    return f"Dark mode turned {status}."

def lock_screen() -> str:
    """Locks the screen."""
    os.system("gnome-screensaver-command -l")
    return "Screen locked."

def shutdown_system() -> str:
    """Shuts down the system."""
    os.system("shutdown -h now")
    return "Shutting down the system."

def restart_system() -> str:
    """Restarts the system."""
    os.system("reboot")
    return "Restarting the system."

# --- Open Applications ---
def open_application(app_name: str) -> str:
    """Opens common applications by name."""
    apps = {
        "vscode": "code",
        "chrome": "google-chrome",
        "firefox": "firefox",
        "terminal": "gnome-terminal",
        "files": "nautilus",
        "spotify": "spotify",
        "telegram": "telegram-desktop",  # Command to launch Telegram
        "intellij": "idea"  # Command to launch IntelliJ IDEA
    }
   
    command = apps.get(app_name.lower())
    
    if not command:
        return f"Application '{app_name}' not supported."
    
    try:
        subprocess.Popen(command, shell=True)
        return f"Opening {app_name}..."
    except Exception as e:
        return f"Error opening {app_name}: {str(e)}"

# --- Mood Detection ---
def detect_mood(text: str) -> str:
    """Analyzes text sentiment and returns mood."""
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
    "happy": "37i9dQZF1DXdPec7aLTmlC",
    "sad": "37i9dQZF1DX64Y3ftTBfaN",
    "stressed": "37i9dQZF1DWU0ScTcjJBdj",
    "neutral": "37i9dQZF1DX0XUsuxWHRQd",
    "angry": "37i9dQZF1DX2DCrI7t4mmy"
}

def recommend_music(mood: str) -> str:
    """Recommends a Spotify playlist based on mood."""
    if not sp:
        return "Spotify integration not available."

    playlist_id = MOOD_PLAYLISTS.get(mood, MOOD_PLAYLISTS["neutral"])
    
    try:
        playlist = sp.playlist(playlist_id, market="US")
        return f"🎵 Based on your mood, listen to: [{playlist['name']}]({playlist['external_urls']['spotify']})"
    except:
        return f"🎵 Listen here: [Spotify Playlist](https://open.spotify.com/playlist/{playlist_id})"

# --- Integrating Gemini AI ---
client = genai.Client(api_key=GEMINI_API_KEY)

config = GenerateContentConfig(
    system_instruction="You are a helpful assistant that controls device settings, launches applications, and recommends music based on mood.",
    tools=[set_brightness, set_volume, toggle_wifi, toggle_dark_mode, lock_screen, shutdown_system, restart_system, open_application, detect_mood, recommend_music]
)

# --- Send SMS Gateway Request ---
def send_sms(phone: str, message: str) -> str:
    """Send an SMS gateway request to the specified API."""
    
    url = "http://10.1.230.6:7081/v1/cbo/"
    
    payload = {
        "SMSGateway_Request": {
            "ESBHeader": {
                "serviceCode": "330000",
                "channel": "USSD",
                "Service_name": "SMSGateway",
                "Message_Id": "6255726663"
            },
            "SMSGateway": {
                "Mobile": phone,
                "Text": message
            }
        }
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        # Send POST request with the payload
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        
        # Check if the request was successful
        if response.status_code == 200:
            return f"SMS sent successfully to {phone}."
        else:
            return f"Error: Unable to send SMS. Status code: {response.status_code}, {response.text}"
    
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"

# --- Streamlit Chat UI ---
st.title("💡 AI System Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
user_input = st.chat_input("Ask me to adjust settings, open apps, or recommend music!")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Check if user wants to open an app
    if 'open' in user_input.lower():
        app_name = user_input.split("open")[-1].strip()
        ai_response = open_application(app_name)
    elif 'music' in user_input.lower():
        detected_mood = detect_mood(" ".join([msg["content"] for msg in st.session_state.messages if msg["role"] == "user"]))
        ai_response = recommend_music(detected_mood)
    elif 'send sms' in user_input.lower():
        parts = user_input.split("send sms")[-1].strip().split(",")
        if len(parts) == 2:
            phone = parts[0].strip()
            message = parts[1].strip()
            ai_response = send_sms(phone, message)
        else:
            ai_response = "Please provide both the phone number and the message text in the format: 'send sms <phone>, <message>'."
    else:
        r = client.models.generate_content(model="gemini-2.0-flash", config=config, contents=user_input)
        ai_response = r.text

    st.session_state.messages.append({"role": "assistant", "content": ai_response})
    with st.chat_message("assistant"):
        st.markdown(ai_response)
