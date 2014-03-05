import io
import unittest


class Plugin:
    def on_command(self, bot, msg, stdin, stdout, reply):
        if len(msg["args"]) >= 2:
            user = msg["args"][1]
            message = " ".join(msg["args"][2:])
            if not message:
                message = stdin.read().strip()

            print("{0}: {1}".format(user, message), file=stdout)

    def on_help(self):
        return "Usage: sendto <user> [<message>]"


class Test(unittest.TestCase):
    def setUp(self):
        self.plugin = Plugin()

    def test_words(self):
        stdout = io.StringIO()
        self.plugin.on_command(None, {"args": [None, "thing", "hello"]}, None, stdout, None)
        self.assertEqual(stdout.getvalue().strip(), "thing: hello")

    def test_help(self):
        self.assertTrue(self.plugin.on_help())
