import io
import hashlib
import unittest


class Plugin:
    def on_command(self, bot, msg, stdin, stdout, reply):
        if len(msg["args"]) >= 2:
            algorithm = msg["args"][1]
            contents = " ".join(msg["args"][2:])
            if not contents:
                contents = stdin.read().strip()

            try:
                h = hashlib.new(algorithm)
            except ValueError:
                print("No such algorithm:", algorithm, file=stdout)
            except TypeError:
                print(self.on_help(), file=stdout)
            else:
                h.update(bytes(contents, "utf-8"))
                print(h.hexdigest(), file=stdout)
        else:
            print(self.on_help(), file=stdout)

    def on_help(self):
        return "Usage: hash <algorithm> <contents>"


class Test(unittest.TestCase):
    def setUp(self):
        self.plugin = Plugin()

    def test_md5(self):
        stdout = io.StringIO()
        self.plugin.on_command(None, {"args": [None, "md5", "hello"]}, None, stdout, None)
        self.assertEqual("5d41402abc4b2a76b9719d911017c592", stdout.getvalue().strip())

    def test_sha1(self):
        stdout = io.StringIO()
        self.plugin.on_command(None, {"args": [None, "sha1", "hello"]}, None, stdout, None)
        self.assertEqual("aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d", stdout.getvalue().strip())

    def test_sha512(self):
        stdout = io.StringIO()
        self.plugin.on_command(None, {"args": [None, "sha512", "hello"]}, None, stdout, None)
        self.assertEqual("9b71d224bd62f3785d96d46ad3ea3d73319bfbc2890caadae2dff72519673ca72323c3d99ba5c11d7c7acc6e14b8c5da0c4663475c2e5c3adef46f73bcdec043", stdout.getvalue().strip())

    def test_help(self):
        self.assertTrue(self.plugin.on_help())

    def test_no_args(self):
        stdout = io.StringIO()
        self.plugin.on_command(None, {"args": [None]}, stdout, stdout, None)
        self.assertEqual(self.plugin.on_help(), stdout.getvalue().strip())

        stdout = io.StringIO()
        self.plugin.on_command(None, {"args": [None, None]}, stdout, stdout, None)
        self.assertEqual(self.plugin.on_help(), stdout.getvalue().strip())
