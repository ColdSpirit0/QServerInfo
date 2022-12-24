from gi.repository import Gtk, Gdk, GLib  # type: ignore
import logging
import subprocess

from .TrayMenu import TrayMenu
from .TrayIcon import TrayIcon
from .server import Server, DummyServer
from .Config import Config
from .utils.gtk import connect, load_global_css, add_css_classes

from .text_parsers import PlainTextParser, XonoticTextParser, QuakeTextParser
from .widgets import ExLabel, ExBox, PlayersTable, ServerDetailsWidget


class MainWindow(Gtk.Window):
    def __init__(self, config: Config):
        super().__init__()
        self.update_title_info(config.server_name or config.server_address)

        self.config = config

        # configure window events
        if config.exit_on_esc:
            def on_key(_, key):
                if key.keyval == Gdk.KEY_Escape:
                    Gtk.main_quit()

            self.connect("key_press_event", on_key)

        connect(self, "delete-event", self.on_delete)

        # setup tray and menu
        self.tray = TrayIcon(config.icon_path, config.font_path, "?", config.icon_title)
        self.menu = TrayMenu(self)

        # right on tray click open menu
        # left click on tray toggles window
        connect(self.tray, "popup-menu", self.menu.show_at_pointer)
        connect(self.tray, "activate", self.toggle_visibility)

        # setup window: widgets, size, pos etc
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

            if self.config.show_mapname:
                logging.debug(f"set mapname: {data.mapname}")
                self.server_details.set_mapname(data.mapname or "No info")

            self.players_table.set_data(data.players, self.get_parser(data.gamename))

            self.tray.set_bottom_text(str(players_count))

        else:
            self.tray.set_bottom_text("X")

        return True  # repeat

    def toggle_visibility(self):
        if self.is_visible():
            self.hide()
        else:
            self.show()

    def on_delete(self):
        self.hide()
        return True  # dont destroy object

    def update_title_info(self, info):
        self.set_title("Server Info: " + info)

    def setup_window(self):
        def create_title_label(text: str) -> ExLabel:
            title = ExLabel(label=text, css_classes="title-label")
            return title

        self.resize(500, 500)

        load_global_css(self.config.styles_path)
        add_css_classes(self, "main-window")

        # create layout
        vbox = ExBox(orientation=Gtk.Orientation.VERTICAL, margin=5, spacing=5, border_width=5)  # type: ignore

        # server info
        vbox.pack_start(create_title_label("Server information"), False, True, 0)
        self.server_details = vbox.pack_start(ServerDetailsWidget(self.config), False)

        # players table
        vbox.pack_start(create_title_label("Players"), False, True, 0)
        self.players_table = vbox.pack_start(PlayersTable([], self.get_parser(None)), True, True, 0)

        # create join button
        if self.config.game_path is not None:
            join_button = vbox.pack_start(Gtk.Button(label="Join!"), False, True, 0)
            add_css_classes(join_button, "join-button")

            connect(join_button, "clicked", self.start_game)

        vbox.show_all()
        self.add(vbox)

    def start_game(self):
        if self.config.game_path is None:
            raise Exception("game path is none, that should not happen")

        logging.debug("running", self.config.game_path)
        self.hide()

        subprocess.Popen([self.config.game_path, "+connect", self.config.server_address],
                         start_new_session=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    @staticmethod
    def get_parser(game_name: str | None):
        match game_name:
            case "Xonotic": return XonoticTextParser
            case "baseoa": return QuakeTextParser  # openarena
            case "Warsow": return QuakeTextParser
            case _: return PlainTextParser
