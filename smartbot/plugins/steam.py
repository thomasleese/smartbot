import lxml.html
import requests

import smartbot.plugin
from smartbot.utils.web import get_title
from smartbot.exceptions import StopCommand, StopCommandWithHelp


class Plugin(smartbot.plugin.Plugin):
    """Display the steam daily deal."""
    names = ["steam"]

    def on_command(self, msg, stdin, stdout, reply):
        if len(msg["args"]) >= 2:
            action = msg["args"][1]
            if "deal".startswith(action):
                page = requests.get("http://store.steampowered.com")
                tree = lxml.html.fromstring(page.text)
                if tree.cssselect(".dailydeal"):
                    url = tree.cssselect(".dailydeal a")[0].get("href")
                    original_price = tree.cssselect(".dailydeal_content .discount_original_price")[0].text
                    final_price = tree.cssselect(".dailydeal_content .discount_final_price")[0].text
                    print("{0} - {1} - from {2} to {3}".format(url,
                                                               get_title(url),
                                                               original_price,
                                                               final_price), file=stdout)
                else:
                    raise StopCommand("No daily deal.")
            else:
                raise StopCommand("{} is not a valid action.".format(action))
        else:
            raise StopCommandWithHelp(self)

    def on_help(self):
        return "{} deal".format(
            super().on_help()
        )
