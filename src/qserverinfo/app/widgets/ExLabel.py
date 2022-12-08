from gi.repository import Gtk  # type: ignore

from .WidgetExtensions import WidgetExtensions


class ExLabel(WidgetExtensions, Gtk.Label):
    pass
