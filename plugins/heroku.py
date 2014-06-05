import requests

import smartbot


class Plugin(smartbot.Plugin):
    names = ["heroku"]

    def on_command(self, msg, stdin, stdout, reply):
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
