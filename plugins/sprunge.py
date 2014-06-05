import requests

import smartbot
from smartbot import utils
from smartbot.exceptions import *


class Plugin(smartbot.Plugin):
    names = ["sprunge"]

    def on_command(self, msg, stdin, stdout, reply):
        contents = stdin.read().strip()
        if contents:
            print(utils.web.sprunge(contents), file=stdout)
        else:
            raise StopCommand("Expected input on stdin.")
