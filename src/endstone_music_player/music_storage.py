import json
from dataclasses import dataclass, field

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
