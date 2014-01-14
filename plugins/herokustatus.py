import urllib.parse
import requests

class Plugin:
    def __call__(self, bot):
        bot.on_respond(r"heroku st(atus)?$", self.on_respond)
        bot.on_help("herokustatus", self.on_help)

    def on_respond(self, bot, msg, reply):
        url = "https://status.heroku.com/api/v3/current-status"
        headers = { "User-Agent": "SmartBot" }

        res = requests.get(url, headers=headers).json()
        reply("Production: {0}\nDevelopment: {1}".format(res["status"]["Production"], res["status"]["Development"]))

    def on_help(self, bot, reply):
        reply("Syntax: heroku st[atus]")
