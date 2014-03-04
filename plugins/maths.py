import io
import unittest

from sympy.parsing import sympy_parser

class Plugin:
    def on_command(self, bot, msg, stdin, stdout, reply):
        expr = " ".join(msg["args"][1:])
        expr = sympy_parser.parse_expr(expr)
        print(expr.evalf(), file=stdout)

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
