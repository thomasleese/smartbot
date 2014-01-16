import urllib.parse
import requests

class Plugin:
    def __call__(self, bot):
        bot.on_respond(r"github st(atus)?$", self.on_respond)
        bot.on_help("githubstatus", self.on_help)

    def on_respond(self, bot, msg, reply):
        url = "https://status.github.com/api/last-message.json"
        headers = { "User-Agent": "SmartBot" }

        res = requests.get(url, headers=headers).json()
        reply("{0} - {1}".format(res["created_on"], res["body"]))

    def on_help(self, bot, msg, reply):
        reply("Syntax: github st[atus]")
