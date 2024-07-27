import base64
import requests
import json
from dotenv import load_dotenv
import os

#load environment variables
load_dotenv()

#get client ID and client secret from environment variables
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

#function to get access token from Spotify API
def get_token():
    auth_string = f"{CLIENT_ID}:{CLIENT_SECRET}"
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")
    headers = {
        "Authorization": f"Basic {auth_base64}"
    }
    data = {
        "grant_type": "client_credentials"
    }
    response = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)
    token = response.json().get("access_token")
    return token

#function to search for track and return track names and IDs
def search_for_track(token, track_name):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    params = {
        "q": track_name,
        "type": "track",
        "limit": 10
    }
    response = requests.get("https://api.spotify.com/v1/search", headers=headers, params=params)
    json_result = response.json().get("tracks", {}).get("items", [])
    track_info_list = []
    for item in json_result:
        track_info = {
            "name": item.get("name"),
            "id": item.get("id"),
            "artist": ", ".join(artist.get("name") for artist in item.get("artists")),
            "artist_ids": [artist.get("id") for artist in item.get("artists")],  # Store artist IDs
            "album": item.get("album").get("name"),
            "release_date": item.get("album").get("release_date"),
            "popularity": item.get("popularity")
        }
        track_info_list.append(track_info)
    return track_info_list

#function to get audio features for a list of track IDs
def get_audio_features(token, track_ids):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    params = {
        "ids": ",".join(track_ids)
    }
    response = requests.get("https://api.spotify.com/v1/audio-features", headers=headers, params=params)
    audio_features = response.json().get("audio_features")
    return audio_features

def get_audio_features_for_tracks(token, track_ids):
    #call get_audio_features function for each track ID and combine the results
    all_audio_features = []
    for track_id in track_ids:
        audio_features = get_audio_features(token, [track_id])
        all_audio_features.extend(audio_features)
    return all_audio_features

def get_artist_details(token, artist_ids):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    params = {
        "ids": ",".join(artist_ids)
    }
    response = requests.get("https://api.spotify.com/v1/artists", headers=headers, params=params)
    artist_details = response.json().get("artists")
    return artist_details

if __name__ == "__main__":
    token = get_token()
    track_info = search_for_track(token, "Imagine")
    artist_ids = list(set(artist_id for track in track_info for artist_id in track['artist_ids']))
    artist_details = get_artist_details(token, artist_ids)
    for artist in artist_details:
        print(artist['name'], artist['genres'])
