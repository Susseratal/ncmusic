import curses
import sys
import time

#curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK) 
#colour stuff for foreground and background

def interface(window):
    col = int(2)
    curses.noecho() #don't immediately echo keystrokes
    curses.curs_set(2) #make cursor visible (block style)
    curses.use_default_colors() #use terminal's default colours
    window.box() #draw a nice box around the screen
    window.keypad(1) #enable buttons
    window.addstr(1,2, "hello world") #print hello world at coords 1,2
    window.addstr(2,2, "this is some more code") 
    window.refresh() #refresh the window
    while True: #this can't delete characters, and isn't designed to be the most ideal text editor, simply testing keystroke stuff
        key = window.getkey() #Get a keystroke and assign it to varaible "Key"
        if key == "q":
            sys.exit(0) #If key is q, quit out
        elif key == "h":
            location = window.getyx() #get cursor position and assign location
            (x, y) = location
            x = int(x)
            y = int(y)-1
            window.move(x, y) #move cursor to new position takes args (newY, newX)
        elif key == "l":
            location = window.getyx() #get cursor position and assign location
            (x, y) = location
            x = int(x)
            y = int(y)+1
            window.move(x, y) #move cursor to new position takes args (newY, newX)
        elif key == "j":
            location = window.getyx() #get cursor position and assign location
            (x, y) = location
            x = int(x)+1
            y = int(y)
            window.move(x, y) #move cursor to new position takes args (newY, newX)
        elif key == "k":
            location = window.getyx() #get cursor position and assign location
            (x, y) = location
            x = int(x)-1
            y = int(y)
            window.move(x, y) #move cursor to new position takes args (newY, newX)
        elif key == "b":
            curses.beep() #beep
        else:
            window.addstr(2, col, key) #otherwise, echo the keystroke at line 2, and the column (default value 2)
            col = col + 1 #increment column value
            window.refresh() #refresh the window

curses.wrapper(interface)
