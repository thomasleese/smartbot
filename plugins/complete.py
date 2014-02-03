import requests
import lxml.etree
import urllib.parse


class Plugin:
    def on_command(self, bot, stdin, stdout, args):
        query = " ".join(args)
        if not query:
            query = stdin.read().strip()

        if not query:
            print(self.on_help(bot), file=stdout)
            return

        url = "http://google.com/complete/search?q={0}&output=toolbar".format(urllib.parse.quote(query))
        headers = {"User-Agent": "SmartBot"}

        page = requests.get(url, headers=headers)
        tree = lxml.etree.fromstring(page.text)

        suggestions = []
        for suggestion in tree.xpath("//suggestion"):
            suggestions.append(suggestion.get("data"))

        if suggestions:
            print(", ".join(suggestions[:5]), file=stdout)
        else:
            print("No suggestions.", file=stdout)

    def on_help(self, bot):
        return "Usage: complete <query>"
