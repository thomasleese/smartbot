import requests
import urllib.parse


class Plugin:
    def __call__(self, bot):
        bot.on_respond(r"is (.*) (?:up|down)\??$", self.on_respond)
        bot.on_respond(r"isup (.*)$", self.on_respond)
        bot.on_help("isup", self.on_help)

    def on_respond(self, bot, msg, reply):
        url = "http://isitup.org/{0}.json".format(urllib.parse.quote(msg["match"][0]))
        headers = {"User-Agent": "SmartBot"}

        res = requests.get(url, headers=headers).json()
        if res["status_code"] == 1:
            reply("{0} looks up for me.".format(res["domain"]))
        else:
            reply("{0} looks down for me.".format(res["domain"]))

    def on_help(self, bot, msg, reply):
        reply("Syntax: is <domain> up|down")
