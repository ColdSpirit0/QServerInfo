from .Server import Server
from .ServerData import ServerData


class DummyServer(Server):
    def __init__(self, *args, **kwargs):
        _ = args, kwargs  # fix pyright 'args not acessed' warning
        pass

    def request_data(self) -> ServerData:
        print("Requesting dummy data...")
        info = {
            "ip": "best.dummy.server.ever",
            "port": 777,
            "gamename": "Xonotic",
            'bots': '1',
            'mapname': 'nexdance',
            'hostname': '| DOOMY | SERVER |',
            'players': [
                {
                    'frags': 30,
                    'ping': 45,
                    'colored_name': '^xAA0Real^x300Player^7',
                },
                {
                    'frags': 30,
                    'ping': 0,
                    'colored_name': '^x055[BOT]^x770un^x0F0real',
                },
                {
                    'frags': 30,
                    'ping': 0,
                    'colored_name': '^1^2^3hello ^4^5game^6^7',
                },
                {
                    'frags': 30,
                    'ping': 0,
                    'colored_name': '^xEEFColdSpirit',
                },
                {
                    'frags': 30,
                    'ping': 0,
                    'colored_name': '^5ColdSpirit',
                },
            ]
        }

        # print(ServerText.decode_recursive(info))
        return ServerData(info)
