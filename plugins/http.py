import io
import requests
import unittest


class Plugin:
    def on_command(self, bot, msg, stdin, stdout, reply):
        url = None
        if len(msg["args"]) >= 3:
            url = msg["args"][2]
        else:
            url = stdin.read().strip()

        if url:
            headers = {"User-Agent": "SmartBot"}
            page = requests.get(url, headers=headers, timeout=15)
            print(page.text, file=stdout)
        else:
            print(self.on_help(), file=stdout)

    def on_help(self):
        return "Usage: http get <url>"


class Test(unittest.TestCase):
    def setUp(self):
        self.plugin = Plugin()

    def test_search(self):
        stdout = io.StringIO()
        self.plugin.on_command(None, {"args": [None, "get", "http://google.com"]}, None, stdout, None)
        self.assertNotEqual(self.plugin.on_help(), stdout.getvalue().strip())

    def test_help(self):
        self.assertTrue(self.plugin.on_help())

    def test_no_args(self):
        stdout = io.StringIO()
        self.plugin.on_command(None, {"args": [None]}, stdout, stdout, None)
        self.assertEqual(self.plugin.on_help(), stdout.getvalue().strip())

        stdout = io.StringIO()
        self.plugin.on_command(None, {"args": [None, None]}, stdout, stdout, None)
        self.assertEqual(self.plugin.on_help(), stdout.getvalue().strip())
