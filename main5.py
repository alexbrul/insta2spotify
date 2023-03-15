from time import sleep

import instaloader
import os
from moviepy.video.io.VideoFileClip import VideoFileClip
from acrcloud.recognizer import ACRCloudRecognizer
import acrcloud
import requests
import hmac
import hashlib
import spotipy
from spotipy.oauth2 import SpotifyOAuth

playlist_name = "carvingski.videos"
number_of_songs_to_scan = 20
spotify_client_id = ""
spotify_client_secret = ""
spotify_redirect_url = "http://localhost:8080"

instagram_username = "carvingski.videos"

arc_api_token = ''






# Set up Spotify credentials
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=spotify_client_id,
                                               client_secret=spotify_client_secret,
                                               redirect_uri=spotify_redirect_url,
                                               scope="playlist-modify-public playlist-modify-private"))

def download_videos(profile, amount_of_videos, folder_path):
    L = instaloader.Instaloader(dirname_pattern=os.path.join(folder_path, profile))
    profile_obj = instaloader.Profile.from_username(L.context, profile)

    counter = 0
    for post in profile_obj.get_posts():
        if counter >= amount_of_videos:
            break
        if post.typename == "GraphVideo":
            counter += 1
            L.download_post(post, target="./../"+folder_path)
            print("folder path", folder_path)
            print(f"Downloaded video {counter}/{amount_of_videos}")

download_videos(instagram_username, number_of_songs_to_scan, "./mediaNew")



def extract_audio_from_videos(folder_path):
    # Create "audio" directory if it doesn't exist
    audio_folder_path = os.path.join(folder_path, "audio")
    if not os.path.exists(audio_folder_path):
        os.makedirs(audio_folder_path)

    # Loop through all files in the directory
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path) and filename.endswith(".mp4"):
            # Extract audio from video file using moviepy
            video_clip = VideoFileClip(file_path)
            audio_clip = video_clip.audio
            audio_filename = os.path.splitext(filename)[0] + ".mp3"
            audio_path = os.path.join(audio_folder_path, audio_filename)
            audio_clip.write_audiofile(audio_path)

            # Delete the original video file
            os.remove(file_path)

            print(f"Extracted audio from {filename} and saved as {audio_filename}.")

    print("All videos processed.")

extract_audio_from_videos("./mediaNew/"+instagram_username)

# Set up ACRCloud credentials
acrcloud_access_key = ''
acrcloud_access_secret = ''
acrcloud_endpoint = 'https://identify-eu-west-1.acrcloud.com/v1/identify'

# Get the song names using ACRCloud and add them to a list

def recognize_tracks_in_folder(folder_path, api_token):
    url = 'https://api.audd.io/'
    print("recongizing tracks in folder")

    def recognize_track(file_path):
        with open(file_path, 'rb') as file:
            files = {'file': file}
            params = {
                'api_token': api_token,
                'return': 'title'
            }
            response = requests.post(url, data=params, files=files)
            response_json = response.json()
            print(response_json)
            try:
                if 'result' in response_json and 'title' in response_json['result']:
                    return ""+response_json['result']['title']+" " + response_json['result']['artist']
            except:
                return None

    tracks = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.mp3'):
            sleep(2)
            file_path = os.path.join(folder_path, filename)
            track_name = recognize_track(file_path)
            if track_name is not None:
                tracks.append(track_name)
    return tracks
folder_path = './mediaNew/'+instagram_username+'/audio/'

tracks = recognize_tracks_in_folder(folder_path, arc_api_token)

# Create a new playlist in Spotify with the profile name
playlist = sp.user_playlist_create(user=sp.current_user()['id'], name=playlist_name, public=True)

for track in tracks:
    print(track)
    # Search for the song on Spotify
    results = sp.search(q=track, type="track", limit=1)

    # Add the first result to the playlist
    if track:
        track = results["tracks"]["items"][0]["uri"]
        print(track)
        sp.playlist_add_items(playlist["id"], [track])



