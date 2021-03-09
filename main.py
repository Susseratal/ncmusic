import os
import os.path
import pathlib
import sys

def show_help():
    print("1. List songs")
    print("2. List albums")
    print("3. Check path")
    print("4. Show help")
    print("5. Quit")

def main():
    while True:
        action = input("What do you want to do? ").lower()
        if action in ["1", "songs", "list songs", "check songs"]:
            print("Songs:")
            for file in file_list: 
                songs = pathlib.Path(file)
                print(songs)
        elif action in ["2", "check albums", "albums"]:
            print("Albums:")
            for file in file_list:
                albums = pathlib.Path(file)
                if path.suffix == ".dir":
                    print(albums.stem)
        elif action in ["3", "check path", "path"]:
            print("Current Working Directory")
            print(path)
        elif action in ["4", "help", "show help"]:
            show_help()
        elif action in ["5", "quit", "exit"]:
            sys.exit()


path = pathlib.Path(sys.argv[0]).resolve()
path = path.parent / "music"
os.chdir(path)
file_list = os.listdir(path)
main()
