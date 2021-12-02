import curses
import glob
import os
import os.path
import pathlib
import sys
import time
from modules import MPVPlayer
from conf import config
Config = config()
Player = MPVPlayer(Config.MPV_Path, None)

class ScreenState: # Assign numbers to variables that represent state
    SelectingArtist = 1
    SelectingAlbum = 2
    SelectingSong = 3 # this allows you to increment and decrement things like any other number

##########################################################################################################################################################
# This is the thing I need to make obselete #
##########################################################################################################################################################

class CursorInfo(object):
    def __init__(self, leftY=0, midY=0, rightY=0, selected_artist=None, selected_album=None, songs=None, state=ScreenState.SelectingArtist, playing=None, artistPos=0, albumPos=0, songPos=0):
        self.leftY = leftY
        self.midY = midY
        self.rightY = rightY
        self.artist = selected_artist
        self.album = selected_album
        self.songs = songs
        self.state = state
        self.playing = playing
        self.artistPos = artistPos
        self.albumPos = albumPos
        self.songPos = songPos

##########################################################################################################################################################
# This is the thing I need to make obselete #
##########################################################################################################################################################

def formatter(state, path): # this system won't work because the formatter is just formatting the text - has no concept of the screen
    if state == 1:
        song = str(path)
        path = song.split("/")[1]
    elif state == 2:
        song = str(path)
        song = song.split("/")[2]
        path = song.removesuffix(".mp3")
    else:
        pass
    return path

class ScrollMgr:
    # initialiser creates the local variables which the entire class is going to need
    def __init__(self, window, formatter): # Needs window to draw to and list of contents passed in
        self.window = window
        self.formatter = formatter
        self.win_height = self.window.getmaxyx()[0] - 1
        self.contents = []
        self.scrollY = 0
        self.cursorY = 1

    def set_contents(self, contents): # Passes in a list such as artistList
        self.scrollY = 0
        self.cursorY = 1
        self.contents = contents # Assign ScrollMgr.contents as whatever is passed in
    
    def clear_window(self, refresh = True):
        self.window.clear()
        self.window.box()
        if refresh:
            self.window.refresh()

    def clear(self):
        self.clear_window()
        self.set_contents([])

    def draw_win(self, state, formatter):
        slice_end = self.scrollY + self.win_height - 1
        for (number, content) in enumerate(self.contents[self.scrollY:slice_end], start=1):
            self.window.addstr(number, 2, formatter(state, str(content)), curses.A_REVERSE if (self.cursorY == number) else 0) # this is where the text gets formatted
        self.window.refresh()

    def move_down(self):
        self.cursorY = min(len(self.contents), self.cursorY + 1) # Take the smaller thing from length of the list or cursorY + 1
        self.clear_window(refresh = False)
        if self.cursorY >= self.win_height:
            self.cursorY -= 1
            if self.scrollY + self.win_height <= len(self.contents):
                self.scrollY += 1

    def move_up(self):
        self.cursorY -= 1
        if self.cursorY == 0:
            self.clear_window(refresh = False)
            self.cursorY += 1
            if self.scrollY > 0:
                self.scrollY -= 1

    def get_selected_item(self):
        return self.contents[self.cursorY + self.scrollY - 1]


class Screen:
    def __init__(self, window, artistList): # Should probably swap artistList for "contents" or something variable? Unless I don't have to. will see
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
        self.bottomWin = bottomWin

        # Initialise the subwindows with contents and the windows to draw to
        self.left = ScrollMgr(leftWin, formatter) # Give self.Left an instance of the ScrollMgr, with the left window
        self.left.set_contents(artistList) # Give the left window the contents "artistList"
        self.mid = ScrollMgr(midWin, formatter)
        self.right = ScrollMgr(rightWin, formatter)
        self.window = window
        self.state = ScreenState.SelectingArtist
        self.subwin = self.left
        self.subwins = {
                ScreenState.SelectingArtist: self.left,
                ScreenState.SelectingAlbum: self.mid,
                ScreenState.SelectingSong: self.right}

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

    def draw(self):
        self.left.draw_win(0, formatter)
        self.mid.draw_win(1, formatter)
        self.right.draw_win(2, formatter)

    def move_down(self):
        self.subwin.move_down()

    def move_up(self):
        self.subwin.move_up()

    def move_right(self, contents):
        if self.state < ScreenState.SelectingSong: # increment screen state if it's less than 3 (selecting songs)
            self.state += 1 
            self.subwin = self.subwins[self.state]
            self.subwin.set_contents(contents)

    def move_left(self):
        if self.state > ScreenState.SelectingArtist:
            self.subwin.clear()
            self.state -= 1
            self.subwin = self.subwins[self.state]

    def get_selected_item(self):
        return self.subwin.get_selected_item()

 
def main(window):
    # Create a cursor object and some list objects
    cursor = CursorInfo(1, 0) # I really want to get rid of this cursor info object
    file_list = os.listdir(path) # Assigns file_list as the contents of the path
    file_list = [pathlib.Path(filename) for filename in file_list] # Get the name of every directory on the path
    artist_list = sorted([path for path in file_list if path.is_dir()]) # wtf does this do?

    # Set up some basic curses settings like the colours and how it behaves on keypresses
    curses.noecho()
    curses.curs_set(0)
    window.keypad(1)
    curses.use_default_colors() 

    mainwindow = Screen(window, artist_list)
    bottomWin = mainwindow.bottomWin # TODO

    def main_menu(artist_list):
        song = None
        (height, width) = window.getmaxyx()
        while True: 
            songLen = len(str(song))
            songLen = int(songLen / 2)
            mainwindow.draw()

            if cursor.playing == True:
                bottomWin.addstr(1, int((width / 2) - songLen - 9), "Currently playing: " + str(song))
                bottomWin.refresh()
            elif cursor.playing == None:
                bottomWin.addstr(1, int((width / 2) - songLen - 9), "Currently paused: " + str(song))
                bottomWin.refresh()
            else:
                pass

            try:
                key = window.getkey()
            except curses.error:
                # TODO: Could be that the font size has changed. Need to fix layout.
                key = None

            if key == "q":
                sys.exit(0)

            elif key == "h":
                mainwindow.move_left()

            elif key == "j":
                mainwindow.move_down()

            elif key == "k":
                mainwindow.move_up()

            elif key == "l":
                if mainwindow.state == ScreenState.SelectingArtist:
                    artist = mainwindow.get_selected_item()
                    artist_list = artist.iterdir() #Need to strip this down from DIR/DIR2 to just DIR2 - use formatter I guess
                    artist_albums = list(sorted(artist_list))
                    mainwindow.move_right(artist_albums)
                elif mainwindow.state == ScreenState.SelectingAlbum:
                    album = mainwindow.get_selected_item()
                    album_list = album.iterdir() #Need to strip this down from DIR/DIR2/MP3 to just MP3
                    album_songs = list(sorted(album_list))
                    mainwindow.move_right(album_songs)
                else:
                    curses.beep()

            elif key == " ":
                Player.stop()
                time.sleep(0.1) 
                song = mainwindow.get_selected_item()
                Player.play(song)
                cursor.playing = True

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
