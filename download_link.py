import os
import sys
import yt_dlp
from pytube import YouTube
from mutagen.easyid3 import EasyID3
import time

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
    while True:
        url = input("Enter Link Video Youtube: ")
        stt += 1
        now = time.strftime("%H:%M:%S", time.localtime())
        print(f"{stt} - {now} - Downloading... ")
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
        question = input("Do you want to continue ? (continue/stop): ")
        if question == "continue":
            continue
        elif question == "stop":
            print("Thank you for using our service ")
            sys.exit()
        else:
            print("You have entered incorrect syntax ")
            sys.exit()