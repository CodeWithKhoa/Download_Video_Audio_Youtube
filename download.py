import os
import sys
import requests
import yt_dlp
from pytube import YouTube
from mutagen.easyid3 import EasyID3
import time

def load_video(auth, cookie):
    headers = {
        'accept': '*/*',
        'accept-language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7',
        'authorization': auth,
        'content-type': 'application/json',
        'cookie': cookie,
        'origin': 'https://www.youtube.com',
        'referer': 'https://www.youtube.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    }

    params = {
        'prettyPrint': 'false',
    }

    json_data = {
        'context': {
            'client': {
                'hl': 'vi',
                'gl': 'VN',
                'clientName': 'WEB',
                'clientVersion': '2.20240502.00.00',
                'osName': 'Windows',
                'osVersion': '10.0',
                'platform': 'DESKTOP',
                'clientFormFactor': 'UNKNOWN_FORM_FACTOR',
                'timeZone': 'Asia/Saigon',
                'browserName': 'Chrome',
                'browserVersion': '124.0.0.0',
            },
            'user': {
                'lockedSafetyMode': False,
            },
            'request': {
                'useSsl': True,
            },
            'clickTracking': {
                'clickTrackingParams': 'CCIQ384DGAEiEwjz5Zr44vWFAxX7nUsFHXPgBtw=',
            },
        },
        'continuation': '4qmFsgKxAxIPRkV3aGF0X3RvX3dhdGNoGoADaWdNVU1oSkZaMGxKUkhodlJsUllWbnBoVjAwbE0wVENCSUFDUjA1VFVYbFFhbWs1V1ZWRVYyMXZTMkZCYjFwbFdGSm1ZMGRHYmxwV09YcGliVVozWXpKb2RtUkdPWGxhVjJSd1lqSTFhR0pDU1daU1dHaG9Va1JzWm1SdVZuQmtNRVpYVjFVMWIxSkhXbkJhUlRsSlYwZFNkMDU2VGtObGFteERXbmh2Y1VGQlFqSmhVVUZDVm1zMFFVRldXazlCUVVWQlVtdFdNMkZIUmpCWU0xSjJXRE5rYUdSSFRtOUJRVVZDUVZGQlFVRlJRVUZCVVVWQldXdEZTVUZDU1ZSYWJXeHpaRWRXZVZwWFVtWmpSMFp1V2xZNU1HSXlkR3hpYUc5VVExQlFiRzEyYW1rNVdWVkVSbVoxWkZOM1ZXUmpMVUZITTBOSlZFTlFVR3h0ZG1wcE9WbFZSRVptZFdSVGQxVmtZeTFCUnpOT2NqWjZOVkZMUVdkblFRJTNEJTNEmgIaYnJvd3NlLWZlZWRGRXdoYXRfdG9fd2F0Y2g%3D',
    }

    response = requests.post(
        'https://www.youtube.com/youtubei/v1/browse',
        params=params,
        headers=headers,
        json=json_data,
    ).json()
    # Check 'onResponseReceivedActions'
    actions = response.get('onResponseReceivedActions', [])
    if not actions:
        print("No response actions received. Please check Cookies again!")
        return []

    # Check 'reloadContinuationItemsCommand'
    continuation_items = actions[0].get('reloadContinuationItemsCommand', {}).get('continuationItems', [])
    if not continuation_items:
        print("No continuation items.")
        return []

    urls = []
    for item in continuation_items:
        try:
            url = "https://youtube.com/watch?v=" + item['richItemRenderer']['content']['videoRenderer']['videoId']
            title = item['richItemRenderer']['content']['videoRenderer']['title']['runs'][0]['text']
            urls.append((url, title))
        except Exception as e:
            print("", end="\r")
    
    return urls

def download_youtube_audio(url, output_path):
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'postprocessor_args': [
                '-id3v2_version', '3'
            ],
            'prefer_ffmpeg': True,
            'quiet': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            title = info_dict.get('title', None)
            artist = info_dict.get('uploader', None)
            new_file = os.path.join(output_path, f"{title}.mp3")
            print(new_file)
            # Add metadata (ID3 tags)
            if os.path.exists(new_file):
                audiofile = EasyID3(new_file)
                audiofile['title'] = title
                audiofile['artist'] = artist
                audiofile.save()

            now = time.strftime("%H:%M:%S", time.localtime())
            print(f"=> {now} - Audio downloaded: {title}")
            return "success"

    except Exception as e:
        print("Failed to download audio:", str(e))
        return "error"
    except KeyboardInterrupt:
        print("KeyboardInterrupt detected. Cleaning up...")
        sys.exit()

def download_youtube_video(url, output_path):
    try:
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        stream.download(output_path)
        print(f"Video downloaded: {yt.title}")
        return "success"
    except Exception as e:
        print("Failed to download video:", str(e))
        return "error"

title = ""
output_path = ""
if __name__ == "__main__":
    output_path = input("Enter the path to save (For example: C:\\Youtube): ")
    download_choice = input("Do you want to download audio or video? (Enter 'audio' or 'video'): ").strip().lower()
    stt = 0
    cookie = input("Enter YouTube Cookie: ")
    auth = input("Enter YouTube Authorization: ")
    while True:
        video_list = load_video(auth, cookie)
        if not video_list:
            cookie = input("Enter YouTube Cookie: ")
            auth = input("Enter YouTube Authorization: ")
            video_list = load_video(auth, cookie)
        for url, title in video_list:
            stt += 1
            now = time.strftime("%H:%M:%S", time.localtime())
            print(f"{stt} - {now} - Downloading: {title}")
            try:
                if download_choice == 'audio':
                    download = download_youtube_audio(url, output_path)
                elif download_choice == 'video':
                    download = download_youtube_video(url, output_path)
                else:
                    print("Invalid selection. Please restart the program and select 'audio' or 'video'.")
                    exit(1)
                if download == "error":
                    stt -= 1
            except Exception as e:
                print(f"Unexpected error: {e}")
                stt -= 1
