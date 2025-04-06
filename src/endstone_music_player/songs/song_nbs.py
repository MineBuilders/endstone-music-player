import os
from pathlib import Path

import pynbs

from endstone_music_player.music_storage import resolve_songs
from endstone_music_player.songs.song import Song


class SongNbsFile(Song):
    def __init__(self, path: str):
        self.path = path
        self.nbs = pynbs.read(path)

    def get_readable_name(self):
        header_name = self.nbs.header.song_name
        if not header_name.strip():
            return Path(self.path).stem
        else:
            return header_name

    @staticmethod
    def load_from_command(arg):
        path = Path(resolve_songs(arg + '.nbs'))
        if path.is_file(): return SongNbsFile(str(path))
        name = (arg + '.nbs').lower()
        for root, _dirs, files in os.walk(path):
            for file in files:
                if file.lower() == name:
                    return SongNbsFile(os.path.join(root, file))
        return None

    def to_nbs(self):
        return self.nbs

    def encode(self):
        return self.path

    @staticmethod
    def decode(data):
        return SongNbsFile(data)
