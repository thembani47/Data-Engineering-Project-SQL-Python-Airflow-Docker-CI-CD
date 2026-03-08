import requests
import json
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="./.env")

CHANNEL_HANDLE = os.getenv("CHANNEL_HANDLE")
API_KEY = os.getenv("API_KEY")
url = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}"

def get_channel_playlistid():

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # print(json.dumps(data, indent=4))

        channel_items = data["items"][0]
        channel_playlistid = channel_items["contentDetails"]["relatedPlaylists"]["uploads"]

        return channel_playlistid
    except requests.exceptions.RequestException as e:
        raise e
    
if __name__ == "__main__":
    playlist_id = get_channel_playlistid()
    print(f"Playlist ID: {playlist_id}")