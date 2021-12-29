import json
import os
import socket
import subprocess
import sys
import logging

class PlayerInterface(object):
    def __init__(self, exe, name, default_args):
        self.exe = exe
        self.name = name
        assert name in PlayerLookup.keys()
        self.default_args = default_args
        self.child = None

    def is_finished(self):
        if self.child:
            finished = self.child.poll() is not None
            if finished:
                self.child = None
            return finished
        else:
            return True

    def _play(self, filepath, allocate_pty):
        cmd = [self.exe] + self.default_args + [filepath.resolve()]
        logging.debug("PlayerInterface._play: %s", cmd)
        if allocate_pty:
            master, slave = os.openpty()
            self.child = subprocess.Popen(cmd,
                                          stdin=master,
                                          stdout=subprocess.DEVNULL,
                                          stderr=subprocess.DEVNULL)
            self.child_stdin = slave
        else:
            self.child = subprocess.Popen(cmd)
            self.child_stdin = None

    def play(self, filepath, widget=None):
        # default implementation
        return self._play(filepath, allocate_pty=False)

    def play_pause(self):
        raise NotImplementedError()

    def stop(self):
        logging.debug("PlayerInterface::stop (%s)", self.child)
        if self.child:
            self.child.kill()
            self.child = None

    def volume_change(self, change):
        pass

    def window_size_changed(self, new_size):
        pass

class MPVPlayer(PlayerInterface):
    @staticmethod
    def encode_command(command):
        command = {"command": command}
        command = json.dumps(command) + "\n"
        command = command.encode()
        return command

    def __init__(self, exe, default_args):
        self.ipc_address = "/tmp/ncmusic.mpv-socket"
        if default_args is None:
            default_args = ["--input-ipc-server=%s" % self.ipc_address, "--no-terminal", "--no-video"] # somehow need to pass in a number for --playlist-start=n
        self.exe = exe
        self.name = "mpv"
        self.default_args = default_args
        self.child = None
        self.pause = MPVPlayer.encode_command(["set_property_string", "pause", "yes"])
        self.resume = MPVPlayer.encode_command(["set_property_string", "pause", "no"])
        self.skip = MPVPlayer.encode_command(["playlist-next", "weak"])
        self.prev = MPVPlayer.encode_command(["playlist-prev", "weak"])
        self.current_volume = 100
        self.sock = None

        if os.path.exists(self.ipc_address):
            os.remove(self.ipc_address)

    def __del__(self):
        self.stop()
        if os.path.exists(self.ipc_address):
            os.remove(self.ipc_address)

    def play(self, filepath, widget=None):
        self.playing = True
        self.sock = None
        return self._play(filepath, allocate_pty=False)
    
    def play_pause(self):
        logging.debug("MPVPlayer::play_pause")
        self.send_command(self.pause if (self.playing) else self.resume)
        self.playing = not self.playing

    def skip_forward(self):
        self.send_command(self.skip)

    def skip_back(self):
        self.send_command(self.prev)

    # def loop(self):
        # Could do something with this?

    def send_command(self, command):
        if not self.child:
            return
        if self.sock is None:
            try:
                self.sock = socket.socket(socket.AF_UNIX)
                self.sock.connect(self.ipc_address)
            except FileNotFoundError:
                logging.debug("No socket found for MPV IPC")
                self.sock = None
                return

        logging.debug("MPVPlayer::send_command %s", command)
        self.sock.sendall(command)

    def volume_change(self, change):
        self.current_volume = clip(0, self.current_volume + 5 * change, 100)
        logging.debug("MPlayer::volume_change %u -> %u", change, self.current_volume)
        self.send_command(MPVPlayer.encode_command(['set_property', 'volume', self.current_volume]))
