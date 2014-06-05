import io

import requests
import lxml.etree

import smartbot
from smartbot import utils
from smartbot.exceptions import *
from smartbot.formatting import *


URL = "http://google.com/complete/search"


class Plugin(smartbot.Plugin):
    """Provide Google auto-complete suggestions."""
    names = ["complete", "autocomplete"]

    def on_command(self, msg, stdin, stdout, reply):
        query = " ".join(msg["args"][1:])
        if not query:
            query = stdin.read().strip()

        if query:
            payload = {"q": query, "output": "toolbar"}
            session = utils.web.requests_session()
            page = session.get(URL, params=payload)
            tree = lxml.etree.fromstring(page.text)

            suggestions = []
            for suggestion in tree.xpath("//suggestion"):
                suggestions.append(suggestion.get("data"))

            if suggestions:
                print(", ".join(suggestions[:5]), file=stdout)
            else:
                raise StopCommand("No suggestions.")
        else:
            raise StopCommandWithHelp(self)

    def on_help(self):
        return "{}|{} {}".format(
            self.bot.format("complete", Style.bold),
            self.bot.format("autocomplete", Style.bold),
            self.bot.format("query", Style.underline)
        )
