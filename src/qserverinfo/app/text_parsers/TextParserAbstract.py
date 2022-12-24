from abc import ABC, abstractmethod


class TextParserAbstract(ABC):
    @classmethod
    @abstractmethod
    def parse_text(cls, text) -> list:
        pass

    @classmethod
    def decode_text(cls, text: str) -> str:
        return text.encode("raw_unicode_escape").decode("utf-8")
