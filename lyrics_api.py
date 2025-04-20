import os
import lyricsgenius
from dotenv import load_dotenv

load_dotenv()

genius = lyricsgenius.Genius(os.getenv("GENIUS_API_KEY"))

def get_lyrics(song_title, artist_name):
    try:
        song = genius.search_song(song_title, artist_name)

        # Check if the title looks like a translation or alternate version
        if song and any(tag in song.title for tag in ["Traduction", "Romanization", "Live"]):
            return "Found alternate version (e.g., translation), not showing lyrics."

        return song.lyrics if song else "Lyrics not found."
    except Exception as e:
        return f"Error fetching lyrics: {e}"