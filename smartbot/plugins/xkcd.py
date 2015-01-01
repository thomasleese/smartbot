import re

import smartbot.plugin
from smartbot.utils.web import get_title
from smartbot.formatting import Style


class Plugin(smartbot.plugin.Plugin):
    """Get an XKCD comic."""
    names = ["xkcd"]

    def on_message(self, msg, reply):
        match = re.findall(r"xkcd\s+(\d+)", msg["message"], re.IGNORECASE)
        for num in match:
            url = "http://xkcd.com/" + num
            reply("{0} -> {1}".format(url, get_title(url)))

    def on_help(self):
        return "{} {}".format(
            super().on_help(),
            self.bot.format("num", Style.underline)
        )
