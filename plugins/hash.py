import hashlib

from smartbot.exceptions import *
from smartbot.formatting import *


class Plugin:
    def on_command(self, bot, msg, stdin, stdout, reply):
        if len(msg["args"]) >= 2:
            algorithm = msg["args"][1]
            value = " ".join(msg["args"][2:])
            if not value:
                value = stdin.read().strip()

            try:
                h = hashlib.new(algorithm)
            except (ValueError, TypeError):
                raise StopCommandWithHelp(self)
            else:
                h.update(bytes(value, "utf-8"))
                print(h.hexdigest(), file=stdout)
        else:
            raise StopCommandWithHelp(self)

    def on_help(self):
        return "{} {} {}".format(
            self.bot.format("hash", Style.bold),
            self.bot.format("algorithm", Style.underline),
            self.bot.format("value", Style.underline)
        )
