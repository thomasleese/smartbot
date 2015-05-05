import urllib.parse

import smartbot.plugin
from smartbot.utils.web import requests_session
from smartbot.exceptions import StopCommandWithHelp
from smartbot.formatting import Style


class Plugin(smartbot.plugin.Plugin):
    """Check if a website is up or not."""
    names = ["isup"]

    def on_command(self, msg, stdin, stdout):
        url = None
        if len(msg["args"]) >= 2:
            url = msg["args"][1]
        else:
            url = stdin.read().strip()

        if not url:
            raise StopCommandWithHelp(self)

        url = "http://isitup.org/{0}.json".format(urllib.parse.quote(url))
        session = requests_session()
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
