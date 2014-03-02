import io
import re
import unittest

from smartbot import utils


class Plugin:
    def on_message(self, bot, msg, reply):
        match = re.findall(r"(https?://[^\s]+)", msg["message"], re.IGNORECASE)
        for i, url in enumerate(match):
            title = utils.web.get_title(url)
            if title:
                reply("[{0}]: {1}".format(i, title))

    def on_help(self):
        return "Echos the titles of websites for any HTTP(S) URL."


class Test(unittest.TestCase):
    def setUp(self):
        self.plugin = Plugin()

    def test_message(self):
        self.plugin.on_message(None, {"message": "http://tomleese.me.uk"}, lambda x: self.assertEqual("[0]: Tom Leese", x))

    def test_help(self):
        self.assertTrue(self.plugin.on_help())
