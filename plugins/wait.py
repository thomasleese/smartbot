import datetime
import re
import time
import unittest

from smartbot import HelpException, StopCommandException, utils


class Plugin:
    def on_command(self, bot, msg, stdin, stdout, reply):
        if len(msg["args"]) >= 2:
            cmd = msg["args"][1]
            if cmd == "in" or cmd == "at":
                try:
                    date = utils.datetime.parse(" ".join(msg["args"][1:]))
                except ValueError:
                    raise StopCommandException("I don't understand that date.")
                else:
                    duration = max(0, (date - datetime.datetime.now()).total_seconds())
                    time.sleep(duration)
        else:
            raise HelpException(self)

    def on_help(self):
        return "Usage: wait in <time>|at <time>"
