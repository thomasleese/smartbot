import io
import sympy
import unittest

class Plugin:
    def on_command(self, bot, msg, stdin, stdout, reply):
        expr = sympy.sympify(" ".join(msg["args"][1:]))
        print(expr, file=stdout)

    def on_help(self):
        return "Perform maths expressions."


class Test(unittest.TestCase):
    def setUp(self):
        self.plugin = Plugin()

    def test_command(self):
        for a in range(1, 1000, 50):
            for b in range(1, 1000, 50):
                stdout = io.StringIO()
                self.plugin.on_command(None, {"args": [None, str(a) + "*" + str(b)]}, None, stdout, None)
                self.assertEqual(int(float(stdout.getvalue().strip())), a * b)

    def test_help(self):
        self.assertTrue(self.plugin.on_help())
