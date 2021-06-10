###############################################
#                                   _         #
#    _ __   ___ _ __ ___  _   _ ___(_) ___    #
#   | '_ \ / __| '_ ` _ \| | | / __| |/ __|   #   
#   | | | | (__| | | | | | |_| \__ \ | (__    #
#   |_| |_|\___|_| |_| |_|\__,_|___/_|\___|   #
#                                             #
###############################################

# TODO currently: artists is albums, albums is songs and you can't see songs

import glob
import os
import os.path
import pathlib
import sys
import curses
from players import MPVPlayer
Player = MPVPlayer("/usr/local/bin/mpv", None)

class CursorInfo:
    def __init__(self, artistY=0, artistX=0, albumY=0, albumX=0, selected_artist=None):
        self.artistY = artistY
        self.artistX = artistX
        self.albumY = albumY
        self.albumX = albumX
        self.artist = selected_artist

def main(window):
    (height, width) = window.getmaxyx()
    artistWinWidth = int(width / 2) #Allocate half window as albumwin
    albumWinWidth = width - (artistWinWidth - 1) #allocate remaining window width as songwin
    artistWin = window.subwin(height - 10, artistWinWidth,0,0)
    albumWin = window.subwin(height - 10, albumWinWidth,0, artistWinWidth-1)
    artistWin.box()
    albumWin.box()
    cursor = CursorInfo(1, 2, 0, 0)
    helptext = ["1. List songs", "2. List albums", "3. Check path", "4. Show help", "5. Quit", "6. Play song", "7. Play album"]
    file_list = os.listdir(path)
    file_list = [pathlib.Path(filename) for filename in file_list]
    artist_list = [path for path in file_list if path.is_dir()]
    album_list = [path for path in file_list if path.is_file()]
    curses.noecho()
    curses.curs_set(0)
    window.keypad(1)
    curses.use_default_colors()
    window.box()
    window.refresh()

    def show_help():
        window.addstr(1,2, helptext[0], curses.A_REVERSE if (cursor.artistY == 1) else 0)
        window.addstr(2,2, helptext[1], curses.A_REVERSE if (cursor.artistY == 2) else 0)
        window.addstr(3,2, helptext[2], curses.A_REVERSE if (cursor.artistY == 3) else 0)
        window.addstr(4,2, helptext[3], curses.A_REVERSE if (cursor.artistY == 4) else 0)
        window.addstr(5,2, helptext[4], curses.A_REVERSE if (cursor.artistY == 5) else 0)
        window.addstr(6,2, helptext[5], curses.A_REVERSE if (cursor.artistY == 6) else 0)
        window.addstr(7,2, helptext[6], curses.A_REVERSE if (cursor.artistY == 7) else 0)

    def list_artist(artist_list):
        for (number, artist) in enumerate(artist_list, start=1):
            artistWin.addstr(number, 2, str(artist), curses.A_REVERSE if (cursor.artistY == number) else 0)
        artistWin.refresh()

    def list_album(selected_artist):
        for (number, album) in enumerate(sorted(selected_artist.iterdir()), start=1): 
            albumWin.addstr(number, 2, str(album.name), curses.A_REVERSE if (cursor.albumY == number) else 0)
        albumWin.refresh()

    def main_menu(artist_list, album_list):
        while True:
            if cursor.artist: #if cursor.album has a value, that means we're looking at the albums by the selected artist
                list_album(cursor.artist) #List songs with the selected album as the value
            else: #This is the condition that means neither cursor.artist or cursor.album has a value so be in the artists list
                list_artist(artist_list)

            window.move(cursor.artistY, cursor.artistX)
            window.refresh()
            try:
                key = window.getkey()
            except curses.error:
                # TODO: Could be that the font size has changed. Need to fix layout.
                key = None

            if key == "q":
                sys.exit(0)

            elif key == "h":
                if cursor.artist:
                    albumWin.clear()
                    albumWin.box()
                    cursor.artist = None
                    albumWin.refresh()
                else:
                    pass

            elif key == "j":
                if cursor.artist:
                    cursor.albumY = min(len(list(cursor.artist.iterdir())), cursor.albumY + 1)
                else:
                    cursor.artistY = min(len(artist_list), cursor.artistY + 1) #need to fix so it knows what artist's albums it's looking at

            elif key == "k":
                if cursor.artist:
                    cursor.albumY = max(1, cursor.albumY - 1)
                else:
                    cursor.artistY = max(1, cursor.artistY - 1)

            elif key == "l":
                if cursor.artist:
                    pass
                else:
                    cursor.albumY = (1)
                    cursor.artist = artist_list[cursor.artistY - 1] #Assign cursor.album as the currently selected itemm in the albums list

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

    main_menu(artist_list, album_list)

path = pathlib.Path(sys.argv[0]).resolve()
path = path.parent / ".." / "music"
os.chdir(path)
curses.wrapper(main)
