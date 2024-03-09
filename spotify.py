import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
from dotenv import load_dotenv, dotenv_values
import os

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
scope = "playlist-modify-public"
username = os.getenv("USERNAME")
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id = client_id,
                                               client_secret = client_secret,
                                               redirect_uri = "https://example.com/",
                                               scope=scope))

playlist_name = "My fav list"
playlist_desc = "Random desc"

x = sp.user_playlist_create(user= username, 
                        name = playlist_name,
                        public= True,
                        description=playlist_desc)

print(json.dumps(x, indent = 4))

sp.current_user_unfollow_playlist(playlist_id=x['id'])

song = input("Enter the song to add: ")
song_res = sp.search(q = song)
# print(json.dumps(song_res, sort_keys=4, indent = 4))
song_res = song_res["tracks"]["items"]

for i in song_res:
    # print(json.dumps(i, sort_keys=4, indent=4))
    # print("===================================================================================================")
    
    artist = i["artists"][0]["name"]
    name = i["name"]
    song_uri = i["uri"]
    # print(artist, name, song_uri) 
    break

# print(artist, name, song_uri)

#returns json object of all playlists
prePlay = sp.user_playlists(user = username)
playlist = prePlay["items"][0]["id"]

sp.user_playlist_add_tracks(user= username, 
                            playlist_id = playlist, 
                            tracks=[song_uri])
print("done")