from pyq3serverlist import Server as QServer, PyQ3SLError, PyQ3SLTimeoutError


class ServerData():
    def __init__(self, data: dict):
        self.data = data

    @property
    def players(self) -> dict:
        return self.data["players"]  # players should be!

    @property
    def players_count(self) -> int:
        return len(self.players)

    @property
    def bots_count(self) -> int:
        # try to get "bots" value
        bots_count = self.data.get("bots")
        if bots_count is not None:
            return int(bots_count)

        # count players where ping 0 or less
        bots_count = 0
        for p in self.players:
            if p.get("ping", 1) <= 0:
                bots_count += 1

        return bots_count


class Server():
    def __init__(self, address: str):
        host, port = address.split(":")
        self.server = QServer(host, int(port))

    def request_data(self) -> ServerData:
        print("Requesting data...")

        try:
            info = self.server.get_status()

            # print server info
            for k, v in info.items():
                print(f"\t{k}: \"{v}\"")

            return ServerData(info)

        except (PyQ3SLError, PyQ3SLTimeoutError) as e:
            print(e)

            return None
