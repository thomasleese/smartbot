import smartbot
from smartbot import utils
from smartbot.exceptions import *
from smartbot.formatting import *


class Plugin(smartbot.Plugin):
    """Perform an HTTP GET request."""
    names = ["http", "web"]

    def on_command(self, msg, stdin, stdout, reply):
        url = None
        if len(msg["args"]) >= 3:
            url = msg["args"][2]
        else:
            url = stdin.read().strip()

        if url:
            session = utils.web.requests_session()
            page = session.get(url, timeout=15)
            print(page.text, file=stdout)
        else:
            raise StopCommandWithHelp(self)

    def on_help(self):
        return "{}|{} get {}".format(
            self.bot.format("http", Style.bold),
            self.bot.format("web", Style.bold),
            self.bot.format("url", Style.underline),
        )
