import datetime
import re
import time

import smartbot
from smartbot import utils
from smartbot.exceptions import *
from smartbot.formatting import *


class Plugin(smartbot.Plugin):
    names = ["wait"]

    def on_command(self, msg, stdin, stdout, reply):
        if len(msg["args"]) >= 2:
            cmd = msg["args"][1]
            if cmd == "in" or cmd == "at":
                try:
                    date = utils.datetime.parse(" ".join(msg["args"][1:]))
                except ValueError:
                    raise smartbot.StopCommand("I don't understand that date.")
                else:
                    duration = (date - datetime.datetime.now()).total_seconds()
                    time.sleep(max(0, duration))
            else:
                raise StopCommand("‘{}’ is not a valid command.".format(cmd))
        else:
            raise StopCommandWithHelp(self)

    def on_help(self):
        return "{} in {}|at {}".format(
            super().on_help(),
            self.bot.format("time", Style.underline),
            self.bot.format("time", Style.underline)
        )
