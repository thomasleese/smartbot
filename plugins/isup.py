import urllib.parse

import requests

import smartbot
from smartbot import utils
from smartbot.exceptions import *
from smartbot.formatting import *


class Plugin(smartbot.Plugin):
    names = ["isup"]

    def on_command(self, msg, stdin, stdout, reply):
        url = None
        if len(msg["args"]) >= 2:
            url = msg["args"][1]
        else:
            url = stdin.read().strip()

        if not url:
            raise StopCommandWithHelp(self)

        url = "http://isitup.org/{0}.json".format(urllib.parse.quote(url))
        session = utils.web.requests_session()
        res = session.get(url).json()
        if res["status_code"] == 1:
            print("{0} is up from here.".format(res["domain"]), file=stdout)
        else:
            print("{0} is down from here.".format(res["domain"]), file=stdout)

    def on_help(self):
        return "{} {}".format(
            self.bot.format("isup", Style.bold),
            self.bot.format("domain", Style.underline),
        )
