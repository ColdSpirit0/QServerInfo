import logging
from .Server import Server
from .ServerData import ServerData


class DummyServer(Server):
    def __init__(self, *args, **kwargs):
        _ = args, kwargs  # fix pyright 'args not acessed' warning
        pass

    def request_data(self) -> ServerData:
        logging.debug("Requesting dummy data...")
        info = {
            "ip": "best.dummy.server.ever",
            "port": 777,
            "gamename": "Xonotic",
            'bots': '1',
            # 'mapname': 'nexdance',
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
                    'ping': 99999,
                    'colored_name': 'TEST NICKNAME',
                },
                {
                    'frags': 30,
                    'ping': -888,
                    'colored_name': '▮▮▮▮▮',
                },
            ]
        }

        return ServerData(info)
