from endstone_music_player.music_player import MusicPlayer
from endstone_music_player.music_storage import MusicPlayerStorage
from endstone_music_player.utils import singleton


@singleton
class MusicPlayerGlobal(MusicPlayer):
    def __init__(self, plugin):
        super().__init__(plugin)
        self.listeners = None
        self.copy(MusicPlayerStorage.read_raw(MusicPlayerStorage.GLOBAL_KEY))

    def play(self, song=None):
        self.listeners = self.plugin.server.online_players
        for player in MusicPlayerStorage.DATA_DICT.values():
            player.pause()
        super().play(song)
