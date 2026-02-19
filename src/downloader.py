import yt_dlp
import os
import re
import subprocess

# Ensure folder exists
os.makedirs("output", exist_ok=True)
os.makedirs("data", exist_ok=True)


def clean_title(title):
    # Remove invalid Windows filename characters
    return re.sub(r'[\\/*?:"<>|]', "", title)


def download_mp3(url_or_search, ffmpeg_location):
    print("Downloading audio...")

    ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': 'output/%(title)s.%(ext)s',
    'ffmpeg_location': ffmpeg_location,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}


    # Allow search queries
    if not url_or_search.startswith("http"):
        url_or_search = f"ytsearch1:{url_or_search}"

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url_or_search, download=True)

        # If it was a search, extract actual video info
        if 'entries' in info:
            info = info['entries'][0]

        #title = clean_title(info['title'])
        title = info['title']
        print(f"Downloaded: {title}.mp3")

    return title


def open_containing_folder(file_path):
    file_path = os.path.abspath(file_path)
    subprocess.run(['explorer', '/select,', file_path])


def main(FFmpeg_path, song = None, open_folder=False):    
    title = download_mp3(song, FFmpeg_path)

    if open_folder: open_containing_folder(f"output/{title}.mp3")