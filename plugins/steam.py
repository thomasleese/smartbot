import lxml.html
import requests

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
            reply("{0} - from {1} to {2}".format(url, original_price, final_price))
        else:
            reply("No daily deal.")

    def on_help(self, bot, msg, reply):
        reply("Syntax: steam|daily deal")
