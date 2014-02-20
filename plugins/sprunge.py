import requests
import sys


class Plugin:
    def on_command(self, bot, msg):
        contents = sys.stdin.read().strip()
        if contents:
            headers = {"User-Agent": "SmartBot"}
            payload = {"sprunge": contents}
            page = requests.post("http://sprunge.us", data=payload, headers=headers)
            print(page.text)
        else:
            print("Expected input on stdin.")

    def on_help(self, bot):
        return "Usage: sprunge"
