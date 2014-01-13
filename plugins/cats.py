import requests
import urllib.parse

class Plugin:
    def __call__(self, bot):
        bot.on_respond(r"cat(s)?(fact)?", self.on_respond)
        bot.on_help("cats", self.on_help)

    def on_respond(self, bot, msg, reply):
        url = "http://catfacts-api.appspot.com/api/facts?number=1"
        headers = { "User-Agent": "SmartBot" }

        res = requests.get(url, headers=headers).json()
        if res.get("success"):
            reply(res["facts"][0])
        else:
            reply("No cat facts today. ☹")

    def on_help(self, bot, msg, reply):
        reply("Syntax: cat[fact]")
