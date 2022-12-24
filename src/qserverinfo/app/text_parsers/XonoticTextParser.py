from .QuakeTextParser import QuakeTextParser


class XonoticTextParser(QuakeTextParser):
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

    # table copied from https://github.com/TheRegulars/website/blob/master/src/dptext.ts
    # MIT license
    qfont_unicode_table = [
        " ", " ", "\u2014", " ", "_", "\u2747", "\u2020",
        "\u00b7", "\ud83d\udd2b", " ", " ", "\u25a0",
        "\u2022", "\u2192", "\u2748", "\u2748", "[", "]",
        "\ud83d\udc7d", "\ud83d\ude03", "\ud83d\ude1e",
        "\ud83d\ude35", "\ud83d\ude15", "\ud83d\ude0a",
        "\u00ab", "\u00bb", "\u2022", "\u203e", "\u2748",
        "\u25ac", "\u25ac", "\u25ac", " ", "!", "\"", "#",
        "$", "%", "&", "'", "(", ")", "\u00d7", "+", ",",
        "-", ".", "/", "0", "1", "2", "3", "4", "5", "6",
        "7", "8", "9", ":", ";", "<", "=", ">", "?", "@",
        "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
        "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
        "U", "V", "W", "X", "Y", "Z", "[", "\\", "]", "^",
        "_", "'", "a", "b", "c", "d", "e", "f", "g", "h",
        "i", "j", "k", "l", "m", "n", "o", "p", "q", "r",
        "s", "t", "u", "v", "w", "x", "y", "z", "{", "|",
        "}", "~", "\u2190", "<", "=", ">", "\ud83d\ude80",
        "\u00a1", "O", "U", "I", "C", "\u00a9", "\u00ae",
        "\u25a0", "\u00bf", "\u25b6", "\u2748", "\u2748",
        "\u2772", "\u2773", "\ud83d\udc7d", "\ud83d\ude03",
        "\ud83d\ude1e", "\ud83d\ude35", "\ud83d\ude15",
        "\ud83d\ude0a", "\u00ab", "\u00bb", "\u2747", "x",
        "\u2748", "\u2014", "\u2014", "\u2014", " ", "!",
        "\"", "#", "$", "%", "&", "'", "(", ")", "*", "+",
        ",", "-", ".", "/", "0", "1", "2", "3", "4", "5",
        "6", "7", "8", "9", ":", ";", "<", "=", ">", "?",
        "@", "A", "B", "C", "D", "E", "F", "G", "H", "I",
        "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S",
        "T", "U", "V", "W", "X", "Y", "Z", "[", "\\", "]",
        "^", "_", "'", "A", "B", "C", "D", "E", "F", "G",
        "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q",
        "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "{",
        "|", "}", "~", "\u25c0"
    ]

    @classmethod
    def get_color(cls, color_text: str):
        if color_text[1] == "x":
            return "#" + color_text[2:]

        return super().get_color(color_text)

    @classmethod
    def decode_char(cls, char: str) -> str:
        charcode = ord(char)
        if 0xE000 <= charcode <= 0xF8FF:
            return cls.qfont_unicode_table[charcode - 0xE000]

        return char

    @classmethod
    def decode_text(cls, text: str) -> str:
        return ''.join(cls.decode_char(char)
                       for char in text.encode("raw_unicode_escape").decode())
