from gi.repository import Gtk, Gdk, GLib

from TrayMenu import TrayMenu
from TrayIcon import TrayIcon
from Server import Server
from Config import Config
from utils import connect


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
        self.setup_window()

        # start server requesting
        self.server = Server(config.server_address)
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

        # create join button
        # TODO: show only when path to game not null
        join_button = Gtk.Button(label="Join!")
        join_button.override_background_color(
            Gtk.StateFlags.NORMAL, Gdk.RGBA(0.7, 0.25, 0.2, 1)
        )
        vbox.pack_start(join_button, False, True, 0)

        vbox.show_all()
        self.add(vbox)
