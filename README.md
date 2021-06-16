ncmusic README
<!-- language: lang-none -->
                                        _      
         _ __   ___ _ __ ___  _   _ ___(_) ___ 
        | '_ \ / __| '_ ` _ \| | | / __| |/ __|
        | | | | (__| | | | | | |_| \__ \ | (__ 
        |_| |_|\___|_| |_| |_|\__,_|___/_|\___|

This is an ncurses client for music. Basically ncpsot, but I don't have Spotify premium and don't like Spotify.

With this in mind, I'm creating a similar interface except it's written in Python. I want it to be able to "play through the terminal" as it were, spawning a background process to play the music, but not having to launch another application. That way I can validate the existence of my program instead of just creating a roundabout and inefficient method of launching an existing program. I'd also like to package it as an actual application type thing, so it can be installed and it automatically creates a music directory. Either you can point it at a different directory or put all your music in the directory it created.  

If none of this made sense, you now have documented evidence of my stupidity. If it did, I hope you enjoy!
~ Iain xx

Recommended Directory structure:  
Artists > Albums > songs  
This is what I've set the variable names to reflect, but if you want to restructure it, just be aware that some code edits may be necessary

Changelog:  
Done:

        - [x] Path to directory, list files  
        - [x] List songs and albums accordingly  
        - [x] Install mpv
        - [x] Proper file vs dir control as seperate lists
        - [x] Connect to mpv
        - [x] Successfully play a song
        - [x] Play albums
        - [x] Play and pause
        - [x] Skip songs in albums
        - [x] create a basic interface program in curses (interface.py)
        - [x] get control of buttons in curses
        - [x] highlighting
        - [x] List Albums
        - [x] get curses working in main file
        - [x] List songs
        - [x] Make it ignore .DS_Store
        - [x] Change dir structure to be artists > albums > songs
        - [x] Make window reflect that change
        - [x] Cycle through windows with "h" and "l" and list songs (sorted) 
        - [x] Cycle through windows with "j" and "k"
        - [x] /tmp contains test files and code snippets
        - [x] pressing "p" now spanws an MPV process, it just can't be heard

To do:

        - [ ] make it so that you can hear the music
        - [ ] add state to track list selection seperately from window 
        - [ ] scrolling
        - [ ] don't crash when song names are long
        - [ ] play songs
        - [ ] music progress bar
        - [ ] song control
        - [ ] Make the dir structure easily configurable
        - [ ] Make a .ncmrc file so that one can configure the path
        - [ ] Package application
        - [ ] Shell script for exectution?
