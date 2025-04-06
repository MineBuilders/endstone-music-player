import json
import os
from dataclasses import dataclass, field

from endstone import Player

from endstone_music_player import MusicPlugin
from endstone_music_player.music_player import PlayOrder
from endstone_music_player.songs.song import Song


@dataclass
class MusicPlayerData:
    order = PlayOrder.SEQUENCE
    songs: list[Song] = field(default_factory=list)
    song: Song | None = None
    tick = 0

    def __post_init__(self):
        if self.songs is None:
            self.songs = []

    def copy(self, source: "MusicPlayerData"):
        self.order = source.order
        self.songs = source.songs
        self.song = source.song
        self.tick = source.tick
        return self

    def encode(self):
        songs = [[song.__class__.__name__, song.encode()] for song in self.songs]
        try:
            song_index = self.songs.index(self.song)
        except ValueError:
            song_index = None
        return json.dumps({
            "order": self.order.name,
            "songs": songs,
            "song": song_index,
            "tick": self.tick,
        })

    @staticmethod
    def decode(data: str):
        data = json.loads(data)
        copy = MusicPlayerData([])
        copy.order = PlayOrder[data["order"]]
        copy.songs = [
            clazz.decode(value)
            for name, value in data["songs"]
            for clazz in Song.get_types()
            if clazz.__name__ == name
        ]
        if data["song"] is not None:
            copy.song = copy.songs[data["song"]]
        copy.tick = data["tick"]
        return copy


class MusicPlayerStorage:
    ROOT_PATH = "plugins/music_player"
    SONGS_ROOT_PATH = ROOT_PATH + "/songs"
    SONGS_CACHE_PATH = ROOT_PATH + "/.cache"
    PLAYER_CACHE_PATH = ROOT_PATH + "/.player"
    DATA_DICT = {}
    GLOBAL_KEY = "GLOBAL"

    @staticmethod
    def get(plugin: MusicPlugin, player: Player):
        from endstone_music_player.music_player import MusicPlayer
        key = player.unique_id.hex
        cache = MusicPlayerStorage.DATA_DICT.get(key)
        if cache is not None: return cache
        cache = MusicPlayerStorage.read_raw(key)
        cache = MusicPlayer(plugin).copy(cache)
        cache.listeners.append(player)
        MusicPlayerStorage.DATA_DICT[key] = cache
        return cache

    @staticmethod
    def save(plugin: MusicPlugin):
        for key, value in MusicPlayerStorage.DATA_DICT.items():
            MusicPlayerStorage.write_raw(key, value)
        from endstone_music_player.music_player_global import MusicPlayerGlobal
        MusicPlayerStorage.write_raw(MusicPlayerStorage.GLOBAL_KEY, MusicPlayerGlobal(plugin))

    @staticmethod
    def read_raw(name: str):
        file_path = _resolve_player_cache(name)
        try:
            with open(file_path, 'r') as file:
                return MusicPlayerData.decode(file.read())
        except FileNotFoundError:
            return MusicPlayerData()

    @staticmethod
    def write_raw(name: str, data: MusicPlayerData):
        file_path = _resolve_player_cache(name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file: file.write(data.encode())


def resolve_songs(path: str):
    return os.path.join(MusicPlayerStorage.SONGS_ROOT_PATH, path)


def resolve_songs_cache(path: str):
    return os.path.join(MusicPlayerStorage.SONGS_CACHE_PATH, path)


def _resolve_player_cache(name: str):
    return os.path.join(MusicPlayerStorage.PLAYER_CACHE_PATH, name + '.json')
