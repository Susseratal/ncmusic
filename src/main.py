###############################################
#                                   _         #
#    _ __   ___ _ __ ___  _   _ ___(_) ___    #
#   | '_ \ / __| '_ ` _ \| | | / __| |/ __|   #
#   | | | | (__| | | | | | |_| \__ \ | (__    #
#   |_| |_|\___|_| |_| |_|\__,_|___/_|\___|   #
#                                             #
###############################################
#/usr/bin/env python

import glob
import os
import os.path
import pathlib
import sys
import curses
from enum import Enum, auto
from players import MPVPlayer
from conf import config
Config = config()
Player = MPVPlayer(Config.MPV_Path, None)

class ScreenState(Enum): #Assign numbers to variables that represent state
    SelectingArtist = auto()
    SelectingAlbumRight = auto()
    SelectingAlbumLeft = auto()
    SelectingSong = auto()
    Playing = auto()

class CursorInfo:
    def __init__(self, leftY=0, rightY=0, selected_artist=None, selected_album=None, songs=None, state=ScreenState.SelectingArtist):
        self.leftY = leftY
        self.rightY = rightY
        self.artist = selected_artist
        self.album = selected_album
        self.songs = songs
        self.state = state

def main(window):
    (height, width) = window.getmaxyx()
    leftWinWidth = int(width / 2) #Allocate half window as albumwin
    rightWinWidth = width - (leftWinWidth - 1) #allocate remaining window width as songwin
    leftWin = window.subwin(height - 10, leftWinWidth,0,0)
    rightWin = window.subwin(height - 10, rightWinWidth,0, leftWinWidth-1)
    leftWin.box()
    rightWin.box()
    cursor = CursorInfo(1, 0)
    helptext = ["1. List songs", "2. List albums", "3. Check path", "4. Show help", "5. Quit", "6. Play song", "7. Play album"]
    file_list = os.listdir(path)
    file_list = [pathlib.Path(filename) for filename in file_list]
    artist_list = [path for path in file_list if path.is_dir()]
    curses.noecho()
    curses.curs_set(0)
    window.keypad(1)
    curses.use_default_colors() # Use the default terminal colours
    window.box()
    window.refresh()

    def show_help():
        window.addstr(1,2, helptext[0], curses.A_REVERSE if (cursor.leftY == 1) else 0)
        window.addstr(2,2, helptext[1], curses.A_REVERSE if (cursor.leftY == 2) else 0)
        window.addstr(3,2, helptext[2], curses.A_REVERSE if (cursor.leftY == 3) else 0)
        window.addstr(4,2, helptext[3], curses.A_REVERSE if (cursor.leftY == 4) else 0)
        window.addstr(5,2, helptext[4], curses.A_REVERSE if (cursor.leftY == 5) else 0)
        window.addstr(6,2, helptext[5], curses.A_REVERSE if (cursor.leftY == 6) else 0)
        window.addstr(7,2, helptext[6], curses.A_REVERSE if (cursor.leftY == 7) else 0)

        #TODO Could reformat the functions to be more dynamic seeing as they need to have 3 lists and a dynamic interface

    def list_artist(artist_list):
        for (number, artist) in enumerate(artist_list, start=1):
            leftWin.addstr(number, 2, str(artist), curses.A_REVERSE if (cursor.leftY == number) else 0)
        leftWin.refresh()

    def list_album_left(artist_albums):
        for (number, album) in enumerate(artist_albums, start=1): 
            leftWin.addstr(number, 2, str(album.name), curses.A_REVERSE if (cursor.leftY == number) else 0)
        leftWin.refresh()

    def list_album_right(artist_albums):
        for (number, album) in enumerate(artist_albums, start=1): 
            rightWin.addstr(number, 2, str(album.name), curses.A_REVERSE if (cursor.rightY == number) else 0)
        rightWin.refresh()

    def list_song(song_list): #List albums in the artist window (left) and songs in the album window (right)
        for (number, song) in enumerate(song_list, start=1):
            rightWin.addstr(number, 2, str(song.name), curses.A_REVERSE if (cursor.rightY == number) else 0)
        rightWin.refresh()

    def main_menu(artist_list):
        while True:
            if cursor.state == ScreenState.SelectingArtist:
                list_artist(artist_list)
            elif cursor.state == ScreenState.SelectingAlbumRight:
                list_album_right(artist_albums) #List songs with the selected album as the value
            elif cursor.state == ScreenState.SelectingAlbumLeft:
                list_album_left(artist_albums)
            elif cursor.state == ScreenState.SelectingSong:
                list_album_left(artist_albums)
                list_song(song_list)
            elif cursor.state == ScreenState.Playing:
                pass
            else:
                assert False

            window.move(cursor.leftY, 2)
            window.refresh()
            try:
                key = window.getkey()
            except curses.error:
                # TODO: Could be that the font size has changed. Need to fix layout.
                key = None

            if key == "q":
                sys.exit(0)

            elif key == "h":
                if cursor.state == ScreenState.SelectingArtist:
                    curses.beep()
                elif cursor.state == ScreenState.SelectingSong:
                    rightWin.clear()
                    rightWin.box()
                    cursor.album = None
                    rightWin.refresh()
                    cursor.state = ScreenState.SelectingAlbumLeft
                elif cursor.state == ScreenState.SelectingAlbumLeft:
                    leftWin.clear()
                    rightWin.clear()
                    rightWin.box()
                    leftWin.box()
                    cursor.artist = None
                    cursor.state = ScreenState.SelectingArtist
                    rightWin.refresh()
                    leftWin.refresh()
                elif cursor.state == ScreenState.SelectingAlbumRight:
                    rightWin.clear()
                    rightWin.box()
                    rightWin.refresh()
                    cursor.artist = None
                    cursor.state = ScreenState.SelectingArtist
                else:
                    assert False # Highlight if an unrecognised state has occurred

            elif key == "j":
                if cursor.state == ScreenState.SelectingArtist:
                    cursor.leftY = min(len(artist_list), cursor.leftY + 1)
                elif cursor.state == ScreenState.SelectingAlbumRight:
                    cursor.rightY = min(len(artist_albums), cursor.rightY + 1)
                elif cursor.state == ScreenState.SelectingAlbumLeft:
                    cursor.leftY = min(len(artist_albums), cursor.leftY + 1)
                elif cursor.state == ScreenState.SelectingSong:
                    cursor.rightY = min(len(song_list), cursor.rightY + 1)
                else:
                    assert False

            elif key == "k":
                if cursor.state == ScreenState.SelectingArtist:
                   cursor.leftY = max(1, cursor.leftY - 1)
                elif cursor.state == ScreenState.SelectingAlbumRight:
                    cursor.rightY = max(1, cursor.rightY - 1)
                elif cursor.state == ScreenState.SelectingAlbumLeft:
                    cursor.leftY = max(1, cursor.leftY - 1)
                elif cursor.state == ScreenState.SelectingSong:
                    cursor.rightY = max(1, cursor.rightY - 1)
                else:
                    assert False

            elif key == "l":
                if cursor.state == ScreenState.SelectingSong: #looking at songs
                    curses.beep()
                elif cursor.state == ScreenState.SelectingAlbumRight: #looking at albums
                    leftWin.clear()
                    leftWin.box()
                    leftWin.refresh()
                    rightWin.clear()
                    rightWin.box()
                    rightWin.refresh()
                    cursor.album = artist_albums[cursor.rightY - 1]
                    song_list = list(sorted(cursor.album.iterdir()))
                    cursor.state = ScreenState.SelectingSong
                    cursor.leftY = cursor.rightY
                    cursor.rightY = (1)
                elif cursor.state == ScreenState.SelectingAlbumLeft:
                    rightWin.clear()
                    rightWin.box()
                    rightWin.refresh()
                    cursor.album = artist_albums[cursor.leftY - 1]
                    song_list = list(sorted(cursor.album.iterdir()))
                    cursor.state = ScreenState.SelectingSong
                    cursor.rightY = (1)
                elif cursor.state == ScreenState.SelectingArtist:
                    cursor.rightY = (1)
                    cursor.artist = artist_list[cursor.leftY - 1] #Assign cursor.album as the currently selected item in the albums list
                    artist_albums = list(sorted(cursor.artist.iterdir()))
                    cursor.state = ScreenState.SelectingAlbumRight
                else: 
                    assert False

            elif key == "p":
                if cursor.state == ScreenState.Playing:
                    Player.play_pause()
                else:
                    if cursor.state == ScreenState.SelectingSong:
                        song = (path / song_list[cursor.leftY - 1])
                        Player.play(song)
                        cursor.state = ScreenState.Playing
                    elif cursor.state == ScreenState.SelectingArtist or cursor.state == ScreenState.SelectingAlbumLeft:
                        song = (path / artist_list[cursor.leftY - 1])
                        rightWin.clear()
                        rightWin.box()
                        rightWin.addstr(1, 2, str(song))
                        rightWin.refresh()
                        #Player.play(song)
                    elif cursor.state == ScreenState.SelectingAlbumRight or cursor.state == ScreenState.SelectingSong:
                        song = (path.parent / artist_list[cursor.rightY - 1])
                        Player.play(song)

            elif key == "[":
                Player.skip_back()

            elif key == "]":
                Player.skip_forward()

            else:
                pass

            #   elif action in ["3", "check path", "path", "pwd"]:
            #       print("Current Working Directory")
            #       print(path)

            #   elif action in ["6", "play song"]:
            #       list_songs(song_list)
            #       play = int(input("Which track do you want to listen to? "))-1
            #       song = song_list[play]

            #   elif action in ["7", "play album"]:
            #       list_albums(album_list)
            #       play = int(input("Which album do you want to listen to? "))-1
            #       album = album_list[play]
            #       Player.play(album)

            #   elif action in ["pause", "please shut up", "p"]:
            #       Player.play_pause()
    main_menu(artist_list)

#path = pathlib.Path(sys.argv[0]).resolve()
#path = path.parent / ".." / "music"
path = Config.Music_Path
os.chdir(path)
curses.wrapper(main)
