import lxml.html
import requests

import smartbot
from smartbot import utils


class Plugin(smartbot.Plugin):
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
                                                               utils.web.get_title(url),
                                                               original_price,
                                                               final_price), file=stdout)
                else:
                    print("No daily deal.", file=stdout)
            else:
                print("No such action:", action, file=stdout)
        else:
            print(self.on_help(), file=stdout)

    def on_help(self):
        return "Usage: steam deal"
