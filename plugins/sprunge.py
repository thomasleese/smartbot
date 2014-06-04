import io
import requests
import unittest

import smartbot.utils


class Plugin:
    def on_command(self, bot, msg, stdin, stdout, reply):
        contents = stdin.read().strip()
        if contents:
            print(smartbot.utils.web.sprunge(contents), file=stdout)
        else:
            print("Expected input on stdin.", file=stdout)

    def on_help(self):
        return "Usage: sprunge"


class Test(unittest.TestCase):
    def setUp(self):
        self.plugin = Plugin()

    def test_no_stdin(self):
        stdout = io.StringIO()
        self.plugin.on_command(None, None, stdout, stdout, None)
        self.assertEqual("Expected input on stdin.", stdout.getvalue().strip())

    def test_upload(self):
        stdout = io.StringIO()
        self.plugin.on_command(None, None, io.StringIO("test"), stdout, None)
        self.assertTrue(stdout.getvalue().strip().startswith("http://sprunge.us/"))

    def test_help(self):
        self.assertTrue(self.plugin.on_help())
