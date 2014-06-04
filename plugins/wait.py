import datetime
import re
import time
import unittest

from smartbot import utils
from smartbot.exceptions import *


class Plugin:
    def on_command(self, bot, msg, stdin, stdout, reply):
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
        return "Usage: wait in <time>|at <time>"
