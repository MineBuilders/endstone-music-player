from endstone import Player
from endstone.command import Command, CommandSender, CommandExecutor

from endstone_music_player import MusicPlugin
from endstone_music_player.music_gui import MusicGui
from endstone_music_player.music_player import MusicPlayer, PlayOrder
from endstone_music_player.music_player_global import MusicPlayerGlobal
from endstone_music_player.music_storage import MusicPlayerStorage
from endstone_music_player.songs.song_nbs import SongNbsFile


class MusicCommand(CommandExecutor):
    def __init__(self, plugin: MusicPlugin):
        super().__init__()
        self.plugin = plugin

    def get_music(self, sender: CommandSender) -> MusicPlayer:
        raise NotImplementedError

    def on_command(self, sender: CommandSender, _: Command, args: list[str]) -> bool:
        music = self.get_music(sender)
        if len(args) == 0:
            if isinstance(sender, Player): return MusicGui(self.plugin, sender, music).main()
            else: return False
        match args:
            case ["play", *rest]:
                path = next(iter(rest), None)
                if path is not None: music.play(SongNbsFile(path))
                else: music.play()
            case ["add", path]:
                music.songs.append(SongNbsFile(path))
            case ["remove", index]:
                del music.songs[int(index)]
            case ["order", order]:
                match order:
                    case "sequence": music.order = PlayOrder.SEQUENCE
                    case "random": music.order = PlayOrder.RANDOM
                    case "repeat_one": music.order = PlayOrder.REPEAT_ONE
                    case "repeat_list": music.order = PlayOrder.REPEAT_LIST
            case ["list"]:
                for index, song in enumerate(music.songs):
                    sender.send_message(f"{index}: {song.encode()}")
            case ["next"]: music.next()
            case ["pause"]: music.pause()
            case ["reset"]: music.reset()
        return True

class MusicCommandPersonal(MusicCommand):
    def get_music(self, sender):
        return MusicPlayerStorage.get(self.plugin, sender)

class MusicCommandGlobal(MusicCommand):
    def get_music(self, sender):
        return MusicPlayerGlobal(self.plugin)
