import io
import re
import unittest

from smartbot import utils


class Plugin:
    def on_message(self, bot, msg, reply):
        match = re.findall(r"xkcd\s+(\d+)", msg["message"], re.IGNORECASE)
        for num in match:
            url = "http://xkcd.com/" + num
            reply("{0} -> {1}".format(url, utils.web.get_title(url)))

    def on_help(self):
        return "Usage: xkcd <num>"


class Test(unittest.TestCase):
    def setUp(self):
        self.plugin = Plugin()

    def test_message(self):
        self.plugin.on_message(None, {"message": "xkcd 1335"}, lambda x: self.assertEqual("http://xkcd.com/1335 -> xkcd: Now", x))

    def test_help(self):
        self.assertTrue(self.plugin.on_help())
