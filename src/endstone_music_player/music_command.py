from endstone import Player
from endstone.command import Command, CommandSender, CommandExecutor

from endstone_music_player import MusicPlugin
from endstone_music_player.music_gui import MusicGui
from endstone_music_player.music_player import MusicPlayer, PlayOrder
from endstone_music_player.music_player_global import MusicPlayerGlobal
from endstone_music_player.music_storage import MusicPlayerStorage
from endstone_music_player.songs.song import Song


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
                song = resolve_song(path)
                if path is None: music.play()
                elif song is None: sender.send_error_message("Could not resolve this song!")
                else: music.play(song)
            case ["add", path]:
                song = resolve_song(path)
                if song is None: sender.send_error_message("Could not resolve this song!")
                else:
                    music.songs.append(song)
                    sender.send_message(f"{song.get_readable_name()} added to the playlist!")
            case ["remove", index]:
                del music.songs[int(index)]
            case ["order", order]:
                match order:
                    case "sequence": music.order = PlayOrder.SEQUENCE
                    case "random": music.order = PlayOrder.RANDOM
                    case "repeat_one": music.order = PlayOrder.REPEAT_ONE
                    case "repeat_list": music.order = PlayOrder.REPEAT_LIST
                sender.send_message(f"Switch to {music.order.name}.")
            case ["list"]:
                for index, song in enumerate(music.songs):
                    sender.send_message(f"{index}: {song.get_readable_name()}")
            case ["next"]: music.next()
            case ["pause"]: music.pause()
            case ["reset"]: music.reset()
        return True


def resolve_song(arg: str):
    if arg is None: return None
    for clazz in Song.get_types():
        song = clazz.load_from_command(arg)
        if song is not None: return song
    return None


class MusicCommandPersonal(MusicCommand):
    def get_music(self, sender):
        return MusicPlayerStorage.get(self.plugin, sender)


class MusicCommandGlobal(MusicCommand):
    def get_music(self, sender):
        return MusicPlayerGlobal(self.plugin)
