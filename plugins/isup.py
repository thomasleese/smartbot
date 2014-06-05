import urllib.parse

import requests

import smartbot


class Plugin(smartbot.Plugin):
    names = ["isup"]

    def on_command(self, msg, stdin, stdout, reply):
        url = None
        if len(msg["args"]) >= 2:
            url = msg["args"][1]
        else:
            url = stdin.read().strip()

        url = "http://isitup.org/{0}.json".format(urllib.parse.quote(url))
        headers = {"User-Agent": "SmartBot"}

        res = requests.get(url, headers=headers).json()
        if res["status_code"] == 1:
            print("{0} looks up for me.".format(res["domain"]), file=stdout)
        else:
            print("{0} looks down for me.".format(res["domain"]), file=stdout)

    def on_help(self):
        return "Usage: isup <domain>"
