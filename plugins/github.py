import requests
import sys


class Plugin:
    def on_command(self, bot, msg):
        if len(sys.argv) >= 2:
            action = sys.argv[1]
            if "status".startswith(action):
                url = "https://status.github.com/api/last-message.json"
                headers = {"User-Agent": "SmartBot"}

                res = requests.get(url, headers=headers).json()
                print("{0} - {1}".format(res["created_on"], res["body"]))
            else:
                print("No such action:", action)
        else:
            print(self.on_help(bot))

    def on_help(self, bot):
        return "Usage: github status"
