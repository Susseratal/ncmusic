import curses
import sys
import time

#curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK) 
#colour stuff for foreground and background
#A_HORIZONTAL #horizontal highlight
#curses.A_REVERSE #Reverse colours to create a nice looking effect
#curses.A_HORIZONTAL?
#curses.curs_set(2) #make cursor visible (block style)

def interface(window):
    (height, width) = window.getmaxyx()
    AlbumWin = window.subwin(height,int(width/3),0,0)
    AlbumWin.box()
    col = int(2)
    content = ["Hello World", "This is some more code"]
    curses.noecho() #don't immediately echo keystrokes
    curses.curs_set(0) #make cursor invisible
    curses.use_default_colors() #use terminal's default colours
    window.box() #draw a nice box around the screen
    window.keypad(1) #enable buttons
    cursorY = int(1)
    cursorX = int(2)

    while True: #t can't delete characters, and isn't designed to be the most ideal text editor, simply testing keystroke stuff
        window.addstr(1,2, content[0], curses.A_REVERSE if (cursorY == 1) else 0) #print hello world at coords 1,2
        window.addstr(2,2, content[1], curses.A_REVERSE if (cursorY == 2) else 0) 
        window.move(cursorY, cursorX)
        window.refresh() #refresh the window
        key = window.getkey() #Get a keystroke and assign it to varaible "Key"
        if key == "q":
            sys.exit(0) #If key is q, quit out

        #elif key == "h":
        #    cursorX = (cursorX - 1)

        elif key == "j":
            cursorY = min(len(content), cursorY + 1)

        elif key == "k":
            cursorY = max(1, cursorY - 1)#Take whichever is bigger from 1, or (cursorY - 1) and assigns it to cursorY

        #elif key == "l":
        #    cursorX = (cursorX + 1)

        elif key == "b":
            curses.beep() #beep

        elif key == "/":
            #search button
            curses.beep()

        else:
            window.addstr(3, col, key) #otherwise, echo the keystroke at line 2, and the column (default value 2)
            col = col + 1 #increment column value
            window.refresh() #refresh the window

curses.wrapper(interface)
