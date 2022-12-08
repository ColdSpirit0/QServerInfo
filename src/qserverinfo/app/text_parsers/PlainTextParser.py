from .TextParserAbstract import TextParserAbstract


class PlainTextParser(TextParserAbstract):
    @classmethod
    def parse_text(cls, text: str):
        print("Plain formatting", text)
        return [(None, text)]
