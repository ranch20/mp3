import tkinter as tk
from customtkinter import *
import os, sys, platform

if os.getcwd().endswith('mp3') == False: os.chdir('mp3')

if platform.uname()[0] == 'Windows':
    os.add_dll_directory(f'C:\\Users\\{os.getlogin()}\\mp3\\include\\vlc')
else: print(platform.uname())

args = sys.argv

if len(args) > 1:
    if args[1] == "-h":
        import src.music as music

        if len(args) > 2:
            music.Playlist.play()       # ADD PLAY PLAYLIST FUNCTION IN PLAYLIST CLASS music.py
else:
    import src.music as music
    import src.ui as ui

    set_appearance_mode('dark')
    set_default_color_theme('dark-blue')

    root = CTk(fg_color='#242424')

    root.title('Music Player')
    root.geometry('940x600+810+420')

    menubar = tk.Menu(root)

    ui.main(root)

    root.mainloop()

music.save_playlists()