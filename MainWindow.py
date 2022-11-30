from gi.repository import Gtk, Gdk, GLib
from pyq3serverlist import Server, PyQ3SLError, PyQ3SLTimeoutError

from TrayMenu import TrayMenu
from TrayIcon import TrayIcon
from utils import connect


class MainWindow(Gtk.Window):
    def __init__(
        self,
        icon_path: str,
        font_path: str,
        server_address: str,
        server_name: str = None,
        request_delay: int = 30000,
        icon_title: str = None,
        **kwargs
    ):
        super().__init__(title="Server Info: " + (server_name or server_address))

        # save params
        self.server_address = server_address

        # configure window events
        self.connect("key_press_event", self.on_key)
        connect(self, "delete-event", self.on_delete)

        # setup tray and menu
        self.tray = TrayIcon(icon_path, font_path, "?", icon_title)
        self.menu = TrayMenu(self)

        # right on tray click open menu
        # left click on tray toggles window
        connect(self.tray, "popup-menu", self.menu.show_at_pointer)
        connect(self.tray, "activate", self.toggle_visibility)

        # setup window: widgets, size, pos etc
        self.setup_window()

        # start server requesting
        host, port = server_address.split(":")
        self.server = Server(host, int(port))
        self.request_server()
        GLib.timeout_add(request_delay, self.request_server)

    def request_server(self):
        print("requesting")

        try:
            info = self.server.get_status()
            print(info)
            text = str(len(info["players"]))
            # text = info["clients"]
        except (PyQ3SLError, PyQ3SLTimeoutError) as e:
            print(e)
            text = "X"

        self.tray.set_bottom_text(text)
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

    def setup_window(self):
        self.resize(500, 500)

        # create layout
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5, border_width=5)

        # create readonly address field
        hbox = Gtk.Box(spacing=5)
        hbox.pack_start(Gtk.Label("Address"), False, True, 0)
        hbox.pack_start(Gtk.Entry(text=self.server_address, editable=False), True, True, 0)

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
