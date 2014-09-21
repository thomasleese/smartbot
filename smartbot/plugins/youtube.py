import isodate

import smartbot
from smartbot import utils
from smartbot.exceptions import *
from smartbot.formatting import *


class Plugin(smartbot.Plugin):
    """Get information about posted YouTube videos."""
    names = ["youtube", "utube"]

    def __init__(self, key):
        self.key = key

    def _search(self, query):
        url = "https://www.googleapis.com/youtube/v3/search"
        payload = {
            "key": self.key,
            "q": query,
            "maxResults": 3,
            "part": "snippet"
        }

        s = utils.web.requests_session()
        res = s.get(url, params=payload).json()
        return res.get("items", [])

    def _format_result(self, i, result):
        url = "https://www.youtube.com/watch?v={}".format(result["id"]["videoId"])
        return "{}: {} {}".format(
            self.bot.format("[{}]".format(i), Style.bold),
            self.bot.format(result["snippet"]["title"], Style.underline),
            url
        )

    def on_command(self, msg, stdin, stdout, reply):
        query = " ".join(msg["args"][1:])
        if not query:
            query = stdin.read().strip()

        results = self._search(query)
        for i, result in enumerate(results):
            print(self._format_result(i, result), file=stdout)

    def on_help(self):
        return "{} {}".format(
            super().on_help(),
            self.bot.format("query", Style.underline)
        )
