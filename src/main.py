###############################################
#                                   _         #
#    _ __   ___ _ __ ___  _   _ ___(_) ___    #
#   | '_ \ / __| '_ ` _ \| | | / __| |/ __|   #   
#   | | | | (__| | | | | | |_| \__ \ | (__    #
#   |_| |_|\___|_| |_| |_|\__,_|___/_|\___|   #
#                                             #
###############################################

import glob
import os
import os.path
import pathlib
import sys
import curses
from players import MPVPlayer
Player = MPVPlayer("/usr/local/bin/mpv", None)

class CursorInfo:
    def __init__(self, albumY=0, albumX=0, songY=0, songX=0, selected_album=None):
        self.albumY = albumY
        self.albumX = albumX
        self.songY = songY
        self.songX = songX
        self.album = selected_album

def main(window):
    (height, width) = window.getmaxyx()
    albumWinWidth = int(width / 2) #Allocate half window as albunwin
    songWinWidth = width - (albumWinWidth - 1) #allocate remaining window width as songwin
    albumWin = window.subwin(height - 10, albumWinWidth,0,0)
    songWin = window.subwin(height - 10, songWinWidth,0, albumWinWidth-1)
    albumWin.box()
    songWin.box()
    cursor = CursorInfo(1, 2, 0, 0)
    helptext = ["1. List songs", "2. List albums", "3. Check path", "4. Show help", "5. Quit", "6. Play song", "7. Play album"]
    file_list = os.listdir(path)
    file_list = [pathlib.Path(filename) for filename in file_list]
    album_list = [path for path in file_list if path.is_dir()]
    song_list = [path for path in file_list if path.is_file()]
    curses.noecho()
    curses.curs_set(0)
    window.keypad(1)
    curses.use_default_colors()
    window.box()
    window.refresh()

    def show_help():
        window.addstr(1,2, helptext[0], curses.A_REVERSE if (cursor.albumY == 1) else 0)
        window.addstr(2,2, helptext[1], curses.A_REVERSE if (cursor.albumY == 2) else 0)
        window.addstr(3,2, helptext[2], curses.A_REVERSE if (cursor.albumY == 3) else 0)
        window.addstr(4,2, helptext[3], curses.A_REVERSE if (cursor.albumY == 4) else 0)
        window.addstr(5,2, helptext[4], curses.A_REVERSE if (cursor.albumY == 5) else 0)
        window.addstr(6,2, helptext[5], curses.A_REVERSE if (cursor.albumY == 6) else 0)
        window.addstr(7,2, helptext[6], curses.A_REVERSE if (cursor.albumY == 7) else 0)

    def list_songs(selected_album):
        for (number, song) in enumerate(sorted(selected_album.iterdir()), start=1): 
            songWin.addstr(number, 2, str(song.name), curses.A_REVERSE if (cursor.songY == number) else 0)
        songWin.refresh()

    def list_albums(album_list):
        for (number, album) in enumerate(album_list, start=1):
            albumWin.addstr(number, 2, str(album), curses.A_REVERSE if (cursor.albumY == number) else 0)
        albumWin.refresh()

    def main_menu(song_list, album_list):
        while True:
            if cursor.album: #if cursor.album has a value, that means we're looking at the songs for that album so we need to list songs
                list_songs(cursor.album) #List songs with the selected album as the value
            else: #This is the condition that means cursor.album has no value so be in the albums list
                list_albums(album_list)

            window.move(cursor.albumY, cursor.albumX)
            window.refresh()
            try:
                key = window.getkey()
            except curses.error:
                # TODO: Could be that the font size has changed. Need to fix layout.
                key = None

            if key == "q":
                sys.exit(0)

            elif key == "j":
                if cursor.album:
                    cursor.songY = min(len(list(cursor.album.iterdir())), cursor.songY + 1)
                else:
                    cursor.albumY = min(len(album_list), cursor.albumY + 1)

            elif key == "k":
                if cursor.album:
                    cursor.songY = max(1, cursor.songY - 1)
                else:
                    cursor.albumY = max(1, cursor.albumY - 1)

            elif key == "l":
                cursor.songY = (1)
                cursor.album = album_list[cursor.albumY - 1] #Assign cursor.album as the currently selected itemm in the albums list

            elif key == "h":
                songWin.clear()
                songWin.box()
                cursor.album = None
                songWin.refresh()

            #   action = input("What do you want to do? ").lower()
            #   if action in ["1", "songs", "list songs", "check songs"]: 
            #       list_songs(song_list) 

            #   elif action in ["2", "check albums", "albums"]:
            #       list_albums(album_list)

            #   elif action in ["3", "check path", "path", "pwd"]:
            #       print("Current Working Directory")
            #       print(path)

            #   elif action in ["4", "help", "show help", "h"]:
            #       show_help()

            #   elif action in ["5", "quit", "exit", "q"]:
            #       sys.exit()

            #   elif action in ["6", "play song"]:
            #       list_songs(song_list)
            #       play = int(input("Which track do you want to listen to? "))-1
            #       song = song_list[play]
            #       Player.play(song)

            #   elif action in ["7", "play album"]:
            #       list_albums(album_list)
            #       play = int(input("Which album do you want to listen to? "))-1
            #       album = album_list[play]
            #       Player.play(album)

            #   elif action in ["pause", "please shut up", "p"]:
            #       Player.play_pause()

            #   elif action in ["skip", "next", "]"]:
            #       Player.skip_forward()

            #   elif action in ["previous", "back", "["]:
            #       Player.skip_back()

    main_menu(song_list, album_list)

path = pathlib.Path(sys.argv[0]).resolve()
path = path.parent / ".." / "music"
os.chdir(path)
curses.wrapper(main)
