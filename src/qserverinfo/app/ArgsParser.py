import argparse


def request_delay_type(value: str) -> int:
    number = int(value)
    if number < 30:
        raise argparse.ArgumentTypeError(f"Given request delay \"{number}\" is less than 30, this is too often!")
    else:
        return number


class ArgsParser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        super().__init__(
            prog="ServerInfo",
            description="Shows in tray how many players on server",
            *args, **kwargs
        )

        self.add_argument("address", help="address to server with port in format [host]:[port]")

        self.add_argument("-n", "--name", help="server name, it will be shown in GUI")

        self.add_argument("-it", "--icon-title", help="text on top of icon")

        self.add_argument("-rd", "--request-delay",
                          help="how often server will be requested; in seconds, minimum 30, default 60",
                          type=request_delay_type)

        self.add_argument("-fb", "--filter-bots", help="remove bots from players count if possible",
                          action="store_true")

        self.add_argument("-e", "--executable",
                          help="path to game executable which will start after"
                          " \"Join\" button click with parameter \"+connect <address>\"")

        self.add_argument("-m", "--show-mapname", help="display mapname in the window if possible",
                          action="store_true")

        # debug
        self.add_argument("--exit-on-esc", help=argparse.SUPPRESS, action="store_true")
