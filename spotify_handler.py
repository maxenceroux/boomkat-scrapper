from requests.models import Response
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import os


class SpotifyHandler:
    def __init__(self) -> None:
        try:
            self.__client = spotipy.Spotify(
                auth_manager=SpotifyClientCredentials(
                    client_id=os.environ.get("SPOTIFY_APP_CLIENT_ID"),
                    client_secret=os.environ.get("SPOTIFY_APP_CLIENT_SECRET"),
                )
            )
        except Exception as e:
            return f"Could not connect to Spotify - Check env variables: {e}"

    def get_albums_urls(self, songs_list):
        albums = {}
        for song in songs_list:
            result = self.__client.search(q=song, limit=10)
            if result.get("tracks").get("items"):
                albums[song] = result["tracks"]["items"][0]["external_urls"]["spotify"]
        return albums
