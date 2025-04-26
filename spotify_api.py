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
    scope = "user-read-playback-state user-read-private user-modify-playback-state"
))

# User Details
user = sp.current_user()
displayName = user['display_name']
userFollowers = user['followers']['total']
userSubscriptionType = user.get("product", "unknown")

#Call to display user JSON data
#print(json.dumps(user, indent=2)) 

# Function to skip song (User must be a premium member of Spotify)
def skipSong():
    isPremium = False
    if userSubscriptionType == 'premium':
        isPremium = True
        try:
            sp.next_track()
            print("Skipped to next track 🎵")
        except spotipy.SpotifyException as e:
            print("Failed to skip track. ⚠️")
    else:
        print("Must be premium member to skip tracks.")

# Function to fetch current song from Spotify
def getCurrentSong():
    current = sp.current_playback() # Get current playback data
    #print(json.dumps(current, sort_keys=True, indent = 4))
    if current and current.get('is_playing'):
        name = current['item']['name']
        artist = current['item']['artists'][0]['name']
        return f"{name} by {artist}"
    return "No song is currently playing"

# Get the album art of the song playing
def getCurrentAlbumArt():
    current = sp.current_playback()
    albumArt = current['item']['album']['images'][0]['url']
    print(json.dumps(current, sort_keys=True, indent=4))
    return albumArt

def getArtist():
    searchQuery = input("Enter an Artist: ")  # Ask the user to type an artist name
    searchResults = sp.search(searchQuery, type="artist", limit=1)  # Use Spotify API to search for the artist
    items = searchResults['artists']['items']  # Extract the list of matching artists from the search results

    if not items:  # If no artists were found
        print("No artist found with that name.")  # Let the user know
        return None  # Exit the function early

    artist = items[0]  # Take the first artist result from the list
    return artist  # Return the artist dictionary for use in other functions

def getArtistFollowers(artist):
    artistName = artist['name']  # Get the artist's name
    artistFollowers = artist['followers']['total'] # Get the artist's total number of followers
    print(f"{artistName} has {artistFollowers:,} followers on Spotify!")  # Formatted follower count

def get_artist_id(artist_name):
    result = sp.search(q=f"artist:{artist_name}", type="artist", limit=1)
    return result['artists']['items'][0]['id']

def get_top_tracks(artist_id):
    tracks = sp.artist_top_tracks(artist_id)['tracks']
    return [track['name'] for track in tracks]
    
def get_top_track_objects(artist_id):
    return sp.artist_top_tracks(artist_id)['tracks']

def getTrackDetails(artist_id):
    try:
        choice = input("Enter the number listed to the left of the track you would like to view the details for: ")
        choiceInt = int(choice)

        if 0 <= choiceInt <=len(track_list):
            track = track_list[choiceInt]
            print("\n🎵 Track Details:\n")
            print(f"Title:          : {track['name']}")
            print(f"Album:          : {track['album']['name']}")
            print(f"Album Artist    : {track['album']['images'][0]['url']}")
            print(f"Duration        : {track['duration_ms'] // 1000} seconds")
            print(f"Preview url     : {track['preview_url'] or 'No preview available'}")
        else:
            print("Invalid number. Please try again.")
        
    except ValueError:
        print("Invalid input. Please enter a number.")

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


#########################################################################################################################
# User Navigation Menu
def mainMenu():
    print()
    print("Welcome to Sonara " + displayName + "!")
    print()
    print("What would you like to do?")
    print()
    print("0 - Search for an artist")
    print("1 - Display current playing song")
    print("2 - Skip Song")
    print("3 - Close app")
    userChoice = input(str("Enter your selection here: "))

    if userChoice == "0":
        artistData = getArtist()
        artistName = artistData['name']
        print()
        print("0 - View " + artistName + "'s followers")
        print("1 - View " + artistName + "'s top 10 tracks")
        print("2 - Return to main menu")
        userChoice = input(str("Enter your selection: "))

        if userChoice == "0":
            print()
            getArtistFollowers(artistData)
            mainMenu()
        
        if userChoice == "1":
            print()
            artistID = get_artist_id(artistName)
            topTracks = get_top_tracks(artistID)
            for i, track in enumerate(topTracks, start = 1):
                print(f"{i}. {track}")
            print()
            print("0 - View specific track details")
            print("1 - Return to main menu")
            userChoice = input(str("Enter your selection: "))

            if userChoice == "0":
                getTrackDetails(artistID)
                
            if userChoice == '1':
                mainMenu()

        if userChoice == "2":
            mainMenu()
    
    if userChoice == "1":
        print()
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print(getCurrentSong())
        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        print()

        if getCurrentSong() == "No song is currently playing":
            mainMenu()

        print("Would you like to see the lyrics?")
        print("0 - Yes, display lyrics!")
        print("1 - No, take me back to main menu...")
        userChoice = input(str("Enter your selection here: "))

        if userChoice == "0":
            getLyrics()
            mainMenu()
        else:
            mainMenu()

    elif userChoice == "2":
        skipSong()
        currentSong = getCurrentSong()
        print()
        print("Now playing " + currentSong)
        mainMenu()

    elif userChoice == "3":
        print("Thanks for using Sonara! 🎧")
        exit()

    elif userChoice == "4":
        print("Dev Controls")
        print("0 - Skip Track")
        userChoice = input("Enter your selection here: ")
        if userChoice == "0":
            getCurrentAlbumArt()

    else:
        print("Invalid input... Try again!")
        mainMenu()

if __name__== "__main__":
    mainMenu()



    