import io
import requests
import unicodedata
import unittest
import urllib.parse


class Plugin:
    def on_command(self, bot, msg, stdin, stdout, reply):
        query = " ".join(msg["args"][1:])
        if not query:
            query = stdin.read().strip()

        if query:
            result = None
            try:
                result = unicodedata.lookup(query)
            except KeyError:
                try:
                    result = unicodedata.name(query)
                except ValueError:
                    try:
                        result = unicodedata.decimal(query)
                    except ValueError:
                        try:
                            result = unicodedata.digit(query)
                        except ValueError:
                            try:
                                result = unicodedata.numeric(query)
                            except ValueError:
                                result = None
            if result:
                print(result, file=stdout)
            else:
                print("Nothing found.", file=stdout)
        else:
            print(self.on_help(), file=stdout)

    def on_help(self):
        return "Usage: unicode <query>"


class Test(unittest.TestCase):
    def setUp(self):
        self.plugin = Plugin()

    def test_help(self):
        self.assertTrue(self.plugin.on_help())

    def test_no_args(self):
        stdout = io.StringIO()
        self.plugin.on_command(None, {"args": [None]}, stdout, stdout, None)
        self.assertEqual(self.plugin.on_help(), stdout.getvalue().strip())
