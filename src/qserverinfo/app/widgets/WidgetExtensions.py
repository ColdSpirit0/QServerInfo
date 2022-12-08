from gi.repository.Gtk import Widget  # type: ignore
from typing import Iterable, cast

from ..utils.gtk import add_css_classes


CLASSES_TYPE = Iterable[str] | str | None


class WidgetExtensions():
    def __init__(self, css_classes: CLASSES_TYPE = None, *args, **kwargs) -> None:
        self.widget_self = cast(Widget, self)
        super().__init__(*args, **kwargs)

        self.add_css_classes(css_classes)

    def add_css_classes(self, css_classes: Iterable[str] | str | None = None):
        if isinstance(css_classes, str):
            add_css_classes(self.widget_self, css_classes)
        elif css_classes is not None:
            add_css_classes(self.widget_self, *css_classes)
