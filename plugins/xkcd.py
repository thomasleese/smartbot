import re

from smartbot import utils


class Plugin:
    def on_message(self, bot, msg, reply):
        match = re.findall(r"xkcd\s+(\d+)", msg["message"], re.IGNORECASE)
        for num in match:
            url = "http://xkcd.com/" + num
            reply("{0} -> {1}".format(url, utils.web.get_title(url)))

    def on_help(self):
        return "Usage: xkcd <num>"
