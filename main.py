import requests
from bs4 import BeautifulSoup
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]
REDIRECT_URI = "http://example.com"

scope = "user-library-read"

song_time = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD:\n")

response = requests.get(f"https://www.billboard.com/charts/hot-100/{song_time}/")
webpage = response.text
soup = BeautifulSoup(webpage, 'html.parser')
song_list = soup.findAll(name="h3", class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 "
                                           "lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 "
                                           "u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 "
                                           "u-max-width-230@tablet-only")


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI, scope=scope))

current_user_id = sp.current_user()['id']
# Replace this with the year of your birth
year = 2000
spotify_uris = []
for song in song_list:
    results = sp.search(q=f"track:{song.get_text()} year:{year}", type="track", limit=1)

    if len(results['tracks']['items']) == 0:
        pass
    else:
        spotify_uris.append(results['tracks']['items'][0]['uri'])

playlist = sp.user_playlist_create(current_user_id, f"{song_time} Billboard 100", public=False,
                                   description="Billboard 100 playlist")

playlist_id = playlist['id']

sp.playlist_add_items(playlist_id, items=spotify_uris)
