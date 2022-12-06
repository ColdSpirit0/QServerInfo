from gi.repository import Gtk, GObject  # type: ignore
from typing import Callable


def connect(obj: GObject.Object, event: str, listener: Callable, *args):
    obj.connect(event, lambda *_: listener(*args))


def connect_after(obj: GObject.Object, event: str, listener: Callable, *args):
    obj.connect_after(event, lambda *_: listener(*args))


def setup_style(widget: Gtk.Widget, target_class: str, css_path: str):
    css_provider = Gtk.CssProvider()
    css_provider.load_from_path(css_path)

    style_context = widget.get_style_context()
    style_context.add_class(target_class)
    style_context.add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
