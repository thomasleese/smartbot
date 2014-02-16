import re
import requests
import urllib.parse


class Plugin:
    def __call__(self, bot):
        bot.on_respond(r"slogan(?:ise)? (.*)$", self.on_respond)
        bot.on_help("slogan", self.on_help)

    def on_respond(self, bot, msg, reply):
        url = "http://www.sloganizer.net/en/outbound.php?slogan={0}".format(
            urllib.parse.quote(msg["match"][0])
        )
        headers = {"User-Agent": "SmartBot"}

        page = requests.get(url, headers=headers)
        reply(re.sub("<.*?>", "", page.text))

    def on_help(self, bot, msg, reply):
        reply("Syntax: slogan[ise] <thing>")
