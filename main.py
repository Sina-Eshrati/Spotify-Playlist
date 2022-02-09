from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

traveled_time = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
year = traveled_time.split('-')[0]

response = requests.get(f"https://www.billboard.com/charts/hot-100/{traveled_time}")
contents = response.text

soup = BeautifulSoup(contents, "html.parser")
songs = [song.getText() for song in soup.select(".chart-element__information__song")]
print(songs)

Client_ID = "bd9d2a0219674a37885545715eb4567d"
Client_Secret = "ac15ee41d3f646a4a6b8345d4384b425"
redirect_URI = "http://localhost:8888/callback"
scope = "playlist-modify-private"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=Client_ID,
                                               client_secret=Client_Secret,
                                               redirect_uri=redirect_URI,
                                               scope=scope
                                               ))
user_id = sp.current_user()["id"]

song_uris = []
for song in songs:
    result = sp.search(q=f"track:{song}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in spotify. skipped.")

spotify_playlist = sp.user_playlist_create(user=user_id, name=f"{traveled_time} Billboard 100", public=False)
print(spotify_playlist)
sp.playlist_add_items(playlist_id=spotify_playlist["id"], items=song_uris)
