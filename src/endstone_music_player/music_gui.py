from endstone import Player

from endstone_music_player import MusicPlugin
from endstone_music_player.music_player import MusicPlayer


class MusicGui:
    def __init__(self, plugin: MusicPlugin, player: Player, music: MusicPlayer):
        self.plugin = plugin
        self.player = player
        self.music = music

    def main(self):
        self.player.send_error_message("GUI is not available yet!")
