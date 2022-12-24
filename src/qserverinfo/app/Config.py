from dataclasses import dataclass

# idk better way to freeze object and use pyright autocompletion & syntax check simultaneously


class Config():
    icon_path: str
    font_path: str
    styles_path: str
    request_delay: int
    server_address: str
    exit_on_esc: bool
    server_name: str | None = None
    icon_title: str | None = None
    filter_bots: bool | None = None
    game_path: str | None = None
    show_mapname: bool | None = None


@dataclass(frozen=True)
class FrozenConfig(Config):
    icon_path: str
    font_path: str
    styles_path: str
    request_delay: int
    server_address: str
    exit_on_esc: bool
    server_name: str | None = None
    icon_title: str | None = None
    filter_bots: bool | None = None
    game_path: str | None = None
    show_mapname: bool | None = None


class ConfigBuilder(Config):
    overrides = {}

    def __setattr__(self, name, value):
        if value is not None:
            self.overrides[name] = value

    def build(self):
        return FrozenConfig(**self.overrides)
