from gi.repository import Gtk  # type: ignore
from PIL import Image, ImageDraw, ImageFont
from .utils.image_manipulation import image2pixbuf, calc_font_size


class TrayIcon(Gtk.StatusIcon):
    def __init__(self, icon_path: str,
                       font_path: str,
                       startup_bottom_text: str,
                       top_text: str | None = None):

        super().__init__()
        self.font_path = font_path

        # use pil image instead of pixbuf
        # to draw text on it without converting from pixbuf
        img = Image.open(icon_path)
        self.background = img

        self.top_text = top_text
        self.set_bottom_text(startup_bottom_text)

    def set_bottom_text(self, bottom_text: str):
        img = self.background.copy()

        if self.top_text or bottom_text:
            stroke_width = max(1, img.width // 50)
            text_padding = stroke_width * 3
            text_container_size = (img.width, img.height // 2.5)
            draw = ImageDraw.Draw(img, "RGBA")

            if self.top_text:
                self.apply_text(draw, self.top_text, (img.width, text_padding),
                                 text_container_size, "rt", stroke_width)

            if bottom_text:
                self.apply_text(draw, bottom_text, (img.width, img.height - text_padding),
                                 text_container_size, "rs", stroke_width)

        # import os
        # os.system("pkill xviewer")
        # img.show()

        self.set_from_pixbuf(image2pixbuf(img))

    def apply_text(self, draw: ImageDraw.ImageDraw, text: str, pos: tuple,
                   text_container_size: tuple, anchor: str, stroke_width):

        font_size = calc_font_size(text, self.font_path, *text_container_size)
        font = ImageFont.truetype(self.font_path, font_size)

        draw.text(pos, text, font=font, fill="white", anchor=anchor,
                  stroke_width=stroke_width, stroke_fill="black",)
