import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
    scope = "user-read-playback-state"
))

# Function to fetch current song from Spotify
def getCurrentSong():
    current = sp.current_playback() # Get current playback data
    if current and current.get('is_playing'):
        name = current['item']['name']
        artist = current['item']['artists'][0]['name']
        return f"{name} by {artist}"
    return "No song is currently playing"

def get_artist_id(artist_name):
    result = sp.search(q=f"artist:{artist_name}:", type="artist", limit=1)
    return result['artist']['items'][0]['id']

def get_top_tracks(artist_id):
    tracks = sp.artist_top_tracks(artist_id)['tracks']
    return [track['name'] for track in tracks]

def get_top_tracks_from_current_song():
    current = sp.current_playback()
    if current and current.get('is_playing'):
        artist_name = current['item']['artists'][0]['name']
        artist_id = get_artist_id(artist_name)
        top_tracks = get_top_tracks(artist_id)
        return top_tracks
    return []

if __name__== "__main__":
    print(getCurrentSong())

    from lyrics_api import get_lyrics

current = sp.current_playback()
if current and current.get('is_playing'):
    title = current['item']['name']
    artist = current['item']['artists'][0]['name']
    print(f"🎵 {title} by {artist}")
    print("\n--- LYRICS ---\n")
    print(get_lyrics(title, artist))