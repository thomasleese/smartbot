import smartbot


class Plugin(smartbot.Plugin):
    names = ["nicebot"]

    def __init__(self, nicebots):
        self.nicebots = nicebots

    def on_join(self, msg):
        for nicebot in self.nicebots:
            if nicebot["channel"] == msg["channel"] and msg["is_me"]:
                self.bot.send(nicebot["target"], nicebot["password"])

    def on_help(self):
        return "Authenticate with NiceBot."
