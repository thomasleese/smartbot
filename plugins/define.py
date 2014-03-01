import io
import requests
import unittest
import urllib.parse


class Plugin:
    def on_command(self, bot, msg, stdin, stdout, reply):
        topic = " ".join(msg["args"][1:])
        if not topic:
            topic = stdin.read().strip()

        if topic:
            url = "http://api.duckduckgo.com/?format=json&q={0}".format(urllib.parse.quote(topic))
            headers = {"User-Agent": "SmartBot"}

            res = requests.get(url, headers=headers).json()
            if res.get("AbstractText"):
                print(res["AbstractText"], file=stdout)
                if res.get("AbstractURL"):
                    print(res["AbstractURL"], file=stdout)
            elif res.get("RelatedTopics"):
                topic = res["RelatedTopics"][0]
                print(topic["Text"], file=stdout)
                if topic.get("FirstURL"):
                    print(topic["FirstURL"], file=stdout)
            elif res.get("Definition"):
                print(res["Definition"], file=stdout)
                if res.get("DefinitionURL"):
                    print(res["DefinitionURL"], file=stdout)
            else:
                print("Don't know what you're talking about.", file=stdout)
        else:
            print(self.on_help(), file=stdout)

    def on_help(self):
        return "Usage: define <topic>"


class Test(unittest.TestCase):
    def setUp(self):
        self.plugin = Plugin()

    def test_define(self):
        stdout = io.StringIO()
        self.plugin.on_command(None, {"args": [None, "cat"]}, None, stdout, None)
        self.assertNotEqual("Don't know what you're talking about.", stdout.getvalue().strip())
        self.assertNotEqual(self.plugin.on_help(), stdout.getvalue().strip())

    def test_help(self):
        self.assertTrue(self.plugin.on_help())

    def test_no_args(self):
        stdout = io.StringIO()
        self.plugin.on_command(None, {"args": [None]}, stdout, stdout, None)
        self.assertEqual(self.plugin.on_help(), stdout.getvalue().strip())
