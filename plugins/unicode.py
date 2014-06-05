import unicodedata

import requests

import smartbot


class Plugin(smartbot.Plugin):
    names = ["unicode", "???"]

    def on_command(self, msg, stdin, stdout, reply):
        query = " ".join(msg["args"][1:])
        if not query:
            query = stdin.read().strip()

        if query:
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
                print("Nothing found.", file=stdout)
        else:
            print(self.on_help(), file=stdout)

    def on_help(self):
        return "Usage: unicode <query>"
