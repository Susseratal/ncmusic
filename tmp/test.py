from conf import config
Config = config()
Player = Config.MPV_Path
Path = Config.Music_Path

print(Player)
print(Path)
