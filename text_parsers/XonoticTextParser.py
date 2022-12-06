import re

from .TextParserAbstract import TextParserAbstract


class XonoticTextParser(TextParserAbstract):
    """ Parses colors with rules (from xonotic documentation):

        Code  | Result                       | Note
        ^1    | #F00 Red                     |
        ^2    | #0F0 Green                   |
        ^3    | #FF0 Yellow                  |
        ^4    | #00F Blue                    |
        ^5    | #0FF Cyan                    |
        ^6    | #F0F Magenta                 |
        ^7    | #FFF White                   |
        ^8    | #FFF8 Half transparent white | Alpha will be ignored
        ^9    | #888 Light Gray              |   
        ^0    | #000 Black                   |
        ^xRGB | #RGB Custom color            |
    """

    color_codes = {
        "1": "#F00",
        "2": "#0F0",
        "3": "#FF0",
        "4": "#00F",
        "5": "#0FF",
        "6": "#F0F",
        "7": "#FFF",
        "8": "#FFF",
        "9": "#888",
        "0": "#000",
    }

    @classmethod
    def parse_text(cls, text: str):
        colors_pattern = r"\^\d|\^x[0-9a-fA-F]{3}"
        regex = re.compile(rf"({colors_pattern})(.*?)(?={colors_pattern}|$)")

        # res = regex.sub(cls.format_match, text)

        result = []

        for match in regex.finditer(text):
            color_text = match.group(1)
            plain_text = match.group(2)

            if plain_text == "":
                continue

            result.append((cls.get_color(color_text), plain_text))

        return result

    @ classmethod
    def get_color(cls, color_text: str):
        match color_text[1]:
            case "x":
                return "#" + color_text[2:]
            case color_number:
                return cls.color_codes[color_number]
