import requests
import urllib.parse
import sys



class Plugin:
    def __init__(self, key, cx):
        self.key = key
        self.cx = cx

    def on_command(self, bot, msg):
        query = " ".join(sys.argv[1:])
        if not query:
            query = sys.stdin.read().strip()

        if query:
            url = "https://www.googleapis.com/customsearch/v1?key={0}&cx={1}&q={2}&num=5".format(
                urllib.parse.quote(self.key),
                urllib.parse.quote(self.cx),
                urllib.parse.quote(query)
            )
            headers = {"User-Agent": "SmartBot"}

            res = requests.get(url, headers=headers).json()
            if "error" in res:
                print(res["error"]["message"])
            elif "items" in res:
                for i, item in enumerate(res["items"]):
                    print("[{0}]: {1} - {2}".format(i, item["title"], item["link"]))
            else:
                print("No results!")
        else:
            print(self.on_help())

    def on_help(self):
        return "Usage: google <query>"
