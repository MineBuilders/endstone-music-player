import math
import random
from enum import Enum, auto
from numbers import Number

from endstone import Player
from endstone.scheduler import Task
from pynbs import Note

from endstone_music_player import MusicPlugin


class PlayOrder(Enum):
    SEQUENCE = auto()
    RANDOM = auto()
    REPEAT_ONE = auto()
    REPEAT_LIST = auto()


from endstone_music_player.music_storage import MusicPlayerData
from endstone_music_player.songs.song import Song


class MusicPlayer(MusicPlayerData):
    INSTRUMENTS = {
        0: 'note.harp', 1: 'note.bassattack',
        2: 'note.bd', 3: 'note.snare',
        4: 'note.hat', 5: 'note.guitar',
        6: 'note.flute', 7: 'note.bell',
        8: 'note.chime', 9: 'note.xylobone',
        10: 'note.iron_xylophone', 11: 'note.cow_bell',
        12: 'note.didgeridoo', 13: 'note.bit',
        14: 'note.banjo', 15: 'note.pling',
    }

    def __init__(self, plugin: MusicPlugin):
        super().__init__()
        self.plugin = plugin
        self.listeners: list[Player] | None = []
        self._notes: dict[Number, list[Note]] | None = None
        self._task: Task | None = None
        self.playing = False

    def play(self, song: Song | None = None):
        print("play")
        if song is not None:
            self.reset()
            self.song = song
            self.play()
            return
        if self.song is None:
            self.next()
            return

        self.pause()
        self._notes = dict(self.song.to_nbs())
        self.playing = True
        self._task = self.plugin.server.scheduler.run_task(
            self.plugin,
            lambda: self._frame(),
            0,
            math.ceil(20 / self.song.to_nbs().header.tempo)
        )

    def _frame(self):
        print(f"_frame {self.tick}")
        notes = self._notes.get(self.tick)
        for note in notes or []:
            if self.song.to_nbs().layers[note.layer].lock: continue
            sound = self.INSTRUMENTS.get(note.instrument)
            if sound is None: continue
            volume = note.velocity
            pitch = 2 ** ((note.key + (note.pitch / 100) - 45) / 12)
            for listener in self.listeners:
                print(f"{listener.name} {self.tick} : playsound {sound} <- {volume} {pitch}")
                self.plugin.server.dispatch_command(listener, f"/execute as @s at @s run playsound {sound} @s ~~~ {volume} {pitch}")
                # listener.play_sound(listener.location, sound, volume, pitch)
        self.tick += 1
        if self.tick >= self.song.to_nbs().header.song_length:
            self.next()

    def next(self):
        print("next")
        self.reset()
        if len(self.songs) == 0:
            return
        if self.song is None:
            return self.play(random.choice(self.songs) if self.order == PlayOrder.RANDOM else self.songs[0])
        if self.order == PlayOrder.REPEAT_ONE:
            return self.play()
        if self.order == PlayOrder.RANDOM:
            return self.play(random.choice(self.songs))
        try:
            index_next = self.songs.index(self.song) + 1
        except ValueError:
            self.song = None
            return
        if index_next < len(self.songs):
            return self.play(self.songs[index_next])
        if self.order == PlayOrder.REPEAT_LIST:
            return self.play(self.songs[0])
        if self.order == PlayOrder.SEQUENCE:
            self.song = None

    def reset(self):
        print("reset")
        self.pause()
        self._notes = None
        self.tick = 0

    def pause(self):
        print("pause")
        self.playing = False
        if self._task is not None: self._task.cancel()
        self._task = None
