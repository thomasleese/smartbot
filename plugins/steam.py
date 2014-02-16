import lxml.html
import requests

from smartbot import utils


class Plugin:
    def __call__(self, bot):
        bot.on_respond(r"(steam|daily) deal", self.on_respond)
        bot.on_help("steam", self.on_help)

    def on_respond(self, bot, msg, reply):
        page = requests.get("http://store.steampowered.com")
        tree = lxml.html.fromstring(page.text)
        if tree.cssselect(".dailydeal"):
            url = tree.cssselect(".dailydeal a")[0].get("href")
            original_price = tree.cssselect(".dailydeal_content .discount_original_price")[0].text
            final_price = tree.cssselect(".dailydeal_content .discount_final_price")[0].text
            reply("{0} - {1} - from {2} to {3}".format(url,
                                                       utils.get_website_title(url),
                                                       original_price,
                                                       final_price))
        else:
            reply("No daily deal.")

    def on_help(self, bot, msg, reply):
        reply("Syntax: steam|daily deal")
