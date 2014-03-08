import io
import re
import unittest


class Plugin:
    def on_command(self, bot, msg, stdin, stdout, reply):
        pattern_str = " ".join(msg["args"][1:])
        if pattern_str:
            pattern = re.compile(pattern_str)
            for line in map(str.strip, stdin):
                if pattern_str in line or re.match(pattern, line):
                    print(line, file=stdout)
        else:
            print(self.on_help(), file=stdout)

    def on_help(self):
        return "Usage: grep <pattern>"


class Test(unittest.TestCase):
    def setUp(self):
        self.plugin = Plugin()

    def test_words(self):
        stdout = io.StringIO()
        stdin = io.StringIO("this is one line\nthis is another\n")
        self.plugin.on_command(None, {"args": [None, "another"]}, stdin, stdout, None)
        self.assertEqual(stdout.getvalue().strip(), "this is another")

    def test_help(self):
        self.assertTrue(self.plugin.on_help())
