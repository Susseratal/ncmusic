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
curses.use_default_colors()
window.box()

def show_help():
    window.addstr("1. List songs")
    window.addstr("2. List albums")
    window.addstr("3. Check path")
    window.addstr("4. Show help")
    window.addstr("5. Quit")
    window.addstr("6. Play song")
    window.addstr("7. Play album")

def list_songs(song_list):
    print("Songs:")
    for (number, song) in enumerate(song_list, start=1): 
        window.addstr(number, ". ", song)

def list_albums(album_list):
    print("Albums:")
    for (number, album) in enumerate(album_list, start=1):
        window.addstr(number, ". ", album)

def main(window):
    file_list = os.listdir(path)
    file_list = [pathlib.Path(filename) for filename in file_list]
    album_list = [path for path in file_list if path.is_dir()]
    song_list = [path for path in file_list if path.is_file()]
    main_menu(song_list, album_list)
    curses.wrapper(main)

def main_menu(song_list, album_list):
    show_help()
    while True:
        action = input("What do you want to do? ").lower()
        if action in ["1", "songs", "list songs", "check songs"]: 
            list_songs(song_list) 

        elif action in ["2", "check albums", "albums"]:
            list_albums(album_list)

        elif action in ["3", "check path", "path", "pwd"]:
            print("Current Working Directory")
            print(path)

        elif action in ["4", "help", "show help", "h"]:
            show_help()

        elif action in ["5", "quit", "exit", "q"]:
            sys.exit()

        elif action in ["6", "play song"]:
            list_songs(song_list)
            play = int(input("Which track do you want to listen to? "))-1
            song = song_list[play]
            Player.play(song)

        elif action in ["7", "play album"]:
            list_albums(album_list)
            play = int(input("Which album do you want to listen to? "))-1
            album = album_list[play]
            Player.play(album)

        elif action in ["pause", "please shut up", "p"]:
            Player.play_pause()

        elif action in ["skip", "next", "]"]:
            Player.skip_forward()

        elif action in ["previous", "back", "["]:
            Player.skip_back()

path = pathlib.Path(sys.argv[0]).resolve()
path = path.parent / ".." / "music"
os.chdir(path)
curses.wrapper(main)
