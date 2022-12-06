from gi.repository import Gtk, Gdk, GLib
import subprocess

from TrayMenu import TrayMenu
from TrayIcon import TrayIcon
from PlayersTable import PlayersTable
from server import Server, DummyServer
from Config import Config
from utils.gtk import connect, setup_style

from text_parsers import PlainTextParser, XonoticTextParser


class MainWindow(Gtk.Window):
    def __init__(self, config: Config):
        super().__init__()
        self.update_title_info(config.server_name or config.server_address)

        self.config = config

        # configure window events
        self.connect("key_press_event", self.on_key)
        connect(self, "delete-event", self.on_delete)

        # setup tray and menu
        self.tray = TrayIcon(config.icon_path, config.font_path, "?", config.icon_title)
        self.menu = TrayMenu(self)

        # right on tray click open menu
        # left click on tray toggles window
        connect(self.tray, "popup-menu", self.menu.show_at_pointer)
        connect(self.tray, "activate", self.toggle_visibility)

        # setup window: widgets, size, pos etc
        setup_style(self, "main-window", "styles/main.css")
        self.setup_window()

        # start server requesting

        ChoosenServer = Server if config.server_address != "dummy" else DummyServer
        self.server = ChoosenServer(config.server_address)
        self.request_server()
        GLib.timeout_add(config.request_delay * 1000, self.request_server)

    def request_server(self):
        data = self.server.request_data()

        if data is not None:
            players_count = data.players_count

            if self.config.filter_bots:
                players_count -= data.bots_count

            if self.config.server_name is None:
                # set name what server provides
                self.update_title_info(data.hostname)

            self.players_table.update_data(data.players, self.get_parser(data.gamename))

            self.tray.set_bottom_text(str(players_count))

        else:
            self.tray.set_bottom_text("X")

        return True  # repeat

    def toggle_visibility(self):
        if self.is_visible():
            self.hide()
        else:
            self.show()

    def on_key(self, caller, key):
        if key.keyval == Gdk.KEY_Escape:
            Gtk.main_quit()

    def on_delete(self):
        self.hide()
        return True  # dont destroy object

    def update_title_info(self, info):
        self.set_title("Server Info: " + info)

    def setup_window(self):
        self.resize(500, 500)

        # create layout
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5, border_width=5)

        # create readonly address field
        hbox = Gtk.Box(spacing=5)
        hbox.pack_start(Gtk.Label("Address"), False, True, 0)
        hbox.pack_start(Gtk.Entry(text=self.config.server_address, editable=False), True, True, 0)

        vbox.pack_start(hbox, True, False, 0)

        self.players_table = PlayersTable([], self.get_parser(None))
        vbox.pack_start(self.players_table, True, True, 0)

        # create join button
        if self.config.game_path is not None:

            join_button = Gtk.Button(label="Join!")
            join_button.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0.7, 0.25, 0.2, 1))
            join_button.override_background_color(Gtk.StateFlags.ACTIVE, Gdk.RGBA(0.8, 0.35, 0.2, 1))
            vbox.pack_start(join_button, False, True, 0)

            connect(join_button, "clicked", self.start_game)

        vbox.show_all()
        self.add(vbox)

    def start_game(self):
        if self.config.game_path is None:
            raise Exception("game path is none, that should not happen")

        print("running", self.config.game_path)
        self.hide()

        subprocess.Popen([self.config.game_path, "+connect", self.config.server_address],
                         start_new_session=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    @staticmethod
    def get_parser(game_name: str | None):
        match game_name:
            case "Xonotic": return XonoticTextParser
            case _: return PlainTextParser
