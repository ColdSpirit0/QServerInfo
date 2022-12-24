import re

from .TextParserAbstract import TextParserAbstract


class QuakeTextParser(TextParserAbstract):
    color_codes = {
        "1": "#F00",
        "2": "#0F0",
        "3": "#FF0",
        "4": "#00F",
        "5": "#0FF",
        "6": "#F0F",
        "7": "#FFF",
        "8": "#fa0",
        "9": "#888",
        "0": "#000",
    }

    @classmethod
    def parse_text(cls, text: str):
        colors_pattern = r"\^\d|\^x[0-9a-fA-F]{3}"
        regex = re.compile(rf"({colors_pattern})?(.*?)(?={colors_pattern}|$)")

        result = []

        for match in regex.finditer(text):
            color_text = match.group(1)
            plain_text = match.group(2)

            if plain_text == "":
                continue

            if color_text is None:
                # set it white
                color_text = "^7"

            result.append((cls.get_color(color_text), plain_text))

        return result

    @classmethod
    def get_color(cls, color_text: str):
        color_number = color_text[1]
        return cls.color_codes[color_number]

