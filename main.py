from requests.cookies import create_cookie
import spotipy
from spotify_handler import SpotifyHandler
from dotenv import load_dotenv
import os
from boomkat_handler import BoomkatHandler
from spotify_handler import SpotifyHandler

load_dotenv()

env = "prod"

if __name__ == "__main__":
    boomkat = BoomkatHandler(driver_path=os.environ.get("DRIVER_PATH"))
    if env == "prod":
        bestsellers = boomkat.get_bestsellers_list()
    if env == "dev":
        bestsellers = [
            "Moritz Von Oswald Trio Dissent",
            "Bendik Giske Cracks",
            "Felisha Ledesma Fringe",
            "Dijit Tapes & Krikor Remixes",
            "Ultravillage Elements",
            "THE CARETAKER Everywhere At The End Of Time Stages 1-3 (Vinyl Set)",
            "LUC FERRARI Labyrinthe de Violence",
        ]
    spotify = SpotifyHandler()

    albums = spotify.get_albums_urls(bestsellers)

    albums_with_tracks = spotify.get_albums_tracks(albums)
    spotify.create_playlist(albums_with_tracks, "test_api")
