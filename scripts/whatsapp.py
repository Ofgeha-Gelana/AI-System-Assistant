import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth

SPOTIFY_CLIENT_ID = "2d960f832ebd4b92aa2052637c52217d"
SPOTIFY_CLIENT_SECRET = "c3b86a96a47143bd829e39ed9f98beb2"
SPOTIFY_REDIRECT_URI = "http://localhost:8080"

auth_manager = SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope="playlist-read-private"
)

sp = spotipy.Spotify(auth_manager=auth_manager)

# Check token expiry
token_info = auth_manager.get_cached_token()
if token_info:
    expires_at = token_info['expires_at']
    time_left = expires_at - time.time()
    print(f"Token expires in {int(time_left)} seconds.")
