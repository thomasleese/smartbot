import hashlib

import smartbot.plugin
from smartbot.exceptions import StopCommandWithHelp
from smartbot.formatting import Style


class Plugin(smartbot.plugin.Plugin):
    """Perform a hash of a string."""
    names = ["hash"]

    def on_command(self, msg, stdin, stdout, reply):
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
