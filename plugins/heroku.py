import requests
import sys


class Plugin:
    def on_command(self, bot, msg):
        if len(sys.argv) >= 2:
            action = sys.argv[1]
            if "status".startswith(action):
                url = "https://status.heroku.com/api/v3/current-status"
                headers = {"User-Agent": "SmartBot"}

                res = requests.get(url, headers=headers).json()
                print("Production: {0}".format(res["status"]["Production"]))
                print("Development: {0}".format(res["status"]["Development"]))
            else:
                print("No such action:", action)
        else:
            print(self.on_help())

    def on_help(self):
        return "Usage: heroku status"
