import datetime
import time

import smartbot.plugin
from smartbot.utils.datetime import parse as parse_datetime
from smartbot.exceptions import StopCommand, StopCommandWithHelp
from smartbot.formatting import Style


class Plugin(smartbot.plugin.Plugin):
    """Wait for an amount of time."""
    names = ["wait"]

    def on_command(self, msg, stdin, stdout, reply):
        if len(msg["args"]) >= 2:
            cmd = msg["args"][1]
            if cmd == "in" or cmd == "at":
                try:
                    date = parse_datetime(" ".join(msg["args"][1:]))
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
