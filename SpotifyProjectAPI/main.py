#Alexander Cramer
#Spotify API Project
#Allows user to see a selected number of top tracks from an artist(<=10)
#Uses Spotify API, generates token with client id and secret

from dotenv import load_dotenv
import os
import base64
from requests import post, get
import requests
import json
import tkinter as tk

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
username = "crameralex1"

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type":"application/x-www-form-urlencoded"
    }
    data = {"grant_type":"client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"
    
    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print("No artist with this name exists...")
        return None
    
    return json_result[0]


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




def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result

def search_artist():
    
    playlists = get_user_playlists(token, username)
    for playlist in playlists:
        print(playlist["name"])
    
    artist_name = entry.get()  # Get the artist name from the entry widget
    num_songs = int(songs_entry.get())  # Get the number of songs from the entry widget
    result = search_for_artist(token, artist_name)
    if result is not None:
        artist_id = result["id"]
        songs = get_songs_by_artist(token, artist_id)
        for idx, song in enumerate(songs[:num_songs]):
            print(f"{idx + 1}. {song['name']}")

token = get_token()

window = tk.Tk()
window.title("Artist Top Tracks")
label = tk.Label(window, text="Enter an artist:")
label.pack()
entry = tk.Entry(window)
entry.pack()
label_songs = tk.Label(window, text="Enter the number of songs(<=10):")
label_songs.pack()
songs_entry = tk.Entry(window)
songs_entry.pack()
button = tk.Button(window, text="Search", command=search_artist)
button.pack()
window.mainloop()