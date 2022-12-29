import gi
import os

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk  # type: ignore
from .ArgsParser import ArgsParser
from .MainWindow import MainWindow
from .Config import ConfigBuilder

# TODO: class ServerInfo


APP_PATH = os.path.dirname(__file__)


def main():
    args = ArgsParser().parse_args()
    builder = ConfigBuilder()

    builder.icon_path = f"{APP_PATH}/data/quake.png"
    builder.font_path = f"{APP_PATH}/data/Xolonium-Bold.ttf"
    builder.styles_path = f"{APP_PATH}/styles/main.css"
    builder.request_delay = args.request_delay or 60
    builder.server_address = args.address
    builder.server_name = args.name
    builder.icon_title = args.icon_title
    builder.filter_bots = args.filter_bots
    builder.game_path = args.executable
    builder.show_mapname = args.show_mapname
    builder.exit_on_esc = args.exit_on_esc

    window = MainWindow(builder.build())
    # TODO: move near tray pos or at least screen center
    # window.move(1600, 800)
    # window.show()
    Gtk.main()
