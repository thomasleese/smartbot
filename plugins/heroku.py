import requests

import smartbot
from smartbot import utils
from smartbot.exceptions import *
from smartbot.formatting import *


STATUS_URL = "https://status.heroku.com/api/v3/current-status"


class Plugin(smartbot.Plugin):
    names = ["heroku"]

    def on_command(self, msg, stdin, stdout, reply):
        if len(msg["args"]) <= 1:
            raise StopCommandWithHelp(self)

        action = msg["args"][1]
        if "status".startswith(action):
            session = utils.web.requests_session()
            res = session.get(STATUS_URL).json()
            status = res["status"]
            print("Production: {}".format(status["Production"]), file=stdout)
            print("Development: {}".format(status["Development"]), file=stdout)
        else:
            raise StopCommandWithHelp(self)

    def on_help(self):
        return "{} status".format(
            self.bot.format("heroku", Style.bold),
        )
