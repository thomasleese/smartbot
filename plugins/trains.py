import requests
import urllib.parse
import sys


class Plugin:
    def on_command(self, bot, msg):
        if len(sys.argv) >= 3:
            url = "http://ojp.nationalrail.co.uk/service/ldb/liveTrainsJson?departing=true&liveTrainsFrom={0}&liveTrainsTo={1}".format(
                urllib.parse.quote(sys.argv[1]),
                urllib.parse.quote(sys.argv[2])
            )
            headers = {"User-Agent": "SmartBot"}

            res = requests.get(url, headers=headers).json()
            if res["trains"]:
                for i, train in enumerate(res["trains"]):
                    if train[4]:
                        print("[{0}]: the {1} to {2} on platform {3} ({4}).".format(i, train[1], train[2], train[4],
                                                                                    train[3].lower()))
                    else:
                        print("[{0}]: the {1} to {2} ({3}).".format(i, train[1], train[2], train[3].lower()))
            else:
                print("No trains.")
        else:
            print(self.on_help())

    def on_help(self):
        return "Usage: trains <from> <to>"
