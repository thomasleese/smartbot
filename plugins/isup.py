import io
import requests
import unittest
import urllib.parse


class Plugin:
    def on_command(self, bot, msg, stdin, stdout, reply):
        url = None
        if len(msg["args"]) >= 2:
            url = msg["args"][1]
        else:
            url = stdin.read().strip()

        url = "http://isitup.org/{0}.json".format(urllib.parse.quote(url))
        headers = {"User-Agent": "SmartBot"}

        res = requests.get(url, headers=headers).json()
        if res["status_code"] == 1:
            print("{0} looks up for me.".format(res["domain"]), file=stdout)
        else:
            print("{0} looks down for me.".format(res["domain"]), file=stdout)

    def on_help(self):
        return "Usage: isup <domain>"


class Test(unittest.TestCase):
    def setUp(self):
        self.plugin = Plugin()

    def test_isup(self):
        stdout = io.StringIO()
        self.plugin.on_command(None, {"args": [None, "google.com"]}, stdout, stdout, None)
        self.assertEqual("google.com looks up for me.", stdout.getvalue().strip())

    def test_isdown(self):
        stdout = io.StringIO()
        self.plugin.on_command(None, {"args": [None, "fsafsddsgss"]}, stdout, stdout, None)
        self.assertEqual("fsafsddsgss looks down for me.", stdout.getvalue().strip())

    def test_help(self):
        self.assertTrue(self.plugin.on_help())
