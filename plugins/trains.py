import requests

import smartbot


class Plugin(smartbot.Plugin):
    names = ["trains"]

    def on_command(self, msg, stdin, stdout, reply):
        if len(msg["args"]) >= 3:
            url = "http://ojp.nationalrail.co.uk/service/ldb/liveTrainsJson"
            headers = {"User-Agent": "SmartBot"}
            payload = {
                "liveTrainsFrom": msg["args"][1],
                "liveTrainsTo"  : msg["args"][2],
                "departing": "true",
            }

            res = requests.get(url, headers=headers, params=payload).json()
            if res["trains"]:
                for i, train in enumerate(res["trains"]):
                    if train[4]:
                        print("[{0}]: the {1} to {2} on platform {3} ({4}).".format(i, train[1], train[2], train[4],
                                                                                    train[3].lower()), file=stdout)
                    else:
                        print("[{0}]: the {1} to {2} ({3}).".format(i, train[1], train[2], train[3].lower()), file=stdout)
            else:
                print("No trains.", file=stdout)
        else:
            print(self.on_help(), file=stdout)

    def on_help(self):
        return "Usage: trains <from> <to>"
