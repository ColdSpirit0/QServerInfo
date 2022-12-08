from gi.repository import Gtk  # type: ignore
from ..Config import Config
from .import ExBox, ExLabel


class ServerDetailsWidget(ExBox):
    def __init__(self, config: Config, *args, **kwargs) -> None:
        super().__init__(orientation=Gtk.Orientation.VERTICAL, *args, **kwargs)

        self.config = config

        # create fields
        self.add_info_pair("Address", self.config.server_address)

        if self.config.show_mapname:
            self.mapname_label = self.add_info_pair("Map", "?")

    def set_mapname(self, mapname: str):
        self.mapname_label.set_label(mapname)

    def add_info_pair(self, name, value):
        hbox = ExBox()

        hbox.pack_start(ExLabel(label=name, css_classes="info-name"), False)
        label = hbox.pack_start(ExLabel(label=value, css_classes="info-value"))

        self.pack_start(hbox)
        return label
