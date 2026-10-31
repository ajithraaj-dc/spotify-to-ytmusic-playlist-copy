# Spotify to YouTube Music Playlist Copier

Copy a Spotify playlist to YouTube Music with a Python script. It reads the playlist through the Spotify API, searches each song on YouTube Music, and creates a new playlist in your account.

## Requirements

- Python 3 (install from [python.org](https://www.python.org/downloads/) and tick **Add python.exe to PATH**)
- A Spotify account with an **active Premium subscription**. Spotify requires Premium for the account that owns a developer app, and without it the script fails with a `403` error.
- A YouTube Music account, logged in on a browser on the same computer

## Setup

### 1. Install the dependencies

```powershell
pip install spotipy ytmusicapi
```

If `pip` gives a launcher error, use `python -m pip install spotipy ytmusicapi` instead.

### 2. Create a Spotify developer app

1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard) and log in.
2. Click **Create app**.
3. Enter any name and description.
4. Set the **Redirect URI** to `http://127.0.0.1:8888/callback` and click **Add**.
5. Select **Web API** when asked which API you plan to use.
6. Save the app, then open **Settings** to find your **Client ID** and **Client Secret**.

> **Web API greyed out?** This is a known dashboard bug. Create the app without it, then click **Edit** on the app and add **Web API** there.

### 3. Set the environment variables

Run these in PowerShell, using your own values. They only last for the current PowerShell window.

```powershell
$env:SPOTIPY_CLIENT_ID="your_client_id"
$env:SPOTIPY_CLIENT_SECRET="your_client_secret"
$env:SPOTIPY_REDIRECT_URI="http://127.0.0.1:8888/callback"
```

### 4. Get your YouTube Music request headers

1. Open [music.youtube.com](https://music.youtube.com) and make sure you are logged in.
2. Press **F12** to open the developer tools and go to the **Network** tab.
3. Click anything on the page (like Home), then type `browse` in the filter box.
4. Click a request with status **200**.
5. Right-click it and choose **Copy → Copy request headers**. Make sure the copied text includes the `cookie:` line.
6. Paste everything into a file named `headers.txt` in the same folder as the script. In Notepad, set **Save as type** to **All files**.

### 5. Create `browser.json`

```powershell
python -c "import ytmusicapi; ytmusicapi.setup(filepath='browser.json', headers_raw=open('headers.txt').read())"
```

Check that it worked with `dir browser.json`. The file should not be empty.

### 6. Run the script

Run it from the folder that contains `spotify_to_ytmusic.py` and `browser.json`:

```powershell
python spotify_to_ytmusic.py "your Spotify playlist link"
```

The first run opens a browser window asking you to approve Spotify access. After you approve, the script creates the playlist on YouTube Music and lists any songs it could not match so you can add them by hand.

## Troubleshooting

| Problem | Fix |
| --- | --- |
| `Active premium subscription required for the owner of the app` | The Spotify account that owns the developer app needs Premium. After subscribing, it can take a few hours before requests are allowed. |
| `JSONDecodeError: Expecting value` | `browser.json` is empty or invalid. Delete it and redo step 5 from the folder you are running the script in. |
| `Fatal error in launcher` when running `pip` | Run it as `python -m pip ...` or `py -m pip ...`. |
| `can't open file ... spotify_to_ytmusic.py` | You are in the wrong folder. `cd` to the folder that contains the script. |
| YouTube Music errors after it worked before | Your cookies expired. Repeat steps 4 and 5. |

## Security

`headers.txt` and `browser.json` contain your YouTube Music session cookies, which work like a password. Do not commit them or share them. Add this to your `.gitignore`:

```
headers.txt
browser.json
```

Never commit your Spotify Client Secret either. Keep it in environment variables, as in step 3.

## No Premium?

If you do not have Spotify Premium, some tools from web like Tunemymusic can transfer a playlist from the browser without needing your own developer app.