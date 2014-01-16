import requests
import time
import urllib.parse

class Plugin:
    def __call__(self, bot):
        bot.on_respond(r"(?:give me a |gimme a |gimme )joke$", self.on_respond)
        bot.on_help("joke", self.on_help)

    def on_respond(self, bot, msg, reply):
        url = "http://jokels.com/random_joke"
        headers = { "User-Agent": "SmartBot" }

        res = requests.get(url, headers=headers).json()
        reply(res["joke"]["question"])
        time.sleep(2)
        reply(res["joke"]["answer"])

    def on_help(self, bot, msg, reply):
        reply("Syntax: [give me a] joke")
