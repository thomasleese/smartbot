import requests


class Plugin:
    def __call__(self, bot):
        bot.on_respond(r"chat|conversation", self.on_respond)
        bot.on_help("chat", self.on_help)

    def on_respond(self, bot, msg, reply):
        url = "http://chatoms.com/chatom.json?Normal=1&Fun=2&Philosophy=3&Out+There=4"
        headers = {"User-Agent": "SmartBot"}

        res = requests.get(url, headers=headers).json()
        if res.get("text"):
            reply(res["text"])
        else:
            reply("No conversation starters for you.")

    def on_help(self, bot, msg, reply):
        reply("Syntax: chat|conversation")
