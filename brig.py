import os
import streamlit as st
import subprocess
from dotenv import load_dotenv
import google.generativeai as gen_ai
from google.generativeai.types import GenerateContentConfig
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Chat with Gemini-Pro!",
    page_icon=":brain:",
    layout="centered",
)

# Configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = "http://localhost:8080"

# Mood-based Spotify Playlist IDs
MOOD_PLAYLISTS = {
    "happy": "spotify:playlist:37i9dQZF1DXdPec7aLTmlC",
    "sad": "spotify:playlist:37i9dQZF1DX7qK8ma5wgG1",
    "energetic": "spotify:playlist:37i9dQZF1DX0UrRvztWcAU",
    "relaxed": "spotify:playlist:37i9dQZF1DX4WYpdgoIcn6",
    "focus": "spotify:playlist:37i9dQZF1DX9uKNf5jGX6m",
    "default": "spotify:playlist:37i9dQZF1DX0XUsuxWHRQd"
}

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

# 1. Define all functions exactly like in your example
def set_brightness(percentage: int) -> str:
    """Sets the screen brightness to the specified percentage (0-100)"""
    try:
        if not 0 <= percentage <= 100:
            return "Brightness must be between 0 and 100"

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
        return f"Failed to set brightness: {result.stderr}"
    except Exception as e:
        return f"Error setting brightness: {str(e)}"

def get_brightness() -> int:
    """Returns the current screen brightness percentage"""
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

def set_volume(percentage: int) -> str:
    """Sets the system volume to the specified percentage (0-100)"""
    try:
        if not 0 <= percentage <= 100:
            return "Volume must be between 0 and 100"

        cmd = f"amixer -q sset Master {percentage}%"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            return f"Volume set to {percentage}%"
        
        # Fallback with sudo if needed
        cmd = f"echo '{percentage}' | sudo tee /proc/self/fd/0 | amixer -q sset Master $(cat -)%"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return f"Volume set to {percentage}%"
        return f"Failed to set volume: {result.stderr}"
    except Exception as e:
        return f"Error setting volume: {str(e)}"

def get_volume() -> int:
    """Returns the current system volume percentage"""
    try:
        cmd = "amixer sget Master"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            for line in result.stdout.splitlines():
                if "Playback" in line and "%" in line:
                    return int(line.split("[")[1].split("%")[0])
        return 50
    except:
        return 50

def recommend_music(mood: str = None) -> str:
    """Recommends a Spotify playlist based on mood (happy/sad/energetic/relaxed/focus)"""
    if not sp:
        return "Spotify service is currently unavailable"
    
    playlist_uri = MOOD_PLAYLISTS.get(mood, MOOD_PLAYLISTS["default"])
    
    try:
        playlist = sp.playlist(playlist_uri, market="US")
        return (f"Recommended playlist: {playlist['name']}\n"
                f"Link: {playlist['external_urls']['spotify']}")
    except Exception as e:
        return f"Couldn't access playlist. Try searching for '{mood} music' on Spotify"

# 2. Create client and configure model exactly like your example
client = gen_ai.GenerativeModel('gemini-1.5-flash')

config = GenerateContentConfig(
    system_instruction="You are a helpful assistant that controls system settings and recommends music.",
    tools=[set_brightness, get_brightness, set_volume, get_volume, recommend_music]
)

# 3. Streamlit UI setup
st.title("🤖 System Control Assistant")

if "chat_session" not in st.session_state:
    st.session_state.chat_session = client.start_chat(history=[])

# Display chat history
for message in st.session_state.chat_session.history:
    with st.chat_message("assistant" if message.role == "model" else "user"):
        st.markdown(message.parts[0].text)

# Handle user input
user_prompt = st.chat_input("What would you like to do?")
if user_prompt:
    # Add user message to chat
    st.chat_message("user").markdown(user_prompt)
    
    # Send to Gemini (exactly like your example)
    response = st.session_state.chat_session.send_message(
        user_prompt,
        generation_config=config
    )
    
    # Process response
    for part in response.parts:
        if hasattr(part, 'function_call'):
            # Call the appropriate function
            func = globals().get(part.function_call.name)
            if func:
                result = func(**part.function_call.args)
                
                # Send result back to Gemini (like your example)
                st.session_state.chat_session.send_message(
                    gen_ai.protos.Content(
                        parts=[gen_ai.protos.Part(
                            function_response=gen_ai.protos.FunctionResponse(
                                name=part.function_call.name,
                                response={"result": result}
                            )
                        )]
                    )
                )
                
                # Get final response
                final_response = st.session_state.chat_session.send_message(
                    "Summarize the results for the user"
                )
                with st.chat_message("assistant"):
                    st.markdown(final_response.text)
        else:
            with st.chat_message("assistant"):
                st.markdown(part.text)

# Sidebar notes
st.sidebar.markdown("**Available Commands:**")
st.sidebar.markdown("- Set brightness/volume (0-100)")
st.sidebar.markdown("- Get current brightness/volume")
st.sidebar.markdown("- Recommend music (happy/sad/energetic/relaxed/focus)")