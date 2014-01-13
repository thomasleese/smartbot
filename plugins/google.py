import requests
import urllib.parse

class Plugin:
    def __init__(self, key, cx):
        self.key = key
        self.cx = cx

    def __call__(self, bot):
        bot.on_respond(r"(?:google|search)(?: for)? (.*)$", self.on_respond)
        bot.on_help("google", self.on_help)

    def on_respond(self, bot, msg, reply):
        url = "https://www.googleapis.com/customsearch/v1?key={0}&cx={1}&q={2}".format(
            urllib.parse.quote(self.key),
            urllib.parse.quote(self.cx),
            urllib.parse.quote(msg["match"][0])
        )
        headers = { "User-Agent": "SmartBot" }

        res = requests.get(url, headers=headers).json()
        if res["items"]:
            for i, item in enumerate(res["items"][:5]):
                reply("[{0}]: {1}".format(i, item["link"]))
        else:
            reply("No results!")

    def on_help(self, bot, msg, reply):
        reply("Syntax: google|search [for] <query>")
