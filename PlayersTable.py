from gi.repository import Gtk, Gdk

from colour import Color
from utils.color_processing import get_contrast_color

from text_parsers import TextParserAbstract
from server import PlayerData


class PlayersTable(Gtk.TreeView):
    def __init__(self, players: list[PlayerData], text_parser: type[TextParserAbstract]):
        super().__init__()

        # get default colors
        _, self.bg_color = self.get_style().lookup_color("bg_color")
        _, self.fg_color = self.get_style().lookup_color("fg_color")

        self.bg_color = Color(rgb=self.bg_color.to_floats())
        self.fg_color = Color(rgb=self.fg_color.to_floats())

        # setup columns
        renderer = Gtk.CellRendererText()

        for i, column_name in enumerate(["Ping", "Nickname", "Frags"]):
            column = Gtk.TreeViewColumn(column_name, renderer, markup=i)
            self.append_column(column)

            # custom header style
            # label = Gtk.Label(label=column_name)
            # label.show_all()
            # column.set_widget(label)
            # column.get_widget().override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 1, 0, 1))

        # create model
        self.players_model = Gtk.ListStore(int, str, int)
        self.set_model(self.players_model)

        # setup data
        self.update_data(players, text_parser)

    def update_data(self, players: list[PlayerData], text_parser: type[TextParserAbstract]):
        self.players_model.clear()

        # fill table
        for player in players:
            formatted_text_parts = []

            for color, text in text_parser.parse_text(player.name_raw):
                final_color = get_contrast_color(self.bg_color, Color(color), 0.15) if color is not None \
                              else self.fg_color

                formatted_text_parts.append(f"""<span color="{final_color.hex}">{text}</span>""")

            self.players_model.append([player.ping, "".join(formatted_text_parts), player.frags])
