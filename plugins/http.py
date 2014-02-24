import requests
import sys


class Plugin:
    def on_command(self, bot, msg):
        url = None
        if len(sys.argv) >= 3:
            url = sys.argv[2]
        else:
            url = sys.stdin.read().strip()

        if url:
            headers = {"User-Agent": "SmartBot"}
            page = requests.get(url, headers=headers)
            print(page.text)
        else:
            print(self.on_help())

    def on_help(self):
        return "Usage: http get <url>"
