import re

import smartbot
from smartbot import utils
from smartbot.exceptions import *
from smartbot.formatting import *


class Plugin(smartbot.Plugin):
    """Get URL titles."""
    names = ["url_titles"]

    def on_message(self, msg, reply):
        match = re.findall(r"(https?://[^\s]+)", msg["message"], re.IGNORECASE)
        for i, url in enumerate(match):
            title = utils.web.get_title(url)
            if title:
                reply("{}: {}".format(
                    self.bot.format("[{}]".format(i), Style.bold), title
                ))

    def on_help(self):
        return "Echos the title of any HTTP(S) URL."
