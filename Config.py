from dataclasses import dataclass


@dataclass(frozen=True)
class Config():
    icon_path: str = None
    font_path: str = None
    request_delay: int = None
    server_address: str = None
    server_name: str = None
    icon_title: str = None
    filter_bots: bool = None
    game_path: str = None


class ConfigBuilder(Config):
    overrides = {}

    def __setattr__(self, name, value):
        if value is not None:
            self.overrides[name] = value

    def build(self):
        return Config(**self.overrides)
