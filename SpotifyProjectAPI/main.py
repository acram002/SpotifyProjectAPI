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
import spotipy
import user_data

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

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

def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result
        
def call_playlist_id():
    username = username_entry.get()
    playlist_ids = user_data.get_playlist_id(token, username)
    for playlist_id in playlist_ids:
        songs = user_data.get_playlist_songs(token, playlist_id)
        for song in songs:
            print(song["name"])

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
label_username = tk.Label(window, text="Enter username:")
label_username.pack()
username_entry = tk.Entry(window)
username_entry.pack()
button = tk.Button(window, text="Search Username", command=call_playlist_id)
button.pack()
window.mainloop()