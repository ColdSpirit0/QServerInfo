import argparse


class ArgsParser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        super().__init__(
            prog="ServerInfo",
            description="Shows in tray how many players on server",
            *args, **kwargs
        )

        self.add_argument("address", help="address to server with port in format [host]:[port]")
        self.add_argument("-n", "--name", help="server name, it will be shown in GUI")
