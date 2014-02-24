import requests
import lxml.etree
import urllib.parse
import sys



class Plugin:
    def on_command(self, bot, msg):
        query = " ".join(sys.argv[1:])
        if not query:
            query = sys.stdin.read().strip()

        if query:
            url = "http://google.com/complete/search?q={0}&output=toolbar".format(urllib.parse.quote(query))
            headers = {"User-Agent": "SmartBot"}

            page = requests.get(url, headers=headers)
            tree = lxml.etree.fromstring(page.text)

            suggestions = []
            for suggestion in tree.xpath("//suggestion"):
                suggestions.append(suggestion.get("data"))

            if suggestions:
                print(", ".join(suggestions[:5]))
            else:
                print("No suggestions.")
        else:
            print(self.on_help())

    def on_help(self):
        return "Usage: complete <query>"
