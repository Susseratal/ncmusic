###############################################
#                                   _         #
#    _ __   ___ _ __ ___  _   _ ___(_) ___    #
#   | '_ \ / __| '_ ` _ \| | | / __| |/ __|   #
#   | | | | (__| | | | | | |_| \__ \ | (__    #
#   |_| |_|\___|_| |_| |_|\__,_|___/_|\___|   #
#                                             #
###############################################
#/usr/bin/env python
# try and make it a 3 window layout
# new and broken

import curses
import glob
import os
import os.path
import pathlib
import sys
import time
from enum import Enum, auto
from players import MPVPlayer
from conf import config
Config = config()
Player = MPVPlayer(Config.MPV_Path, None)

class ScreenState(Enum): #Assign numbers to variables that represent state
    SelectingArtist = auto()
    SelectingAlbum = auto()
    SelectingSong = auto()

class CursorInfo:
    def __init__(self, leftY=0, midY=0, rightY=0, selected_artist=None, selected_album=None, songs=None, state=ScreenState.SelectingArtist, playing=None, songListScrollPos=0):
        self.leftY = leftY
        self.midY = midY
        self.rightY = rightY
        self.artist = selected_artist
        self.album = selected_album
        self.songs = songs
        self.state = state
        self.playing = playing
        self.songListScrollPos = songListScrollPos

def main(window):
    # Create a cursor object and some list objects
    cursor = CursorInfo(1, 0)
    file_list = os.listdir(path)
    file_list = [pathlib.Path(filename) for filename in file_list]
    artist_list = sorted([path for path in file_list if path.is_dir()])

    # Set up some basic curses settings like the colours and how it behaves on keypresses
    curses.noecho()
    curses.curs_set(0)
    window.keypad(1)
    curses.use_default_colors() 

    # Get the height and width of the window and set the width of the sub windows
    (height, width) = window.getmaxyx()
    leftWinWidth = int((width / 3) + 1)
    midWinWidth = int(leftWinWidth + 2)
    rightWinWidth = int(width - (leftWinWidth + midWinWidth) + 2)
    topWinHeight = int(height - 11)

    # Create the subwindows
    leftWin = window.subwin(height - 10, leftWinWidth, 0, 0)
    midWin = window.subwin(height - 10, midWinWidth, 0, leftWinWidth - 1)
    rightWin = window.subwin(height - 10, rightWinWidth, 0, int(leftWinWidth + midWinWidth - 2))
    bottomWin = window.subwin(10, width, height - 10, 0)

    # Box the windows
    window.box()
    leftWin.box()
    midWin.box()
    rightWin.box()
    bottomWin.box()

    # Refresh the newly boxed windows
    window.refresh()
    leftWin.refresh()
    midWin.refresh()
    rightWin.refresh()
    bottomWin.refresh()

    def list_artist(artist_list):
        for (number, artist) in enumerate(artist_list, start=1):
            leftWin.addstr(number, 2, str(artist), curses.A_REVERSE if (cursor.leftY == number) else 0)
        leftWin.refresh()

    def list_album(artist_albums):
        for (number, album) in enumerate(artist_albums, start=1): 
            midWin.addstr(number, 2, str(album.name), curses.A_REVERSE if (cursor.midY == number) else 0)
        midWin.refresh()

    def list_song(song_list): #List albums in the artist window (left) and songs in the album window (right)
        sliceEnd = cursor.songListScrollPos + topWinHeight - 1
        for (number, song) in enumerate(song_list[cursor.songListScrollPos:sliceEnd], start=1):
            rightWin.addstr(number, 2, str(song.name.removesuffix(".mp3")), curses.A_REVERSE if (cursor.rightY == number) else 0)
        rightWin.refresh()

    def main_menu(artist_list):
        song = None
        (height, width) = window.getmaxyx()
        while True: 
            songLen = len(str(song))
            songLen = int(songLen / 2)
            # Check the cursor state and list the necessary information
            if cursor.state == ScreenState.SelectingArtist:
                list_artist(artist_list)
            elif cursor.state == ScreenState.SelectingAlbum:
                list_album(artist_albums)
            elif cursor.state == ScreenState.SelectingSong:
                list_song(song_list)
            else:
                assert False

            # if it's playing, say "playing," if not, say "paused"
            # still a little janky/flickery, maybe should tweak some more
            if cursor.playing == True:
                bottomWin.addstr(1, int((width / 2) - songLen - 9), "Currently playing: " + str(song))
                bottomWin.refresh()
            elif cursor.playing == None:
                bottomWin.addstr(1, int((width / 2) - songLen - 9), "Currently paused: " + str(song))
                bottomWin.refresh()
            else:
                pass

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
                elif cursor.state == ScreenState.SelectingAlbum:
                    midWin.clear()
                    midWin.box()
                    midWin.refresh()
                    cursor.album = None
                    cursor.state = ScreenState.SelectingArtist
                elif cursor.state == ScreenState.SelectingSong:
                    rightWin.clear()
                    rightWin.box()
                    rightWin.refresh()
                    cursor.artist = None
                    cursor.state = ScreenState.SelectingAlbum
                else:
                    assert False # Highlight if an unrecognised state has occurred

            elif key == "j":
                if cursor.state == ScreenState.SelectingArtist:
                    cursor.leftY = min(len(artist_list), cursor.leftY + 1)
                elif cursor.state == ScreenState.SelectingAlbum:
                    cursor.midY = min(len(artist_albums), cursor.midY + 1)
                elif cursor.state == ScreenState.SelectingSong:
                    cursor.rightY = min(len(song_list), cursor.rightY + 1)
                    if cursor.rightY >= topWinHeight:
                        rightWin.clear()
                        rightWin.box()
                        cursor.rightY -= 1
                        if (cursor.songListScrollPos + topWinHeight) <= len(song_list): # Scroll position + height of window = num of last item on screen
                            cursor.songListScrollPos += 1
                else:
                    assert False

            elif key == "k":
                if cursor.state == ScreenState.SelectingArtist:
                   cursor.leftY = max(1, cursor.leftY - 1)
                elif cursor.state == ScreenState.SelectingAlbum:
                    cursor.midY = max(1, cursor.midY - 1)
                elif cursor.state == ScreenState.SelectingSong:
                    cursor.rightY = (cursor.rightY - 1)
                    if cursor.rightY == 0: # rightY has gone off the top of the screen
                        rightWin.clear()
                        rightWin.box()
                        cursor.rightY += 1
                        if cursor.songListScrollPos > 0:
                            cursor.songListScrollPos -= 1
                else:
                    assert False

            elif key == "l":
                if cursor.state == ScreenState.SelectingSong: #looking at songs
                    curses.beep()
                elif cursor.state == ScreenState.SelectingArtist:
                    cursor.midY = (1)
                    cursor.artist = artist_list[cursor.leftY - 1] #Assign cursor.album as the currently selected item in the albums list
                    artist_albums = list(sorted(cursor.artist.iterdir()))
                    cursor.state = ScreenState.SelectingAlbum
                elif cursor.state == ScreenState.SelectingAlbum:
                    cursor.rightY = (1)
                    rightWin.clear()
                    rightWin.box()
                    rightWin.refresh()
                    cursor.album = artist_albums[cursor.midY - 1]
                    song_list = list(sorted(cursor.album.iterdir()))
                    cursor.state = ScreenState.SelectingSong
                else: 
                    assert False

            elif key == " ":
                Player.stop()
                time.sleep(0.1) # Give the previous process time to die, should it need it. just a bandaid fix on two processes running for now. will do something proper later
                if cursor.state == ScreenState.SelectingArtist:
                    song = (path / artist_list[cursor.leftY - 1])
                    Player.play(song)
                    song = (artist_list[cursor.leftY - 1])
                    cursor.playing = True
                    bottomWin.clear()
                    bottomWin.box()
                    bottomWin.refresh()
                elif cursor.state == ScreenState.SelectingAlbum:
                    song = (path / artist_albums[cursor.midY - 1])
                    Player.play(song)
                    song = (artist_albums[cursor.midY - 1])
                    cursor.playing = True
                    bottomWin.clear()
                    bottomWin.box()
                    bottomWin.refresh()
                elif cursor.state == ScreenState.SelectingSong:
                    song = (path / song_list[cursor.rightY + cursor.songListScrollPos - 1])
                    Player.play(song)
                    song = (song_list[cursor.rightY + cursor.songListScrollPos - 1]) # want to strip the leading "00 " and trailing ".mp3" from the string
                    song = str(song)
                    song = str(song.removesuffix(".mp3"))
                    cursor.playing = True
                    bottomWin.clear()
                    bottomWin.box()
                    bottomWin.refresh()
                else:
                    pass

            elif key == "p":
                if cursor.playing:
                    Player.play_pause()
                    cursor.playing = None
                    bottomWin.clear()
                    bottomWin.box()
                    bottomWin.refresh()
                else:
                    Player.play_pause()
                    cursor.playing = True
                    bottomWin.clear()
                    bottomWin.box()
                    bottomWin.refresh()

            elif key == "[":
                Player.skip_back()

            elif key == "]":
                Player.skip_forward()

            elif key == "f":
                Player.stop()

            else:
                pass

    main_menu(artist_list)

path = Config.Music_Path
os.chdir(path)
curses.wrapper(main)
