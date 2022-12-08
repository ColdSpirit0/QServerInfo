from gi.repository import Gtk  # type: ignore
from typing import TypeVar

from .WidgetExtensions import WidgetExtensions

T = TypeVar("T", bound=Gtk.Widget)


class ExBox(WidgetExtensions, Gtk.Box):
    def pack_start(self, child: T, expand: bool = True, fill: bool = True, padding: int = 0) -> T:
        super().pack_start(child, expand, fill, padding)
        return child

    def pack_end(self, child: T, expand: bool = True, fill: bool = True, padding: int = 0) -> T:
        super().pack_end(child, expand, fill, padding)
        return child
