from gi.repository import Gtk
from PIL import Image as PImage, ImageDraw, ImageFont
from utils import image2pixbuf, calc_font_size


class TrayIcon(Gtk.StatusIcon):
    def __init__(self, icon_path, font_path=None, startup_text=None):
        super().__init__()
        self.font_path = font_path

        # use pil image instead of pixbuf
        # to draw text on it without converting from pixbuf
        img = PImage.open(icon_path)
        self.background = img

        self.set_text(startup_text)

    def set_text(self, text: str | None):
        img = self.background.copy()

        if text:
            # print("apply text:", text)

            stroke_width = max(1, img.width // 50)
            text_padding = stroke_width * 3

            text_container_size = (img.width, img.height // 2.5)

            font_size = calc_font_size(text, self.font_path, *text_container_size)
            font = ImageFont.truetype(self.font_path, font_size)

            draw = ImageDraw.Draw(img, "RGBA")
            draw.text(
                (img.width, img.height - text_padding),
                text,
                font=font,
                fill="white",
                anchor="rs",
                stroke_width=stroke_width,
                stroke_fill="black",
            )

            # import os
            # os.system("pkill xviewer")
            # img.show()

        self.set_from_pixbuf(image2pixbuf(img))
