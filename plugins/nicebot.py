import smartbot
from smartbot.formatting import *


class Plugin(smartbot.Plugin):
    """Authenticate with a NiceBot."""
    names = ["nicebot"]

    def __init__(self, nicebots):
        self.nicebots = nicebots

    def on_join(self, msg):
        for nicebot in self.nicebots:
            if nicebot["channel"] == msg["channel"] and msg["is_me"]:
                self.bot.send(nicebot["target"], nicebot["password"])

    def on_command(self, msg, stdin, stdout, reply):
        print(" ".join(nicebot["channel"] for nicebot in self.nicebots), file=stdout)

    def on_help(self):
        return self.bot.format("nicebot", Style.bold)
