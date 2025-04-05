import pynbs

from endstone_music_player.songs.song import Song


class SongNbsFile(Song):
    def __init__(self, path: str):
        self.path = path
        self.nbs = pynbs.read(path)

    def to_nbs(self):
        return self.nbs

    def encode(self):
        return self.path

    @staticmethod
    def decode(data: str):
        return SongNbsFile(data)
