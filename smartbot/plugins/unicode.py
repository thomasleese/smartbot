import unicodedata

import requests

import smartbot
from smartbot.exceptions import *
from smartbot.formatting import *


class Plugin(smartbot.Plugin):
    """Get unicode information."""
    names = ["unicode", "???"]

    def on_command(self, msg, stdin, stdout, reply):
        query = " ".join(msg["args"][1:])
        if not query:
            query = stdin.read().strip()

        if not query:
            raise StopCommandWithHelp(self)

        try:
            c = unicodedata.lookup(query)
            result = "{} (U+{})".format(c, hex(ord(c))[2:])
        except KeyError:
            try:
                name = unicodedata.name(query)
                result = "{} (U+{})".format(name, hex(ord(query))[2:])
            except (ValueError, TypeError):
                result = None

        if result:
            print(result, file=stdout)
        else:
            raise StopCommand("Nothing found.")

    def on_help(self):
        return "{} {}".format(
            super().on_help(),
            self.bot.format("query", Style.underline)
        )
