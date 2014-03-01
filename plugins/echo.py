import io
import unittest


class Plugin:
    def on_command(self, bot, msg, stdin, stdout, reply):
        print(*msg["args"][1:], file=stdout)

    def on_help(self):
        return "Usage: echo <string>"


class Test(unittest.TestCase):
    def setUp(self):
        self.plugin = Plugin()

    def test_words(self):
        for i in range(1, 100):
            stdout = io.StringIO()
            words = [None] + ["word"] * i
            self.plugin.on_command(None, {"args": words}, None, stdout, None)
            self.assertEqual(stdout.getvalue().strip(), " ".join(words[1:]))

    def test_help(self):
        self.assertTrue(self.plugin.on_help())
