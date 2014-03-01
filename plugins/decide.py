import io
import random
import shlex
import unittest


class Plugin:
    def on_command(self, bot, msg, stdin, stdout, reply):
        args = msg["args"][1:]
        if not args:
            args = shlex.split(stdin.read().strip())
        if args:
            print(random.choice(args), file=stdout)
        else:
            print(self.on_help(), file=stdout)

    def on_help(self):
        return "Usage: decide <a> <b> …"


class Test(unittest.TestCase):
    def setUp(self):
        self.plugin = Plugin()

    def test_decisions(self):
        decisions = []
        for i in range(1, 10):
            decisions.append("decision {0}".format(i))
            stdout = io.StringIO()
            self.plugin.on_command(None, {"args": [None] + decisions}, None, stdout, None)
            self.assertTrue(stdout.getvalue().strip() in decisions)

    def test_help(self):
        self.assertTrue(self.plugin.on_help())

    def test_no_args(self):
        stdout = io.StringIO()
        self.plugin.on_command(None, {"args": [None]}, stdout, stdout, None)
        self.assertEqual(self.plugin.on_help(), stdout.getvalue().strip())
