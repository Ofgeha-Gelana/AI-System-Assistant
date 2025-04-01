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

# # --- Initialize Spotify Client ---
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

# # --- Mood Detection ---
# def detect_mood(text: str) -> str:
#     analysis = TextBlob(text)
#     polarity = analysis.sentiment.polarity
#     text_lower = text.lower()

#     if "angry" in text_lower or "mad" in text_lower:
#         return "angry"
#     elif "happy" in text_lower or "joy" in text_lower or "excited" in text_lower:
#         return "happy"
#     elif "sad" in text_lower or "depressed" in text_lower:
#         return "sad"
#     elif "stressed" in text_lower or "anxious" in text_lower:
#         return "stressed"
    
#     return "happy" if polarity > 0.3 else "sad" if polarity < -0.3 else "neutral"

# # --- Spotify Music Recommendation ---
# MOOD_PLAYLISTS = {
#     "happy": "https://open.spotify.com/playlist/37i9dQZF1DXdPec7aLTmlC",
#     "sad": "https://open.spotify.com/playlist/37i9dQZF1DX64Y3ftTBfaN",
#     "stressed": "https://open.spotify.com/playlist/37i9dQZF1DWU0ScTcjJBdj",
#     "neutral": "https://open.spotify.com/playlist/37i9dQZF1DX0XUsuxWHRQd",
#     "angry": "https://open.spotify.com/playlist/37i9dQZF1DX2DCrI7t4mmy"
# }

# def recommend_music(mood: str) -> str:
#     return MOOD_PLAYLISTS.get(mood, MOOD_PLAYLISTS["neutral"])

# # --- Integrating Gemini AI ---
# client = genai.Client(api_key=GEMINI_API_KEY)
# model_id = "gemini-2.0-flash"
# config = GenerateContentConfig(
#     system_instruction="You are a helpful assistant that detects mood and recommends music.",
#     tools=[detect_mood, recommend_music],
# )

# # --- Streamlit Chat UI ---
# st.title("🎵 Mood-Based Music Recommender")

# if "messages" not in st.session_state:
#     st.session_state.messages = []

# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# user_input = st.chat_input("How are you feeling today?")

# if user_input:
#     st.session_state.messages.append({"role": "user", "content": user_input})
#     with st.chat_message("user"):
#         st.markdown(user_input)

#     detected_mood = detect_mood(user_input)
#     playlist_link = recommend_music(detected_mood)
#     ai_response = f"I sense you're feeling **{detected_mood}**. Here's a playlist for you: [Listen on Spotify]({playlist_link}) 🎶"

#     st.session_state.messages.append({"role": "assistant", "content": ai_response})
#     with st.chat_message("assistant"):
#         st.markdown(ai_response)
















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

# # --- Initialize Spotify Client ---
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

# # --- Mood Detection ---
# def detect_mood(text: str) -> str:
#     """
#     Detects the mood based on the input text.

#     Args:
#         text (str): Input text from the user.

#     Returns:
#         str: Detected mood ('happy', 'sad', 'stressed', 'neutral', 'angry').
#     """
#     if not text:  # Check if text is None or empty
#         return "neutral"

#     analysis = TextBlob(text)
#     polarity = analysis.sentiment.polarity
#     text_lower = text.lower()

#     if "angry" in text_lower or "mad" in text_lower:
#         return "angry"
#     elif "happy" in text_lower or "joy" in text_lower or "excited" in text_lower:
#         return "happy"
#     elif "sad" in text_lower or "depressed" in text_lower:
#         return "sad"
#     elif "stressed" in text_lower or "anxious" in text_lower:
#         return "stressed"
    
#     return "happy" if polarity > 0.3 else "sad" if polarity < -0.3 else "neutral"

# # --- Spotify Music Recommendation ---
# MOOD_PLAYLISTS = {
#     "happy": "https://open.spotify.com/playlist/37i9dQZF1DXdPec7aLTmlC",
#     "sad": "https://open.spotify.com/playlist/37i9dQZF1DX64Y3ftTBfaN",
#     "stressed": "https://open.spotify.com/playlist/37i9dQZF1DWU0ScTcjJBdj",
#     "neutral": "https://open.spotify.com/playlist/37i9dQZF1DX0XUsuxWHRQd",
#     "angry": "https://open.spotify.com/playlist/37i9dQZF1DX2DCrI7t4mmy"
# }

# def recommend_music(mood: str) -> str:
#     """
#     Recommends a Spotify playlist based on the detected mood.

#     Args:
#         mood (str): Detected mood.

#     Returns:
#         str: URL to the recommended playlist.
#     """
#     return MOOD_PLAYLISTS.get(mood, MOOD_PLAYLISTS["neutral"])

# # --- Integrating Gemini AI ---
# client = genai.Client(api_key=GEMINI_API_KEY)
# model_id = "gemini-2.0-flash"

# # Generation Config
# config = GenerateContentConfig(
#     system_instruction="You are a helpful assistant that detects mood and recommends music when specifically asked.",
#     tools=[detect_mood, recommend_music],  # Define callable functions
# )

# # --- Streamlit Chat UI ---
# st.title("🎵 Mood-Based Music Recommender")

# if "messages" not in st.session_state:
#     st.session_state.messages = []
#     st.session_state.detected_mood = "neutral"  # Store the detected mood

# # Display chat messages
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# user_input = st.chat_input("How are you feeling today?")

# if user_input:
#     # Add user input to chat history
#     st.session_state.messages.append({"role": "user", "content": user_input})
#     with st.chat_message("user"):
#         st.markdown(user_input)

#     # Detect mood based on user input
#     detected_mood = detect_mood(user_input)
#     st.session_state.detected_mood = detected_mood  # Store the detected mood

#     # Respond to the user with mood detection
#     ai_response = f"I sense you're feeling **{detected_mood}**. How can I assist you today?"
    
#     st.session_state.messages.append({"role": "assistant", "content": ai_response})
#     with st.chat_message("assistant"):
#         st.markdown(ai_response)

# # User asks for music
# if user_input and "music" in user_input.lower():
#     # Provide the playlist link based on the stored detected mood
#     playlist_link = recommend_music(st.session_state.detected_mood)
#     music_response = f"I recommend this playlist for your mood: [Listen on Spotify]({playlist_link}) 🎶"
    
#     st.session_state.messages.append({"role": "assistant", "content": music_response})
#     with st.chat_message("assistant"):
#         st.markdown(music_response)




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

# # --- Initialize Spotify Client ---
# def initialize_spotify():
#     """Authenticates and returns a Spotify client instance."""
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

# # --- Brightness Control ---
# def set_brightness(level: int) -> str:
#     """
#     Sets the system brightness level.

#     Args:
#         level (int): Brightness percentage (0-100).
#     """
#     try:
#         if not 0 <= level <= 100:
#             raise ValueError("Brightness must be between 0 and 100.")

#         backlight_path = "/sys/class/backlight/intel_backlight/"
#         if not os.path.exists(backlight_path):
#             backlight_path = "/sys/class/backlight/amdgpu_bl0/"

#         if not os.path.exists(backlight_path):
#             return "Could not find backlight control path."

#         with open(f"{backlight_path}max_brightness", "r") as f:
#             max_brightness = int(f.read().strip())

#         target_brightness = int((level / 100) * max_brightness)

#         cmd = f"echo {target_brightness} | sudo tee {backlight_path}brightness"
#         subprocess.run(cmd, shell=True, capture_output=True, text=True)

#         return f"Brightness set to {level}%"
#     except Exception as e:
#         return f"Error setting brightness: {str(e)}"

# # --- Volume Control ---
# def set_volume(level: int) -> str:
#     """
#     Sets the system volume.

#     Args:
#         level (int): Volume percentage (0-100).
#     """
#     os.system(f"pactl set-sink-volume @DEFAULT_SINK@ {level}%")
#     return f"Volume set to {level}%"

# # --- Mood Detection ---
# def detect_mood(text: str) -> str:
#     """
#     Analyzes text and determines mood.

#     Args:
#         text (str): Input text.

#     Returns:
#         str: Detected mood ('happy', 'sad', 'stressed', 'neutral', 'angry').
#     """
#     analysis = TextBlob(text)
#     polarity = analysis.sentiment.polarity
#     text_lower = text.lower()

#     if "angry" in text_lower or "mad" in text_lower:
#         return "angry"
#     elif "happy" in text_lower or "joy" in text_lower:
#         return "happy"
#     elif "sad" in text_lower or "depressed" in text_lower:
#         return "sad"
#     elif "stressed" in text_lower or "anxious" in text_lower:
#         return "stressed"

#     return "happy" if polarity > 0.3 else "sad" if polarity < -0.3 else "neutral"

# # --- Spotify Music Recommendation ---
# # MOOD_PLAYLISTS = {
# #     "happy": "spotify:playlist:37i9dQZF1DXdPec7aLTmlC",
# #     "sad": "spotify:playlist:37i9dQZF1DX64Y3ftTBfaN",
# #     "stressed": "spotify:playlist:37i9dQZF1DWU0ScTcjJBdj",
# #     "neutral": "spotify:playlist:37i9dQZF1DX0XUsuxWHRQd",
# #     "angry": "spotify:playlist:37i9dQZF1DX2DCrI7t4mmy"
# # }

# MOOD_PLAYLISTS = {
#     "happy": "37i9dQZF1DXdPec7aLTmlC",    # Just the ID portion
#     "sad": "37i9dQZF1DX64Y3ftTBfaN",
#     "stressed": "37i9dQZF1DWU0ScTcjJBdj",
#     "neutral": "37i9dQZF1DX0XUsuxWHRQd",
#     "angry": "37i9dQZF1DX2DCrI7t4mmy"
# }



# def recommend_music(mood: str) -> str:
#     """
#     Recommends a Spotify playlist based on the detected mood.

#     Args:
#         mood (str): Detected mood.

#     Returns:
#         str: URL to the recommended playlist.
#     """
#     if not sp:
#         return "Spotify integration not available."

#     playlist_id = MOOD_PLAYLISTS.get(mood, MOOD_PLAYLISTS["neutral"])
    
#     try:
#         playlist = sp.playlist(playlist_id, market="US")  # Added market parameter
#         return f"Based on your mood, listen to: [{playlist['name']}]({playlist['external_urls']['spotify']}) 🎶"
    
#     except spotipy.exceptions.SpotifyException as e:
#         # If the API request fails, return the direct playlist link instead
#         return f"Couldn't fetch playlist details, but you can still listen here: [Spotify Playlist](https://open.spotify.com/playlist/{playlist_id})"
    
#     except Exception as e:
#         return f"Unexpected error: {str(e)}"


# # --- Mood Detection Based on Chat History ---
# def detect_mood_from_history() -> str:
#     """
#     Analyzes the chat history and determines the user's overall mood.
    
#     Returns:
#         str: Detected mood ('happy', 'sad', 'stressed', 'neutral', 'angry').
#     """
#     # Combine all previous messages in the chat history
#     chat_history = " ".join([message["content"] for message in st.session_state.messages if message["role"] == "user"])

#     # Detect the mood based on the combined chat history
#     return detect_mood(chat_history)

# # --- Mood Detection and Music Recommendation Integration ---
# def recommend_music_based_on_history() -> str:
#     """
#     Detects the mood from chat history and recommends music based on that mood.
    
#     Returns:
#         str: A message with the recommended playlist link based on detected mood.
#     """
#     # Detect mood from chat history
#     detected_mood = detect_mood_from_history()
    
#     # Recommend music based on detected mood
#     return recommend_music(detected_mood)


# # --- Integrating Gemini AI ---
# # Create Gemini Client
# client = genai.Client(api_key=GEMINI_API_KEY)

# # Define the Model
# model_id = "gemini-2.0-flash"

# # Generation Config
# config = GenerateContentConfig(
#     system_instruction="You are a helpful assistant that controls device settings and recommends music based on mood.",
#     tools=[set_brightness, set_volume, detect_mood, recommend_music],  # Define callable functions
# )

# # --- Streamlit Chat UI ---
# st.title("💡 AGI for everything")

# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # Display chat messages
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# # User Input
# user_input = st.chat_input("Ask me to adjust settings or recommend music!")

# if user_input:
#     # Add user input to chat
#     st.session_state.messages.append({"role": "user", "content": user_input})
#     with st.chat_message("user"):
#         st.markdown(user_input)

#     # Check if the user is asking for music
#     if 'music' in user_input.lower():
#         # Get the recommended music based on chat history's detected mood
#         ai_response = recommend_music_based_on_history()
#     else:
#         # Otherwise, process the request as normal
#         r = client.models.generate_content(
#             model=model_id,
#             config=config,
#             contents=user_input
#         )
#         ai_response = r.text

#     # Add AI response to chat
#     st.session_state.messages.append({"role": "assistant", "content": ai_response})
#     with st.chat_message("assistant"):
#         st.markdown(ai_response)




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

# # --- Initialize Spotify Client ---
# def initialize_spotify():
#     """Authenticates and returns a Spotify client instance."""
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

# # --- System Controls ---
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

# def set_volume(level: int) -> str:
#     """Sets the system volume level (Linux)."""
#     os.system(f"pactl set-sink-volume @DEFAULT_SINK@ {level}%")
#     return f"Volume set to {level}%"

# def toggle_wifi(status: str) -> str:
#     """Turns Wi-Fi on or off."""
#     if status.lower() not in ["on", "off"]:
#         return "Invalid option. Use 'on' or 'off'."
#     os.system(f"nmcli radio wifi {status}")
#     return f"Wi-Fi turned {status}."

# def toggle_dark_mode(status: str) -> str:
#     """Toggles dark mode (GNOME-based Linux)."""
#     if status.lower() not in ["on", "off"]:
#         return "Invalid option. Use 'on' or 'off'."
#     os.system(f"gsettings set org.gnome.desktop.interface gtk-theme {'Adwaita-dark' if status == 'on' else 'Adwaita'}")
#     return f"Dark mode turned {status}."

# def lock_screen() -> str:
#     """Locks the screen."""
#     os.system("gnome-screensaver-command -l")
#     return "Screen locked."

# # --- Mood Detection ---
# def detect_mood(text: str) -> str:
#     """Analyzes text sentiment and returns mood."""
#     analysis = TextBlob(text)
#     polarity = analysis.sentiment.polarity
#     text_lower = text.lower()

#     if "angry" in text_lower or "mad" in text_lower:
#         return "angry"
#     elif "happy" in text_lower or "joy" in text_lower:
#         return "happy"
#     elif "sad" in text_lower or "depressed" in text_lower:
#         return "sad"
#     elif "stressed" in text_lower or "anxious" in text_lower:
#         return "stressed"

#     return "happy" if polarity > 0.3 else "sad" if polarity < -0.3 else "neutral"

# # --- Spotify Music Recommendation ---
# MOOD_PLAYLISTS = {
#     "happy": "37i9dQZF1DXdPec7aLTmlC",
#     "sad": "37i9dQZF1DX64Y3ftTBfaN",
#     "stressed": "37i9dQZF1DWU0ScTcjJBdj",
#     "neutral": "37i9dQZF1DX0XUsuxWHRQd",
#     "angry": "37i9dQZF1DX2DCrI7t4mmy"
# }

# def recommend_music(mood: str) -> str:
#     """Recommends a Spotify playlist based on mood."""
#     if not sp:
#         return "Spotify integration not available."

#     playlist_id = MOOD_PLAYLISTS.get(mood, MOOD_PLAYLISTS["neutral"])
    
#     try:
#         playlist = sp.playlist(playlist_id, market="US")
#         return f"🎵 Based on your mood, listen to: [{playlist['name']}]({playlist['external_urls']['spotify']})"
#     except:
#         return f"🎵 Listen here: [Spotify Playlist](https://open.spotify.com/playlist/{playlist_id})"

# # --- Integrating Gemini AI ---
# client = genai.Client(api_key=GEMINI_API_KEY)

# config = GenerateContentConfig(
#     system_instruction="You are a helpful assistant that controls device settings and recommends music based on mood.",
#     tools=[set_brightness, set_volume, toggle_wifi, toggle_dark_mode, lock_screen, detect_mood, recommend_music]
# )

# # --- Streamlit Chat UI ---
# st.title("💡 AI System Assistant")

# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # Display chat messages
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# # User Input
# user_input = st.chat_input("Ask me to adjust settings or recommend music!")

# if user_input:
#     st.session_state.messages.append({"role": "user", "content": user_input})
#     with st.chat_message("user"):
#         st.markdown(user_input)

#     # Check if user wants music recommendation
#     if 'music' in user_input.lower():
#         detected_mood = detect_mood(" ".join([msg["content"] for msg in st.session_state.messages if msg["role"] == "user"]))
#         ai_response = recommend_music(detected_mood)
#     else:
#         r = client.models.generate_content(
#             model="gemini-2.0-flash",
#             config=config,
#             contents=user_input
#         )
#         ai_response = r.text

#     st.session_state.messages.append({"role": "assistant", "content": ai_response})
#     with st.chat_message("assistant"):
#         st.markdown(ai_response)









import os
import streamlit as st
import subprocess
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from textblob import TextBlob
from google.genai.types import GenerateContentConfig
from google import genai

import requests
import json

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


import requests
import json

def send_sms_gateway_request() -> str:
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
                "Mobile": "+251935070773",
                "Text": "778"
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
            return f"SMS Gateway request successful"
        else:
            return f"Error: Unable to send request. Status code: {response.status_code}, {response.text}"
    
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"


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
        ai_response = send_sms_gateway_request()

    else:
        r = client.models.generate_content(model="gemini-2.0-flash", config=config, contents=user_input)
        ai_response = r.text

    st.session_state.messages.append({"role": "assistant", "content": ai_response})
    with st.chat_message("assistant"):
        st.markdown(ai_response)
