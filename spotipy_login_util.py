import spotipy
from spotipy.oauth2 import SpotifyOAuth

SPOTIFY_DEVICE_ID = "ea5609d2f3ccf1b02dc032b86a05c47c193cd0aa"  # LunchBox
# SPOTIFY_DEVICE_ID = "b8581271559fd61aa994726df743285c"  # Kitchen Speaker

scope = "user-read-playback-state,user-modify-playback-state"


def get_spotipy_obj():
    return spotipy.Spotify(
        # Cyrus Spotify Credentials
        client_credentials_manager=SpotifyOAuth(
            client_id="4e871cef2b4c4874993692f855de8ed7",
            client_secret="cfa7e3f20ef54949880f6d902fa4eaed",
            redirect_uri="http://localhost:8080",
            scope=scope,
        )
        # Jen Spotify Credentials
        # client_credentials_manager=SpotifyOAuth(
        #     client_id="1a5db297714949e7bc8ac7ba6f85bda6",
        #     client_secret="03394308b693443ebb1675233a97a3e2",
        #     redirect_uri="http://localhost:8080",
        #     scope=scope,s
        # )
    )
