import yt_dlp
import os
import re
import subprocess

# Ensure folder exists
os.makedirs("music/Library", exist_ok=True)


def clean_title(title):
    # Remove invalid Windows filename characters
    return re.sub(r'[\\/*?:"<>|]', "", title)


def download_mp3(url_or_search):
    print("Downloading audio...")

    ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': 'music/Library/%(title)s.%(ext)s',
    'ffmpeg_location': r'C:\Users\riley\Desktop\ffmpeg-8.0.1-essentials_build\ffmpeg-8.0.1-essentials_build\bin',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}


    # Allow search queries like "ytsearch: lil uzi malfunction"
    if not url_or_search.startswith("http"):
        url_or_search = f"ytsearch1:{url_or_search}"

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url_or_search, download=True)

        # If it was a search, extract actual video info
        if 'entries' in info:
            info = info['entries'][0]

        title = clean_title(info['title'])
        print(f"Downloaded: {title}.mp3")

    return title


def open_containing_folder(file_path):
    file_path = os.path.abspath(file_path)
    subprocess.run(['explorer', '/select,', file_path])


# Example usage
title = download_mp3("https://youtu.be/ba0yXl6OPSA?si=Olx1-LNopJ381NuK")
open_containing_folder(f"music/Library/{title}.mp3")