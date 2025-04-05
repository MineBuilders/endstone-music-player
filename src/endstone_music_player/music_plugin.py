from endstone.plugin import Plugin


class MusicPlugin(Plugin):
    prefix = "MusicPlayer"
    api_version = "0.5"
    load = "POSTWORLD"

    commands = {
        "music-player": {
            "description": "'Sounds' Good with Endstone!",
            "usages": [
                "/music-player",
                "/music-player play [path:message]",
                "/music-player <add|remove> <path:message>",
                "/music-player <list|next|pause|reset>",
            ],
            "aliases": ["songs", "mp"],
            "permissions": ["music_player.command.music_player"],
        },
        "music-player-global": {
            "description": "Play music for everyone!",
            "usages": [
                "/music-player-global",
                "/music-player-global play [path:message]",
                "/music-player-global <list|next|reset|pause>",
            ],
            "aliases": ["songs-g", "mpg"],
            "permissions": ["music_player.command.music_player_global"],
        }
    }

    permissions = {
        "music_player.command.music_player": {
            "description": "Allow users to use the /music-player command.",
            "default": True,
        },
        "music_player.command.music_player_global": {
            "description": "Allow users to use the /music-player-global command.",
            "default": "op",
        },
    }

    def on_load(self) -> None:
        return

    def on_enable(self) -> None:
        from endstone_music_player.music_command import MusicCommandPersonal, MusicCommandGlobal
        self.get_command("music-player").executor = MusicCommandPersonal(self)
        self.get_command("music-player-global").executor = MusicCommandGlobal(self)

    def on_disable(self) -> None:
        from endstone_music_player.music_storage import MusicPlayerStorage
        MusicPlayerStorage.save(self)
        return
