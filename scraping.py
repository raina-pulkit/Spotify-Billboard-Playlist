# Simple python application to scrape data from BillBoard and create a playlist of those top 100 songs from a particular year
import requests
from bs4 import BeautifulSoup

year = input("Enter the date you wish to create playlist for in DD-MM-YYYY format: ").split('-')
date, month, yr = year[0], year[1], year[2]
extension = yr + "-" + month + "-" + date + "/"
url = "https://www.billboard.com/charts/hot-100/" + extension

res = requests.get(url)
soup = BeautifulSoup(res.text, "html.parser")

top100 = soup.find_all(name = "div", class_ = "o-chart-results-list-row-container")
songs = []
for i in top100:
    i = i.select_one("ul")
    position = int(i.select_one("li span").text.strip())
    s = i.select_one("li.lrv-u-width-100p ul li")
    songName = s.find(name="h3").text.strip()
    artist = s.find(name = "span").text.strip()
    songs.append([position, songName, artist])
songs.sort(key=lambda x: x[0])
# Now songs contains all the songs in sorted order

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
from dotenv import load_dotenv, dotenv_values
import os

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
scope = "playlist-modify-public"
username = os.getenv("USER_NAME")

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id = client_id,
                                               client_secret = client_secret,
                                               redirect_uri = "https://example.com/",
                                               scope=scope))

whichMonth = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December",
}

playlist_name = f"Travel back to {whichMonth[int(month)]} of {yr}"
playlist_desc = f"Billboard Top 100 songs from the week of {date} of {whichMonth[int(month)]}, {yr}"
playlist_created = sp.user_playlist_create(user= username, 
                        name = playlist_name,
                        public= True,
                        description=playlist_desc)
playlist_created = playlist_created["id"]

tracks = []
for songItem in songs:
    songQuery = songItem[1]
    artistQuery = songItem[2]
    # print("Searching for", songQuery, artistQuery)
    song_res = sp.search(q = f"artist:{artistQuery} track:{songQuery}")
    # print(json.dumps(song_res, sort_keys=4, indent = 4))
    song_res = song_res["tracks"]["items"]

    # print(json.dumps(i, sort_keys=4, indent=4))
    # print("===================================================================================================")

    if(len(song_res) == 0): continue
    
    artist = song_res[0]["artists"][0]["name"]
    name = song_res[0]["name"]
    song_uri = song_res[0]["uri"]
    tracks.append(song_uri)

    # print(artist, name, song_uri)

# print(tracks)
sp.user_playlist_add_tracks(user= username, 
                                playlist_id = playlist_created, 
                                tracks=tracks)
