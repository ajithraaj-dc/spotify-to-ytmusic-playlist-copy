"""
Copy a Spotify playlist to YouTube Music.

Setup:
  pip install spotipy ytmusicapi
  ytmusicapi browser          # one-time: creates browser.json (paste request headers)

Env vars (from developer.spotify.com -> your app):
  SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET
  SPOTIPY_REDIRECT_URI = http://127.0.0.1:8888/callback   (add this in the app settings too)

Run:
  python spotify_to_ytmusic.py <spotify playlist link or ID>
"""
import sys
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from ytmusicapi import YTMusic

if len(sys.argv) < 2:
    sys.exit("Usage: python spotify_to_ytmusic.py <spotify playlist link or ID>")

sp = Spotify(auth_manager=SpotifyOAuth(scope="playlist-read-private"))
yt = YTMusic("browser.json")

playlist_id = sys.argv[1]
meta = sp.playlist(playlist_id, fields="name,description")

# Collect all tracks (handles playlists over 100 songs)
tracks = []
page = sp.playlist_items(playlist_id, additional_types=("track",))
while page:
    for item in page["items"]:
        t = item.get("track")
        if t and t.get("name"):
            tracks.append((t["name"], t["artists"][0]["name"]))
    page = sp.next(page) if page.get("next") else None

print(f"Found {len(tracks)} tracks in '{meta['name']}'")

video_ids, missed = [], []
for name, artist in tracks:
    results = yt.search(f"{name} {artist}", filter="songs", limit=1)
    if results:
        video_ids.append(results[0]["videoId"])
    else:
        missed.append(f"{name} - {artist}")

new_id = yt.create_playlist(
    meta["name"], meta.get("description") or "Copied from Spotify",
    video_ids=video_ids[:100],
)
for i in range(100, len(video_ids), 100):
    yt.add_playlist_items(new_id, video_ids[i:i + 100], duplicates=True)

print(f"Created playlist with {len(video_ids)} tracks.")
if missed:
    print("Not found, add manually:")
    for m in missed:
        print("  -", m)