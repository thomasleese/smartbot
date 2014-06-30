import datetime

import smartbot
from smartbot.exceptions import *
from smartbot.formatting import *


class Plugin(smartbot.Plugin):
    """Check last time someone was seen."""
    names = ["seen"]

    def on_message(self, msg, reply):
        self.bot.storage["seen." + msg["sender"]] = {
            "action": "spoke",
            "datetime": datetime.datetime.now()
        }

    def on_command(self, msg, stdin, stdout, reply):
        if len(msg["args"]) >= 2:
            user = msg["args"][1]
            try:
                info = self.bot.storage["seen." + user]
                datetime_str = info["datetime"].strftime("%a %d %b %H:%M %Z").strip()
                print("{0} {1} on {2}.".format(user, info["action"], datetime_str), file=stdout)
            except KeyError:
                raise StopCommand("I don't know anything about {0}.".format(user))
        else:
            raise StopCommandWithHelp(self)

    def on_help(self):
        return "{} {}".format(
            super().on_help(),
            self.bot.format("user", Style.underline)
        )
