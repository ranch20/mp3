import tkinter as tk
from tkinter import ttk as ttk
from tkinter import filedialog
#from ttkbootstrap import *
from customtkinter import *
from PIL import Image

import os

import src.music as music

play = Image.open('src/imgs/untitled.png')
pause = Image.open('src/imgs/untitled.png')
skip = Image.open('src/imgs/untitled.png')
rewind = Image.open('src/imgs/untitled.png')

print(f'Available Playlists: {music.playlist_list}')

class Music():

	class searchFrame():

		def __init__(self, root):
			self.String = StringVar()

			self.searchFrame = CTkFrame(
				root, 
				width=640, 
				height=32
				)
			self.searchbar = CTkEntry(
				self.searchFrame, 
				width=500, 
				height=32,
				placeholder_text='Search...',
				placeholder_text_color='#00ffff',
				text_color='#00ffff',
				corner_radius=0
				)
			self.download = CTkButton(self.searchFrame, 
				text='Download', 
				command=lambda: Music.searchFrame.getMusic(self),
				corner_radius=0,
				bg_color='#003350',
				fg_color='#003350',
				text_color='#ffffff',
				font=('Sans', 12),
				)

			self.searchFrame.place(x=300, y=0)
			self.searchbar.pack(side='left', fill='both')
			self.download.pack(side='right', fill='both')


			#self.searchbar.bind('<FocusIn>' and '<Key>', test) 
			'''while searchbar focus-in search library for songs
				for song found create button/label under searchbar
				to play song
				if song not in library show label "Song not in Library"
				pack button side=right "download now"'''

		def getMusic(self, musicframe):
			self.search = self.searchbar.get()
			self.link = music.getURL(self.search)
			title = music.dlMP4(self.link)
			music.stripMP4()
			Music.musicFrame.loadMusic(self=musicframe)
			music.delMP4()


	class musicFrame():

		def __init__(self, root):
			self.musicFrame = CTkFrame(
				root, 
				width=300, 
				height=600
				)
			self.buttonFrame = CTkFrame(
				self.musicFrame,
				width=315,
				height=30,
			)
			self.newPlaylist = CTkButton(
				self.buttonFrame, 
				height=30,
				width=150,
				font=('Sans', 16),
				fg_color='#ff8ff3',
				text_color='#000000',
				text='New Playlist',
				corner_radius=0,
				border_color='black',
				border_width=1,
				anchor='w',
				command=self.new_playlist
				)
			self.Playlists = CTkComboBox(
				self.buttonFrame, 
				width=150,
				font=('Sans', 16),
				text_color='#000000',
				fg_color='#ff8ff3',
				corner_radius=0,
				border_color='black',
				border_width=1,
				state=tk.NORMAL,
				justify='left',
				dropdown_fg_color='#ff8ff3',
				button_color='#003350',
				button_hover_color='white',
				dropdown_hover_color='white',
				values=music.playlist_list,
				dropdown_text_color='black',
				dropdown_font=('Sans', 12),
				command=lambda name: self.loadPlaylists(name=name),
				)
			self.scrollbar = CTkScrollbar(
				self.musicFrame,
				width=15
				)
			self.musicList = tk.Listbox(
				self.musicFrame, 
				height=20, 
				width=31,
				font=('Sans', 11),
				bg='#003350',
				fg='#ffffff',
				borderwidth=2,
				highlightcolor='#003350',
				highlightthickness=0,
				selectbackground='#ff8ff3',
				selectborderwidth=1,
				yscrollcommand=self.scrollbar.set,
				)
			self.musicInfo = CTkLabel(
				self.musicFrame,
				text='MUSIC INFO',
				height=150,
				)
			

			self.menu = tk.Menu()
			self.playlist_menu = tk.Menu()

			self.menu.bind('<Leave>', lambda x: self.menu.destroy)


			self.menu.add_cascade(label='Add To Playlist', menu=self.playlist_menu)

			for playlist in music.Playlists.keys():
				self.playlist_menu.add_command(label=playlist, command=self.add_to_playlist)

			self.scrollbar.configure(command=self.musicList.yview)
			self.Playlists.set('All Songs')

			self.musicFrame.place(x=0, y=0)
			self.buttonFrame.pack(side='top')
			self.musicInfo.pack(side='bottom', fill='both')
			self.newPlaylist.pack(side='left', fill='both')
			self.Playlists.pack(side='right', fill='both')
			self.musicList.pack(side='left', fill='both')
			self.scrollbar.pack(side='right', fill='both', padx=0)


		def loadPlaylists(self, name):
			self.musicList.delete(first=0, last='end')

			playlist = music.Playlists[name]
			for song in playlist:
				self.musicList.insert('end', song)

		def loadMusic(self):
			path = 'Library'
			print(f'Current working directory: {os.getcwd()}')
			#os.chdir(path) 
			songs = os.listdir('music/Library')
			#print(self.musicList.get(0, 'end'))
			print('Loading Library...')
			for song in songs:
				if song[:-4] not in self.musicList.get(0, 'end') and song.endswith('mp3'):
					self.musicList.insert('end', song[:-4])
					print(f'{song} Loaded Successfully')

		def getSong(self):
			return self.musicList.get(ACTIVE)
		
		def new_playlist(self):

			new_playlist_win = CTkInputDialog(
				title='Create a New Playlist',
				text='Enter Playlist Name',
			)

			music.new_playlist(new_playlist_win.get_input())
			music.save_playlists()
			


		def playSelectedSong(self):
			name = self.musicList.get(ACTIVE)
			music.current_song['Current Song'] = name

			song = music.Song(name=name)
			song.play()
			print(f'Playing {self.musicList.get(ACTIVE)}')


		def rightClickMenu(self, root, event):
			self.menu.post(event.x_root, event.y_root)	


		def add_to_playlist(self):
			
			print(self.Playlists.get(ACTIVE))
			music.Playlists[self.Playlists.get(ACTIVE)].append(self.musicList.get(ACTIVE))


			


	class mediaKeys():
		def __init__(self, root):
			self.play = CTkImage(play, None, (50,50))
			self.pause = CTkImage(pause, None, (50, 50))
			self.skip = CTkImage(skip, None, (50, 50))
			self.rewind = CTkImage(rewind, None, (50, 50))

			self.mediaFrame = CTkFrame(
				root, 
				fg_color='#242424',
				width=640, 
				height=100,
				)
			self.playButton = CTkButton(
				self.mediaFrame,
				width=50,
				height=50,
				text=None,
				image=self.play,
				fg_color='transparent',
				border_width=0,
				corner_radius=25
				)
			self.testButton = CTkButton(
				self.mediaFrame,
				width=40,
				height=100,
				text='TEST',
				corner_radius=0,
				)
			self.volumeSlider = CTkSlider(
				self.mediaFrame,
				width=150,
				from_=0, to=1,
				orientation='horizontal',
				command=lambda x: music.Song.volume(value=x),
				progress_color='#ff8ff3',
				corner_radius=0,
			)
			self.skipButton = CTkButton(
				self.mediaFrame,
				text=None,
				width=25,
				height=50,
				image=self.skip,
				fg_color='transparent',
				corner_radius=50,
			)
			self.goBackButton = CTkButton(
				self.mediaFrame,
				text=None,
				width=10,
				height=50,
				image=self.rewind,
				fg_color='transparent',
				corner_radius=50,
			)
			
			self.mediaFrame.place(x=300, y=500)
			self.goBackButton.pack(side='left')
			self.playButton.pack(side='left')
			self.skipButton.pack(side='left')
			self.volumeSlider.pack(side='left')
			self.testButton.pack(side='right')


		def pausePlay(self):
			if music.mixer.music.get_busy() is True:
				music.mixer.music.pause()
				self.playButton.configure(image=self.pause)

			elif music.mixer.music.get_busy() is False:
				music.mixer.music.unpause()
				self.playButton.configure(image=self.play)

		def skip(self):
			current_song = music.current_song['Current Song']
			length = music.get_length(current_song)
			music.mixer.music.set_pos(length*100)
			print(f'Skipping {current_song}')
			music.previous_songs.append(current_song)

		def go_back(self):
			music.mixer.music.load(f'Library/{music.previous_songs[-1]}.mp3')
			music.mixer.music.play()
			music.current_song['Current Song'] = music.previous_songs[-1]
			music.previous_songs.remove(music.previous_songs[-1])
			print(music.previous_songs)



class Options():
	def Settings(self):
		pass

	def Themes(self):
		pass



def main(root):
	root_ = root
	
	searchFrame = Music.searchFrame(root)
	musicFrame = Music.musicFrame(root)
	mediaFrame = Music.mediaKeys(root)

	musicFrame.loadMusic()
	musicFrame.musicList.bind('<FocusIn>' and '<Double -Button-1>', lambda thisVariableJustPreventsAnError: musicFrame.playSelectedSong())
	musicFrame.musicList.bind('<FocusIn>' and '<Button-3>', lambda event: musicFrame.rightClickMenu(root, event))
	musicFrame.Playlists.set('All Songs')
	musicFrame.loadPlaylists('All Songs')

	mediaFrame.playButton.configure(command=mediaFrame.pausePlay)
	mediaFrame.skipButton.configure(command=mediaFrame.skip)
	mediaFrame.goBackButton.configure(command=mediaFrame.go_back)

	searchFrame.searchbar.bind('<FocusIn>' and '<Return>', lambda x: searchFrame.getMusic(musicFrame))
	searchFrame.download.configure(command=lambda: searchFrame.getMusic(musicframe=musicFrame))
