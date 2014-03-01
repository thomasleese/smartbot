import io
import requests
import lxml.etree
import unittest
import urllib.parse


class Plugin:
    def on_command(self, bot, msg, stdin, stdout, reply):
        query = " ".join(msg["args"][1:])
        if not query:
            query = stdin.read().strip()

        if query:
            url = "http://google.com/complete/search?q={0}&output=toolbar".format(urllib.parse.quote(query))
            headers = {"User-Agent": "SmartBot"}

            page = requests.get(url, headers=headers)
            tree = lxml.etree.fromstring(page.text)

            suggestions = []
            for suggestion in tree.xpath("//suggestion"):
                suggestions.append(suggestion.get("data"))

            if suggestions:
                print(", ".join(suggestions[:5]), file=stdout)
            else:
                print("No suggestions.", file=stdout)
        else:
            print(self.on_help(), file=stdout)

    def on_help(self):
        return "Usage: complete <query>"


class Test(unittest.TestCase):
    def setUp(self):
        self.plugin = Plugin()

    def test_suggestions(self):
        stdout = io.StringIO()
        self.plugin.on_command(None, {"args": [None, "hello"]}, None, stdout, None)
        self.assertTrue(stdout.getvalue().strip())

    def test_no_suggestions(self):
        stdout = io.StringIO()
        self.plugin.on_command(None, {"args": [None, "fsjklfsjlkfsjklfsdajlkfdsjklfjlkfajlkfajklfa"]}, None, stdout, None)
        self.assertEqual("No suggestions.", stdout.getvalue().strip())

    def test_help(self):
        self.assertTrue(self.plugin.on_help())

    def test_no_args(self):
        stdout = io.StringIO()
        self.plugin.on_command(None, {"args": [None]}, stdout, stdout, None)
        self.assertEqual(self.plugin.on_help(), stdout.getvalue().strip())
