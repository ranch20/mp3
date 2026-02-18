import os
os.add_dll_directory(r"C:\Program Files\VideoLAN\VLC")
import vlc

from pytube import YouTube
from moviepy.editor import VideoFileClip

import urllib.request, re
import os
import json

print('-----------------------------------\n')

#GOOD
def getURL(search):
    print("Getting url...")

    Search = ''
    for i in range(0, len(search.split())):
        Search += f'{search.split()[i]}+'

    html = urllib.request.urlopen(f'https://www.youtube.com/results?search_query={Search}')
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())

    print(f'URL Obtained: https://www.youtube.com/watch?v=' + video_ids[0])
    return ("https://www.youtube.com/watch?v=" + video_ids[0])

#GOOD
def dlMP4(link):
    print("Downloading mp4...")

    yt = YouTube(link)
    title = yt.title

    # Removes annoying extra characters in titles
    replacements = [('#', ''), ('%', ''), ('&', ''), ('{', ''), ('}', ''), ('/', ''),('<', ''), ('>', ''), ('?', ''), ('\'', ''), ('.', ''), ('$', 'S')]
    for char, replacements in replacements:
        if char in title:
            title = title.replace(char, replacements)
    
    if f'{title}.mp4' in os.listdir('music/Library/temp'):
        print(f'{title} is already downloaded')
        return title
    elif f'{title}.mp3' in os.listdir('music/Library'):
        print(f'{title} is already in your library')
        return title
    else:
        yd = yt.streams.get_highest_resolution()
        yd.download('music/Library/temp', filename=f'{title}.mp4')
        print('mp4 downloaded')
        return title

# GOOD
def stripMP4():
    print("Stripping mp4 to mp3...")

    for vid in os.listdir('music/Library/temp'):
        video = VideoFileClip(f'music/Library/temp/{vid}')
        video.audio.write_audiofile(f'music/Library/{vid[:-4]}.mp3')

    print("mp4 Stripped to mp3")

def delMP4(video = None):

    if video != None: 
        print(f'Deleting {video}.mp4')
        os.remove(f'music/Library/temp/{video}')
        print(f'{video} Deleted')
    else: 
        for vid in os.listdir('music/Library/temp'): 
            print(f'Deleting {vid}')
            os.remove(f'music/Library/temp/{vid}')
            print(f'{vid} Deleted')

#GOOD
# Setup
setupInfo = os.listdir()
if 'music' not in setupInfo:
    os.mkdir('music')
    os.mkdir('music/Library')
    os.mkdir('music/Library/temp')

    with open('music/playlists.json', "w+") as Playlists:
        Playlists.write("{\"All Songs\": []}")
        Playlists.close()
    
delMP4()   # Empty temp folder on startup -- Make this toggle-able later

#GOOD
# LOAD PLAYLIST DATA
# GET RID OF THIS? MOVE IT FURTHER DOWN? WHY IS IT HERE?
# I THINK ITS HERE TO ADD NEW MANUALLY ADDED MP3's TO THE DEFAULT PLAYLIST
with open('music/playlists.json', 'r') as playlistsJSON:
    Playlists = json.load(playlistsJSON)
    playlistsJSON.close()

Library = os.listdir('music/Library')
for song in Library:
    if song.endswith('.mp3') and song[:-4] not in Playlists['All Songs']:
        Playlists['All Songs'].append(song[:-4])

current_song = {}
previous_songs = []


# TESTING
if 0:
    url = getURL("lil uzi malfunction")
    dlMP4(url)
    stripMP4()
    try: delMP4()
    except PermissionError: print("Could not empty temp folder. Will be emptied on next program start")


# NEW MUSIC PLAY PAUSE ETC. FUNCTIONS
class Song():
    def __init__(self, name):
        self.name = name
        self.player = vlc.MediaPlayer(f'music/Library/{name}.mp3')
        self.volume = 50
    def play(self):
        self.player.play()
    
    def pause(self):
        self.player.stop()
    
    def volume(self, value):
        self.player.set_audio_volume(self=self, value=value)


class Playlist():
    def __init__(self, name):
        self.name = name

    def new_playlist(name):
        if name not in Playlists.keys():
            Playlists[name] = []
            name = Playlist(name)
            playlist_dict[name.name] = name
            playlist_list.append(name)
            print(name.name)
            print(Playlists.keys())

        else: return 'Playlist name exists already'

def save_playlists():
    json_obj = json.dumps(Playlists, indent=4)


    with open('music/playlists.json', 'w') as outfile:
        outfile.write(json_obj)
        outfile.close()
    print('Playlist Data Saved')



playlist_dict = {}
playlist_list = []

for playlist in Playlists.keys():
    playlist = Playlist(playlist)
    playlist_dict[playlist.name] = playlist
    playlist_list.append(playlist.name)

dlMP4("https://youtu.be/ba0yXl6OPSA?si=Olx1-LNopJ381NuK")
stripMP4()