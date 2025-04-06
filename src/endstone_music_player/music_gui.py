from endstone import Player, ColorFormat
from endstone.form import ActionForm, Dropdown, Label, MessageForm, ModalForm, Slider, StepSlider, TextInput, Toggle

from endstone_music_player import MusicPlugin
from endstone_music_player.music_player import MusicPlayer
from endstone_music_player.songs.song import Song


class MusicGui:
    def __init__(self, plugin: MusicPlugin, player: Player, music: MusicPlayer):
        self.plugin = plugin
        self.player = player
        self.music = music

    def main(self):
        form = ActionForm(f"{ColorFormat.BOLD + ColorFormat.GOLD}Music Player")
        if not self.music.playing:
            form.content = "'Sounds' Good with Endstone!"
        else:
            form.content = ColorFormat.BOLD + "> " + ColorFormat.YELLOW
            form.content += self.music.song.get_readable_name() + ColorFormat.RESET + "\n"
            bar_size = 100
            progress = int(bar_size * (self.music.tick / self.music.song.to_nbs().header.song_length))
            form.content += ColorFormat.DARK_GREEN + "|" * (progress - 1)
            form.content += ColorFormat.BOLD + ColorFormat.GREEN + "|" + ColorFormat.RESET
            form.content += ColorFormat.GRAY + "|" * (bar_size - progress)
        form.add_button("Control Panel", "textures/ui/creator_glyph_color", lambda _: self.control())
        form.add_button("Playlists", "textures/ui/icon_bookshelf", lambda _: self.list())
        form.add_button("Share with Friends", "textures/ui/icon_multiplayer", lambda _: self.share())
        self.player.send_form(form)

    def control(self):
        form = ModalForm(f"{ColorFormat.BOLD + ColorFormat.GOLD}Control Panel")
        form.on_close = lambda _: self.main()
        form.submit_button = "Apply"
        form.add_control(Label("Control Panel is not available yet."))
        form.add_control(Label("Use command instead plz!!!"))
        self.player.send_form(form)

    def list(self, page_num=1, page_size=8):
        songs = self.music.songs
        total_pages = len(songs) // page_size + (1 if len(songs) % page_size != 0 else 0)
        if page_num > total_pages: return self.list()
        if page_num < 1: return self.list(total_pages)
        start_index = (page_num - 1) * page_size
        end_index = min(start_index + page_size, len(songs))
        songs = songs[start_index:end_index]
        form = ActionForm(f"{ColorFormat.BOLD + ColorFormat.GOLD}Playlists")
        form.on_close = lambda _: self.main()
        form.content = f"({page_num} / {total_pages})"
        form.add_button(ColorFormat.DARK_GREEN + "Explore & Add", "textures/ui/worldsIcon", lambda _: self.explore())
        form.add_button(ColorFormat.DARK_AQUA + "<<<<< Previous", "textures/ui/switch_dpad_left", lambda _: self.list(page_num - 1))
        for song in songs:
            text = song.get_readable_name()
            on_click = lambda _, s=song: self.song(s, lambda: self.list(page_num))
            if song == self.music.song: form.add_button(ColorFormat.BOLD + text, "textures/ui/icon_saleribbon", on_click)
            else: form.add_button(text, "textures/ui/item_seperator", on_click)
        form.add_button(ColorFormat.DARK_AQUA + "Next >>>>>", "textures/ui/switch_dpad_right", lambda _: self.list(page_num + 1))
        self.player.send_form(form)

    def song(self, song: Song, back=None):
        form = ActionForm(f"{ColorFormat.BOLD + ColorFormat.GOLD}Song")
        form.on_close = lambda _: (back or (lambda : self.main()))()
        form.content = song.get_readable_name()
        def play_now():
            self.music.play(song)
            form.on_close(self.player)
        form.add_button("Play Now", on_click=lambda _: play_now())
        if song in self.music.songs:
            def remove():
                local_form = MessageForm(ColorFormat.BOLD + ColorFormat.RED + "Remove Song")
                local_form.content = f"Remove {song.get_readable_name()} ?"
                local_form.on_close = lambda _: self.song(song, back)
                local_form.button1 = "Yes"
                local_form.on_submit = lambda _, i: (self.music.songs.remove(song), form.on_close(self.player))\
                    if i == 0 else local_form.on_close(self.player)
                local_form.button2 = "No"
                self.player.send_form(local_form)
            form.add_button(ColorFormat.RED + "Remove", on_click=lambda _: remove())
        self.player.send_form(form)

    def explore(self):
        self.player.send_toast("Explore & Add", "Not available yet.")
        self.main()

    def share(self):
        self.player.send_toast("Share with Friends", "Not available yet.")
        self.main()
