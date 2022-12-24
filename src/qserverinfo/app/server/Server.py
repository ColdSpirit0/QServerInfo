import logging
from pyq3serverlist import Server as QServer, PyQ3SLError, PyQ3SLTimeoutError

from .ServerText import ServerText
from .ServerData import ServerData


class Server():
    def __init__(self, address: str):
        host, port = address.split(":")
        self.server = QServer(host, int(port))

    def request_data(self) -> ServerData | None:
        logging.debug("Requesting data...")

        try:
            info = self.server.get_status()
            logging.debug(ServerText.decode_recursive(info))
            return ServerData(info)

        except (PyQ3SLError, PyQ3SLTimeoutError) as e:
            logging.warning(e)

            return None
