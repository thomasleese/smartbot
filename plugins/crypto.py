import base64
import io
import unittest


class Plugin:
    def get_hash_func(self, algorithm, action):
        if algorithm == "base64" or algorithm == "b64":
            if "encode".startswith(action):
                return base64.b64encode
            elif "decode".startswith(action):
                return base64.b64decode
        elif algorithm == "base32" or algorithm == "b32":
            if "encode".startswith(action):
                return base64.b32encode
            elif "decode".startswith(action):
                return base64.b32decode
        elif algorithm == "base16" or algorithm == "b16":
            if "encode".startswith(action):
                return base64.b16encode
            elif "decode".startswith(action):
                return base64.b16decode

    def on_command(self, bot, msg, stdin, stdout, reply):
        if len(msg["args"]) >= 3:
            algorithm = msg["args"][1]
            action = msg["args"][2]
            contents = " ".join(msg["args"][3:])
            if not contents:
                contents = stdin.read().strip()

            func = self.get_hash_func(algorithm, action)
            if func:
                result = str(func(bytes(contents, "utf-8")), "utf-8")
                print(result, file=stdout)
            else:
                print("No hash algorithm:", algorithm, file=stdout)
        else:
            print(self.on_help(), file=stdout)

    def on_help(self):
        return "Usage: crypto <algorithm> encode|decode <contents>"


class Test(unittest.TestCase):
    def setUp(self):
        self.plugin = Plugin()

    def test_base64(self):
        stdout = io.StringIO()
        self.plugin.on_command(None, {"args": [None, "b64", "encode", "hello"]}, None, stdout, None)
        self.assertEqual("aGVsbG8=", stdout.getvalue().strip())

        stdout.seek(0)
        stdout2 = io.StringIO()
        self.plugin.on_command(None, {"args": [None, "b64", "decode"]}, stdout, stdout2, None)
        self.assertEqual("hello", stdout2.getvalue().strip())        

    def test_base32(self):
        stdout = io.StringIO()
        self.plugin.on_command(None, {"args": [None, "b32", "encode", "hello"]}, None, stdout, None)
        self.assertEqual("NBSWY3DP", stdout.getvalue().strip())

        stdout.seek(0)
        stdout2 = io.StringIO()
        self.plugin.on_command(None, {"args": [None, "b32", "decode"]}, stdout, stdout2, None)
        self.assertEqual("hello", stdout2.getvalue().strip())        

    def test_base16(self):
        stdout = io.StringIO()
        self.plugin.on_command(None, {"args": [None, "b16", "encode", "hello"]}, None, stdout, None)
        self.assertEqual("68656C6C6F", stdout.getvalue().strip())

        stdout.seek(0)
        stdout2 = io.StringIO()
        self.plugin.on_command(None, {"args": [None, "b16", "decode"]}, stdout, stdout2, None)
        self.assertEqual("hello", stdout2.getvalue().strip())

    def test_help(self):
        self.assertTrue(self.plugin.on_help())

    def test_no_args(self):
        stdout = io.StringIO()
        self.plugin.on_command(None, {"args": [None]}, stdout, stdout, None)
        self.assertEqual(self.plugin.on_help(), stdout.getvalue().strip())

        stdout = io.StringIO()
        self.plugin.on_command(None, {"args": [None, None]}, stdout, stdout, None)
        self.assertEqual(self.plugin.on_help(), stdout.getvalue().strip())
