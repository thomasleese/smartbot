import requests
import urllib.parse
import sys



class Plugin:
    def on_command(self, bot, msg):
        url = None
        if len(sys.argv) >= 2:
            url = sys.argv[1]
        else:
            url = sys.stdin.read().strip()

        url = "http://isitup.org/{0}.json".format(urllib.parse.quote(url))
        headers = {"User-Agent": "SmartBot"}

        res = requests.get(url, headers=headers).json()
        if res["status_code"] == 1:
            print("{0} looks up for me.".format(res["domain"]))
        else:
            print("{0} looks down for me.".format(res["domain"]))

    def on_help(self):
        return "Usage: isup <domain>"
