import spotipy
import requests
import json
from requests import post, get

def get_user_playlists(token, username):
    url = f"https://api.spotify.com/v1/users/{username}/playlists"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for non-2xx status codes
        playlists = response.json().get("items", [])
        return playlists
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return None
    
def get_playlist_id(token, username):
    """Get the playlist ID of a user's playlists."""
    url = "https://api.spotify.com/v1/users/{}/playlists".format(username)
    response = requests.get(url, headers={"Authorization": "Bearer {}".format(token)})
    if response.status_code == 200:
        playlists_data = response.json()
        playlist_ids = []
        for playlist in playlists_data["items"]:  # Access the "items" list
            playlist_id = playlist["id"]
            playlist_ids.append(playlist_id)
        return playlist_ids
    else:
        return None
    
def get_playlist_songs(token, playlist_id):
    """Get the songs from a user's playlist."""
    sp = spotipy.Spotify(auth=token)
    response = sp.playlist_tracks(playlist_id)
    songs = []
    for item in response["items"]:
        song = item["track"]
        songs.append(song)
    return songs
    