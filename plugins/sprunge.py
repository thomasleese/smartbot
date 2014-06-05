import requests

import smartbot
from smartbot import utils


class Plugin(smartbot.Plugin):
    names = ["sprunge"]

    def on_command(self, msg, stdin, stdout, reply):
        contents = stdin.read().strip()
        if contents:
            print(utils.web.sprunge(contents), file=stdout)
        else:
            print("Expected input on stdin.", file=stdout)

    def on_help(self):
        return "Usage: sprunge"
