import pynbs
import time
import threading

from endstone.command import Command, CommandSender
from endstone.plugin import Plugin

class MusicPlugin(Plugin):
    prefix = "MusicPlayer"
    api_version = "0.5"
    load = "POSTWORLD"

    commands = {
        "music-player": {
            "description": "Play music to everyone.",
            "usages": ["/music-player <path: message>"],
            "permissions": ["music_player.command.music_player"],
        },
    }

    permissions = {
        "music_player.command.music_player": {
            "description": "Allow users to use the /music-player command.",
            "default": "op",
        },
    }

    INSTRUMENTS = {
        0:  'note.harp',           1:  'note.bassattack',
        2:  'note.bd',             3:  'note.snare',
        4:  'note.hat',            5:  'note.guitar',
        6:  'note.flute',          7:  'note.bell',
        8:  'note.chime',          9:  'note.xylobone',
        10: 'note.iron_xylophone', 11: 'note.cow_bell',
        12: 'note.didgeridoo',     13: 'note.bit',
        14: 'note.banjo',          15: 'note.pling',
    }

    def on_load(self) -> None:
        return

    def on_enable(self) -> None:
        self.register_events(self)

    def on_disable(self) -> None:
        return

    def on_command(self, sender: CommandSender, _: Command, args: list[str]) -> bool:
        path = args[0]
        path = "D:/Users/Cdm2883/Achieved/Projects/brid-geo-old/bridgeo-data/data/nbs-player/3/第五人格推理之径.nbs"

        def play():
            nbs = pynbs.read(path)
            for _, chord in nbs:
                for note in chord:
                    try:
                        sound = self.INSTRUMENTS[note.instrument]
                        volume = note.velocity
                        pitch = (2 ** ((note.key + (note.pitch / 100) - 45) / 12))
                        self.server.dispatch_command(sender, f"/execute as @a at @s run playsound {sound} @s ~~~ {volume} {pitch}")
                    except KeyError:
                        print(f"Wtf inst: {note.instrument}")
                time.sleep(nbs.header.tempo / 20)
        thread = threading.Thread(target=play)
        thread.daemon = True
        thread.start()
        return True
