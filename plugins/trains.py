import io
import requests
import unittest
import urllib.parse


class Plugin:
    def on_command(self, bot, msg, stdin, stdout, reply):
        if len(msg["args"]) >= 3:
            url = "http://ojp.nationalrail.co.uk/service/ldb/liveTrainsJson?departing=true&liveTrainsFrom={0}&liveTrainsTo={1}".format(
                urllib.parse.quote(msg["args"][1]),
                urllib.parse.quote(msg["args"][2])
            )
            headers = {"User-Agent": "SmartBot"}

            res = requests.get(url, headers=headers).json()
            if res["trains"]:
                for i, train in enumerate(res["trains"]):
                    if train[4]:
                        print("[{0}]: the {1} to {2} on platform {3} ({4}).".format(i, train[1], train[2], train[4],
                                                                                    train[3].lower()), file=stdout)
                    else:
                        print("[{0}]: the {1} to {2} ({3}).".format(i, train[1], train[2], train[3].lower()), file=stdout)
            else:
                print("No trains.", file=stdout)
        else:
            print(self.on_help(), file=stdout)

    def on_help(self):
        return "Usage: trains <from> <to>"


class Test(unittest.TestCase):
    def setUp(self):
        self.plugin = Plugin()

    def test_command(self):
        stdout = io.StringIO()
        self.plugin.on_command(None, {"args": [None, "WAT", "SAL"]}, None, stdout, None)
        self.assertNotEqual("No trains.", stdout.getvalue().strip())

        stdout = io.StringIO()
        self.plugin.on_command(None, {"args": [None, "fsdfs", "fsdfs"]}, None, stdout, None)
        self.assertEqual("No trains.", stdout.getvalue().strip())

    def test_help(self):
        self.assertTrue(self.plugin.on_help())

    def test_no_args(self):
        stdout = io.StringIO()
        self.plugin.on_command(None, {"args": [None]}, stdout, stdout, None)
        self.assertEqual(self.plugin.on_help(), stdout.getvalue().strip())

        stdout = io.StringIO()
        self.plugin.on_command(None, {"args": [None, None]}, stdout, stdout, None)
        self.assertEqual(self.plugin.on_help(), stdout.getvalue().strip())
