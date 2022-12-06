from abc import ABC, abstractmethod


class TextParserAbstract(ABC):
    @classmethod
    @abstractmethod
    def parse_text(cls, text) -> list:
        pass
