ncmusic README
<!-- language: lang-none -->
                                        _      
         _ __   ___ _ __ ___  _   _ ___(_) ___ 
        | '_ \ / __| '_ ` _ \| | | / __| |/ __|
        | | | | (__| | | | | | |_| \__ \ | (__ 
        |_| |_|\___|_| |_| |_|\__,_|___/_|\___|

This is an ncurses based nusic client written in python. I am considering rewriting this in C or C# or something like that, just for the learning experience. There are a few things you should know going into this:  
The program comes with a default config file, if you just do 

        cp config.def.py config.py

you can then delete config.def.py once you've given config.py your path to your music directory and installation of MPV. While relative paths should work fine, absolute paths are probably more sensible.  
The Music_Path in the config file should go to the top most "music" directory, which should then look like:  
Music/Artists/Albums/Songs  
This is what I've set the variable names to reflect, but if you want to restructure it, just be aware that some code edits may be necessary.  

The controls are vim based (or at least vim inspired), I'll probably make them configurable at some point, but they're not just yet. They are as follows:  

        K == Up
        J == Down
        H == Left
        L == Right
        Space bar == Play selected song
        P == play/pause
        [ == skip back a track
        ] == skip forward a track
        g == jump to top of list
        G == jump to bottom of list

note: Skipping forward and back only works when you've selected an entire artist or album to play. pressing play on track 2 of an album, for instance, just plays track 2, rather than the entire album starting from track 2  
As I say, player is unfinished, but in the most baseline usable state

Second Note: If you scale up the terminal or change the font size, the program gets upset. if the text goes of the screen, it crashes. scrolling isn't a feature yet. it's on the todo list
