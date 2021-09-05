from requests.models import Response
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import os

from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import math
from collections import Iterable

load_dotenv()

scope = "user-library-read playlist-modify-private playlist-modify-public"


def flatten(lis):
    for item in lis:
        if isinstance(item, Iterable) and not isinstance(item, str):
            for x in flatten(item):
                yield x
        else:
            yield item


class SpotifyHandler:
    def __init__(self) -> None:
        try:
            self.__client = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
            self.__my_id = self.__client.me().get("id")
        except Exception as e:
            return f"Could not connect to Spotify - Check env variables: {e}"

    def get_albums_urls(self, songs_list):
        song_properties = []
        found_songs_list = []
        for song in songs_list:
            result = self.__client.search(q=song, limit=10)
            if result.get("tracks").get("items"):
                found_songs_list.append(song)
                # print(result["tracks"]["items"][0])
                song_properties.append(
                    {
                        "url": result["tracks"]["items"][0]["album"]["external_urls"][
                            "spotify"
                        ],
                        "id": result["tracks"]["items"][0]["album"]["id"],
                    }
                )
        if found_songs_list:
            albums = dict(zip(found_songs_list, song_properties))
        else:
            albums = None
        return albums

    def get_albums_tracks(self, albums_dict):

        for album in albums_dict:
            album_id = albums_dict[album]["id"]
            tracks = self.__client.album_tracks(album_id=album_id)
            tracks_ids = [x["id"] for x in tracks["items"]]

            albums_dict[album]["tracks"] = tracks_ids
            # print(albums_dict)
        return albums_dict

    def does_playlist_exist(self, playlist_name):
        playlist_ids = [
            x["id"]
            for x in self.__client.user_playlists(self.__my_id)["items"]
            if x["name"] == playlist_name
        ]
        if len(playlist_ids) > 0:
            return playlist_ids[0]
        else:
            return False

    def create_playlist(self, albums_with_tracks, playlist_name):
        track_ids = list(
            flatten(
                [
                    [track for track in albums_with_tracks[album]["tracks"]]
                    for album in albums_with_tracks
                ]
            )
        )
        if not self.does_playlist_exist(playlist_name):
            playlist_id = self.__client.user_playlist_create(
                user=self.__my_id, name=playlist_name
            )["id"]
        else:
            playlist_id = self.does_playlist_exist(playlist_name)

        if len(track_ids) > 100:
            iteration = int(math.ceil(len(track_ids) / 100))
            for i in range(iteration):
                if i == iteration - 1:
                    track_ids_batch = track_ids[i * 100 :]
                else:
                    track_ids_batch = track_ids[i * 100 : i + 1 * 100]

                self.__client.playlist_add_items(playlist_id, track_ids_batch)
