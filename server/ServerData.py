from functools import cached_property

from .ServerText import ServerText
from .PlayerData import PlayerData


class ServerData():
    def __init__(self, data: dict):
        self.data = data

    @cached_property
    def players(self) -> list[PlayerData]:

        players = []
        for player in self.data["players"]:
            data = PlayerData(
                player["ping"],
                player["frags"],
                player["colored_name"],
            )
            players.append(data)

        return players

    @cached_property
    def players_count(self) -> int:
        return len(self.players)

    @cached_property
    def bots_count(self) -> int:
        # try to get "bots" value
        bots_count = self.data.get("bots")
        if bots_count is not None:
            return int(bots_count)

        # count players where ping 0 or less
        bots_count = 0
        for player in self.players:
            if player.ping <= 0:
                bots_count += 1

        return bots_count

    @cached_property
    def hostname(self) -> str:
        return ServerText.decode_text(self.data.get("hostname") or self.data.get("sv_hostname"))

    @cached_property
    def gamename(self) -> str:
        name = self.data.get("gamename")
        assert isinstance(name, str)
        return name

    @cached_property
    def mapname(self) -> str | None:
        mapname = self.data.get("mapname")
        return mapname
