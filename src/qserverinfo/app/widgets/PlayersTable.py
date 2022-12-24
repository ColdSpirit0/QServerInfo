from gi.repository import Gtk, Pango  # type: ignore
from colour import Color

from ..utils.gtk import connect
from ..utils.color_processing import get_contrast_color
from ..text_parsers import TextParserAbstract
from ..server import PlayerData


class PlayersTable(Gtk.TreeView):
    def __init__(self, players: list[PlayerData], text_parser: type[TextParserAbstract]):
        super().__init__()

        # setup columns
        renderer = Gtk.CellRendererText()
        renderer.set_properties(xalign=0.5)

        name_renderer = Gtk.CellRendererText()
        name_renderer.set_properties(xalign=0.5, weight=Pango.Weight.BOLD)

        default_params = {
                "alignment": 0.5,
                "min_width": 70,
        }

        for i, column_data in enumerate([
                    ("Ping", renderer, {}),
                    ("Nickname", name_renderer, {
                        "expand": True
                    }),
                    ("Frags", renderer, {}),
        ]):

            column_name, renderer, custom_params = column_data
            params = dict(default_params, **custom_params)

            column = Gtk.TreeViewColumn(column_name, renderer, markup=i)
            column.set_properties(**params)

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
        self.update_colors()
        self.set_data(players, text_parser)

        def init_signals():
            connect(self, "style-updated", self.on_style_updated)

        connect(self, "realize", init_signals)

    def set_data(self, players: list[PlayerData], text_parser: type[TextParserAbstract]):
        # cache data for redraw
        self.players = players
        self.text_parser = text_parser

        self.redraw_table()

    def redraw_table(self):
        # fill the table
        self.players_model.clear()

        for player in self.players:
            formatted_text_parts = []

            # TODO: cant see yellow color on white background
            for color, text in self.text_parser.parse_text(player.name_raw):
                final_color = get_contrast_color(self.bg_color, Color(color), 0.15) if color is not None \
                              else self.fg_color

                decoded_text = self.text_parser.decode_text(text)

                formatted_text_parts.append(f"""<span color="{final_color.hex}">{decoded_text}</span>""")

            self.players_model.append([player.ping, "".join(formatted_text_parts), player.frags])

    def on_style_updated(self):
        # when theme changed, need to get color and redraw nicknames to be contrast
        self.update_colors()
        self.redraw_table()

    def update_colors(self):
        # get default colors
        self.bg_color = self.get_theme_color(["theme_bg_color", "theme_base_color", "bg_color"], "#222")
        self.fg_color = self.get_theme_color(["theme_fg_color", "theme_text_color", "fg_color"], "#CCC")

    def get_theme_color(self, color_names: list[str], fallback_hex: str) -> Color:
        if not hasattr(self, "style"):
            self.style = self.get_style()

        for color_name in color_names:
            ok, gtk_color = self.style.lookup_color(color_name)

            if ok:
                return Color(rgb=gtk_color.to_floats())

        return Color(fallback_hex)
