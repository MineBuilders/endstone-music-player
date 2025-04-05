from endstone_music_player.music_player import MusicPlayer
from endstone_music_player.utils import singleton


@singleton
class MusicPlayerGlobal(MusicPlayer):
    def __init__(self, server):
        super().__init__(server)
        self.listeners = None

    def play(self, song = None):
        self.listeners = self.plugin.server.online_players
        super().play(song)
