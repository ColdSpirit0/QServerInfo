from gi.repository import Gtk  # type: ignore
from .utils.gtk import connect


class TrayMenu(Gtk.Menu):
    def __init__(self, window: Gtk.Window):
        super().__init__()

        self.add_item("Show window", window.show)
        self.add_item("Exit", Gtk.main_quit)

    def add_item(self, name, action):
        item = Gtk.MenuItem(label=name)
        connect(item, "activate", action)
        self.append(item)
        item.show()

    def show_at_pointer(self):
        self.popup_at_pointer()
