import smartbot.plugin
from smartbot.utils.web import requests_session
from smartbot.exceptions import StopCommandWithHelp
from smartbot.formatting import Style


class Plugin(smartbot.plugin.Plugin):
    """Unshorten a shortened URL."""
    names = ["unshorten"]

    def __init__(self, api_key):
        self.api_key = api_key

    def on_command(self, msg, stdin, stdout):
        short_urls = msg["args"][1:]
        if not short_urls:
            short_urls = stdin.read().strip().split()

        if not short_urls:
            raise StopCommandWithHelp(self)

        url = "http://api.unshorten.it/"
        session = requests_session()
        for i, short_url in enumerate(short_urls):
            payload = {
                "shortURL": short_url,
                "apiKey": self.api_key
            }

            text = session.get(url, params=payload).text
            print("{}: {}".format(
                self.bot.format("[{}]".format(i), Style.bold),
                text), file=stdout)

    def on_help(self):
        return "{} {} …".format(
            super().on_help(),
            self.bot.format("short_url", Style.underline),
        )
