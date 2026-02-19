import src.downloader as ytdl

with open("data/ffmpeg_location.txt", "a") as f:
    pass

with open("data/ffmpeg_location.txt", "r") as path_file:
    path = path_file.read()
    if not path: 
        path_file.close()
        with open("data/ffmpeg_location.txt", "w") as path_file:
            path = (input("Enter FFmpeg path: "))
            path_file.write(path)
            path_file.close()

input_song = input("Enter youtube link or search: ")

ytdl.main(FFmpeg_path=path, song=input_song, open_folder=True)