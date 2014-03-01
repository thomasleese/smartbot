import io
import requests
import unittest


class Plugin:
    def on_command(self, bot, msg, stdin, stdout, reply):
        if len(msg["args"]) >= 2:
            action = msg["args"][1]
            if "status".startswith(action):
                url = "https://status.heroku.com/api/v3/current-status"
                headers = {"User-Agent": "SmartBot"}

                res = requests.get(url, headers=headers).json()
                print("Production: {0}".format(res["status"]["Production"]), file=stdout)
                print("Development: {0}".format(res["status"]["Development"]), file=stdout)
            else:
                print("No such action:", action, file=stdout)
        else:
            print(self.on_help(), file=stdout)

    def on_help(self):
        return "Usage: heroku status"


class Test(unittest.TestCase):
    def setUp(self):
        self.plugin = Plugin()

    def test_status(self):
        stdout = io.StringIO()
        self.plugin.on_command(None, {"args": [None, "status"]}, None, stdout, None)
        self.assertFalse(stdout.getvalue().startswith("No such action"))
        self.assertNotEqual(self.plugin.on_help(), stdout.getvalue().strip())

    def test_help(self):
        self.assertTrue(self.plugin.on_help())

    def test_no_args(self):
        stdout = io.StringIO()
        self.plugin.on_command(None, {"args": [None]}, stdout, stdout, None)
        self.assertEqual(self.plugin.on_help(), stdout.getvalue().strip())
