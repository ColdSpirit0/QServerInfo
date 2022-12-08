from dataclasses import dataclass


@dataclass(frozen=True)
class PlayerData():
    ping: int
    frags: int
    name_raw: str
