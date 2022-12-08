from gi.repository import Gtk, Gdk, GObject  # type: ignore
import re
from typing import Callable


def connect(obj: GObject.Object, event: str, listener: Callable, *args):
    obj.connect(event, lambda *_: listener(*args))


def connect_after(obj: GObject.Object, event: str, listener: Callable, *args):
    obj.connect_after(event, lambda *_: listener(*args))


def load_global_css(path: str, **variables):
    with open(path, "r") as f:
        css = f.read()

    def repl(match: re.Match) -> str:
        found = match.group(0)

        if v := variables.get(found[1:]):
            return str(v)

        raise ValueError(f"value for css variable {found} not set")

    css = re.sub(r"\$[\d\w]+", repl, css)

    css_provider = Gtk.CssProvider()
    css_provider.load_from_data(bytes(css, "utf8"))  # type: ignore

    screen = Gdk.Screen.get_default()
    if screen is not None:
        Gtk.StyleContext.add_provider_for_screen(screen, css_provider,
                                                 Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
    else:
        raise Exception("screen is None")


def add_css_classes(widget: Gtk.Widget, *css_classes: str):
    style_context = widget.get_style_context()

    for v in css_classes:
        style_context.add_class(v)
