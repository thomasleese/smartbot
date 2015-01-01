import random
import shlex

import smartbot.plugin
from smartbot.exceptions import StopCommandWithHelp
from smartbot.formatting import Style


class Plugin(smartbot.plugin.Plugin):
    """
    Save your brain for more important things by letting SmartBot make
    important decisions for you.
    """
    names = ["decide", "choose"]

    def on_command(self, msg, stdin, stdout, reply):
        args = msg["args"][1:]
        if not args:
            args = shlex.split(stdin.read().strip())

        if not args:
            raise StopCommandWithHelp(self)

        print(random.choice(args), file=stdout)

    def on_help(self):
        return "{}|{} {}…".format(
            self.bot.format("decide", Style.bold),
            self.bot.format("choose", Style.bold),
            self.bot.format("option", Style.underline)
        )
