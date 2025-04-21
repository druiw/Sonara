import os
import spotipy
import json
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
    scope = "user-read-playback-state"
))

user = sp.current_user()
displayName = user['display_name']

# Function to fetch current song from Spotify
def getCurrentSong():
    current = sp.current_playback() # Get current playback data
    #print(json.dumps(current, sort_keys=True, indent = 4))
    if current and current.get('is_playing'):
        name = current['item']['name']
        artist = current['item']['artists'][0]['name']
        return f"{name} by {artist}"
    return "No song is currently playing"

def getArtist():
    searchQuery = input("Enter an Artist: ")
    searchResults = sp.search(searchQuery, 1, 0, "artist")
    artist = searchResults['artists']['items'][0]
    artistName = artist['name']
    artistFollowers = artist['followers']['total']
    print()
    print(f"{artistName} has {artistFollowers:,} followers on Spotify!")
    #print(json.dumps(searchResults, sort_keys=True, indent = 4))


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

def getLyrics():
    from lyrics_api import get_lyrics

    current = sp.current_playback()
    
    if current and current.get('is_playing'):
        title = current['item']['name']
        artist = current['item']['artists'][0]['name']
        print(f"🎵 {title} by {artist}")
        print("\n--- LYRICS ---\n")
        print(get_lyrics(title, artist))
    else:
        print("No song is currently playing.")

if __name__== "__main__":
    print()
    print("Welcome to Sonara " + displayName + "!")
    print()
    print("What would you like to do?")
    print()
    print("0 - Search for an artist")
    print("1 - Display current playing song")
    userChoice = input(str("Enter your selection here: "))

    if userChoice == "0":
        getArtist()
    
    if userChoice == "1":
        print()
        print()
        print(getCurrentSong())
        print()
        print("Would you like to see the lyrics?")
        print("0 - Yes, display lyrics!")
        print("1 - No, take me back to main menu...")
        userChoice = input(str("Enter your selection here: "))

        if userChoice == "0":
            getLyrics()




    