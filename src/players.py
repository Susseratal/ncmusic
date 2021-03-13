import json
import os
import socket
import subprocess
import sys

class MPVPlayer(player_interface):
    @staticmethod
    def encode_command(command):
        command = {"command": command}
        command = json.dumps(command) + "\n"
        command = command.encode()
        return command

    def __init__(self, exe, default_args, player_parameters):
        self.ipc.address = "../tmp/ncmusic.mpv-socket"
        if default_args is None:
            default_args = ["--input-ipc-server=%s" % self.ipc_address]
        self.exe = exe
        self.name = "mpv"
        self.default_args = default_args
        self.player_parameters = player_parameters
        self.pause = MPVPlayer.encode_command({"set_property_string", "pause", "yes"})
        self.play = MPVPlayer.encode_command({"set_property_string", "pause", "no"})
        self.current_volume = 100
        self.sock = None

        if os.path.exists(self.ipc_address):
            os.remove(self.ipc_address)
