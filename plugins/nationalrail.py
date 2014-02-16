import requests
import urllib.parse


class Plugin:
    def __call__(self, bot):
        bot.on_respond(r"trains(?: from)? (\w{3}) to (\w{3})$", self.on_respond)
        bot.on_help("nationalrail", self.on_help)

    def on_respond(self, bot, msg, reply):
        match = msg["match"][0]
        url = "http://ojp.nationalrail.co.uk/service/ldb/liveTrainsJson?departing=true&liveTrainsFrom={0}&liveTrainsTo={1}".format(
            urllib.parse.quote(match[0]),
            urllib.parse.quote(match[1])
        )
        headers = {"User-Agent": "SmartBot"}

        res = requests.get(url, headers=headers).json()
        if res["trains"]:
            for i, train in enumerate(res["trains"]):
                if train[4]:
                    reply("[{0}]: the {1} to {2} on platform {3} ({4}).".format(i, train[1], train[2], train[4],
                                                                                train[3].lower()))
                else:
                    reply("[{0}]: the {1} to {2} ({3}).".format(i, train[1], train[2], train[3].lower()))
        else:
            reply("No trains.")

    def on_help(self, bot, msg, reply):
        reply("Syntax: trains [from] <from> to <to>")
