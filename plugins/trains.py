import requests

import smartbot
from smartbot import utils
from smartbot.exceptions import *
from smartbot.formatting import *


class Plugin(smartbot.Plugin):
    """Get train times from National Rail."""
    names = ["trains"]

    def on_command(self, msg, stdin, stdout, reply):
        if len(msg["args"]) >= 3:
            url = "http://ojp.nationalrail.co.uk/service/ldb/liveTrainsJson"
            payload = {
                "liveTrainsFrom": msg["args"][1],
                "liveTrainsTo"  : msg["args"][2],
                "departing": "true",
            }

            session = utils.web.requests_session()
            res = session.get(url, params=payload).json()
            if not res["trains"]:
                raise StopCommand("No trains.")

            for i, train in enumerate(res["trains"]):
                if train[4]:
                    print("[{}]: the {} to {} on platform {} ({}).".format(
                        i, train[1], train[2], train[4], train[3].lower()
                    ), file=stdout)
                else:
                    print("[{}]: the {} to {} ({}).".format(
                        i, train[1], train[2], train[3].lower()
                    ), file=stdout)
        else:
            raise StopCommandWithHelp(self)

    def on_help(self):
        return "{} {} {}".format(
            super().on_help(),
            self.bot.format("from", Style.underline),
            self.bot.format("to", Style.underline)
        )
