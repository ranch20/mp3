'''event right click focus in musicList get music.list ACTIVE popup menu...
options add to playlist remove from library rename etc...'''

'''combobox for playlist selection
combobox = ctk.CTkComboBox(window, values=['Playlist 1', 'Playlist 2', 'Playlist 3', 'Playlist 4'], state='readonly', command=lambda x: print(x))
combobox.pack()'''


mp3 = "Path/to/file.mp3"
player = vlc.MediaPlayer(mp3)
player.play()
player.audio_set_volume(1-100)
player.stop()
player.get_length()
player.get_state()
player.get_time()

convert music to vlc library instead of pygame
add sys.argv to run headless
    > args to run a certain playlist + loops + shuffle
convert ui to pyqt6 instead of tkinter
make libvlc.dll load from include folder
