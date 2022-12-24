import logging
from .TextParserAbstract import TextParserAbstract


class PlainTextParser(TextParserAbstract):
    @classmethod
    def parse_text(cls, text: str):
        logging.debug("Plain formatting", text)
        return [(None, text)]
