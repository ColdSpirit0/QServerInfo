import sys
import os
import logging

sys.path.insert(0, os.path.join(".", "src"))

from qserverinfo.app.main import main

logging.basicConfig(level=logging.DEBUG)

main()
