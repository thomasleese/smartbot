import smartbot.plugin
from smartbot.utils.web import requests_session
from smartbot.exceptions import StopCommandWithHelp
from smartbot.formatting import Style


class Plugin(smartbot.plugin.Plugin):
    """Perform an HTTP GET request."""
    names = ["http", "web"]

    def on_command(self, msg, stdin, stdout):
        url = None
        if len(msg["args"]) >= 3:
            url = msg["args"][2]
        else:
            url = stdin.read().strip()

        if url:
            session = requests_session()
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
