import requests

import smartbot


class Plugin(smartbot.Plugin):
    names = ["http", "web"]

    def on_command(self, msg, stdin, stdout, reply):
        url = None
        if len(msg["args"]) >= 3:
            url = msg["args"][2]
        else:
            url = stdin.read().strip()

        if url:
            headers = {"User-Agent": "SmartBot"}
            page = requests.get(url, headers=headers, timeout=15)
            print(page.text, file=stdout)
        else:
            print(self.on_help(), file=stdout)

    def on_help(self):
        return "Usage: http get <url>"
