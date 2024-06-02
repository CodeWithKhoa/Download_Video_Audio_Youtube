import os, sys
import requests
from pytube import YouTube
from pydub import AudioSegment
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
        yt = YouTube(url)
        stream = yt.streams.filter(only_audio=True).first()
        out_file = stream.download(output_path)
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        
        # Convert to mp3 if necessary
        audio = AudioSegment.from_file(out_file)
        audio.export(new_file, format="mp3")
        
        # Add metadata (ID3 tags)
        audiofile = EasyID3(new_file)
        audiofile['title'] = yt.title
        audiofile['artist'] = yt.author
        audiofile.save()

        # Remove original file
        os.remove(out_file)
        now = time.strftime("%H:%M:%S", time.localtime())
        print(f"=> {now} - Audio downloaded: {yt.title}")
        return "success"
    except Exception as e:
        print("Failed to download audio:", str(e))
        if os.path.exists(out_file):
            os.remove(out_file)
            print(f"File '{out_file}' deleted due to error.")
        return "error"

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
    try:
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
    except KeyboardInterrupt:      
        print(output_path+"\\"+title+".mp4")
        if os.path.exists(output_path+"\\"+title+".mp4"):
            try:
                # Attempt to close any open handles to the file
                with open(output_path+"\\"+title+".mp4", 'r') as f:
                    pass  # Do nothing, just attempt to open and close the file
                # Now, attempt to remove the file
                os.remove(output_path+"\\"+title+".mp4")
                print("\nExiting the program.")
                sys.exit()
            except PermissionError:
                print("File is still in use. Cannot delete.")
