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

Changelog:
Done:
        - [x] Path to directory, list files  
        - [x] List songs and albums accordingly  

To do:

        - [ ] Connect to mpv
        - [ ] Successfully play a song
        - [ ] Make a .ncmrc file so that one can configure the path
        - [ ] Package application
        - [ ] Shell script for exectution?
