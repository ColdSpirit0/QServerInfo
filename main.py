import gi

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk
from ArgsParser import ArgsParser
from MainWindow import MainWindow

# TODO: class ServerInfo


def override_config(key, value):
    if value is not None:
        config[key] = value


# TODO: remove concrete data from project
config = {
    "icon_path": "data/quake.png",
    "font_path": "data/Xolonium-Bold.ttf",
    "request_delay": 10000,  # TODO: in seconds, min 30
    "server_address": None,
    "server_name": None,  # TODO: request from server itself if None
    "icon_title": None,
    "filter_bots": False,  # maybe TODO: filter by ping or by bots info
    "game_path": None,
}

args = ArgsParser().parse_args()
override_config("server_address", args.address)
override_config("server_name", args.name)
override_config("icon_title", args.icon_title)

window = MainWindow(**config)
window.move(1600, 800)
window.show()
Gtk.main()
