import gi

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk
from ArgsParser import ArgsParser
from MainWindow import MainWindow
from Config import ConfigBuilder

# TODO: class ServerInfo

args = ArgsParser().parse_args()
builder = ConfigBuilder()

builder.icon_path = "data/quake.png"
builder.font_path = "data/Xolonium-Bold.ttf"
builder.request_delay = args.request_delay or 60
builder.server_address = args.address
builder.server_name = args.name
builder.icon_title = args.icon_title
builder.filter_bots = args.filter_bots
builder.game_path = args.executable


window = MainWindow(builder.build())
window.move(1600, 800)
window.show()
Gtk.main()
