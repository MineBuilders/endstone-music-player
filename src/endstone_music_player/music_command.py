from endstone.command import Command, CommandSender, CommandExecutor

from endstone_music_player import MusicPlugin


class MusicCommand(CommandExecutor):
    def __init__(self, plugin: MusicPlugin):
        super().__init__()
        self.plugin = plugin

    def on_command(self, sender: CommandSender, _: Command, args: list[str]) -> bool:
        return True

class MusicCommandPersonal(MusicCommand): pass

class MusicCommandGlobal(MusicCommand): pass
