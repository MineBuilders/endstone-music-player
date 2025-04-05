from abc import ABC, abstractmethod

from pynbs import File


class Song(ABC):
    @staticmethod
    def get_types():
        from endstone_music_player.songs.song_nbs import SongNbsFile
        return [
            SongNbsFile,
        ]

    @abstractmethod
    def to_nbs(self) -> File:
        pass

    @abstractmethod
    def encode(self) -> str:
        pass

    @staticmethod
    @abstractmethod
    def decode(data: str) -> "Song":
        pass
