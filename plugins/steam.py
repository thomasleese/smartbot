import io
import lxml.html
import requests
import unittest

from smartbot import utils


class Plugin:
    def on_command(self, bot, msg, stdin, stdout, reply):
        if len(msg["args"]) >= 2:
            action = msg["args"][1]
            if "deal".startswith(action):
                page = requests.get("http://store.steampowered.com")
                tree = lxml.html.fromstring(page.text)
                if tree.cssselect(".dailydeal"):
                    url = tree.cssselect(".dailydeal a")[0].get("href")
                    original_price = tree.cssselect(".dailydeal_content .discount_original_price")[0].text
                    final_price = tree.cssselect(".dailydeal_content .discount_final_price")[0].text
                    print("{0} - {1} - from {2} to {3}".format(url,
                                                               utils.web.get_title(url),
                                                               original_price,
                                                               final_price), file=stdout)
                else:
                    print("No daily deal.", file=stdout)
            else:
                print("No such action:", action, file=stdout)
        else:
            print(self.on_help(), file=stdout)

    def on_help(self):
        return "Usage: steam deal"


class Test(unittest.TestCase):
    def setUp(self):
        self.plugin = Plugin()

    def test_bundle(self):
        stdout = io.StringIO()
        self.plugin.on_command(None, {"args": [None, "deal"]}, stdout, stdout, None)
        self.assertNotEqual("No daily deal.", stdout.getvalue().strip())

    def test_no_action(self):
        stdout = io.StringIO()
        self.plugin.on_command(None, {"args": [None, "cat"]}, stdout, stdout, None)
        self.assertEqual("No such action: cat", stdout.getvalue().strip())

    def test_help(self):
        self.assertTrue(self.plugin.on_help())

    def test_no_args(self):
        stdout = io.StringIO()
        self.plugin.on_command(None, {"args": [None]}, stdout, stdout, None)
        self.assertEqual(self.plugin.on_help(), stdout.getvalue().strip())
