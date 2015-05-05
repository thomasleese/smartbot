import lxml.html

import smartbot.plugin
from smartbot.utils.web import requests_session
from smartbot.exceptions import StopCommand, StopCommandWithHelp
from smartbot.formatting import Style


SEARCH_URL = "http://www.xboxachievements.com/search.php"
GUIDE_URL = "http://www.xboxachievements.com/game/{0}/guide/"


class Plugin(smartbot.plugin.Plugin):
    """A plugin which provides an interface to xboxachievements.com."""
    names = ["ach"]

    def __init__(self):
        self.saved_items = {}

    def _search(self, terms):
        session = requests_session()
        page = session.post(SEARCH_URL, data={"search": terms})
        tree = lxml.html.fromstring(page.text)

        results = []
        elements = tree.cssselect(".bl_la_main .linkT")
        for i, element in enumerate(elements[::2]):
            game_id = element.get("href")[6:-10]
            self.saved_items[i] = game_id
            results.append(element.text_content())

        return results

    @staticmethod
    def _guide(name):
        game_id = name.lower().replace(" ", "-")
        session = requests_session()
        page = session.get(GUIDE_URL.format(game_id))
        tree = lxml.html.fromstring(page.text)

        li_elements = tree.cssselect(
            "#col_l .bl_la_main_guide .showhide ul li")
        if li_elements:
            return [x.text_content().strip() for x in li_elements[:5]]
        else:
            elements = tree.cssselect("#col_l .bl_la_main_guide .showhide p")
            if not elements:
                elements = tree.cssselect(
                    "#col_l .bl_la_main_guide .showhide div div")

            if elements:
                info = []
                html = lxml.html.tostring(elements[0])
                lines = html.decode("utf-8").split("<br>")
                for line in lines[1:6]:
                    span_str = "<span>{0}</span>".format(line)
                    span = lxml.html.fragment_fromstring(span_str)
                    s = span.text_content().strip()
                    if s.startswith("-"):
                        s = s[1:]
                    info.append(s)
                return info

    def on_command(self, msg, stdin, stdout):
        game = " ".join(msg["args"][1:])
        if not game:
            game = stdin.read().strip()

        if game:
            try:
                game = self.saved_items[int(game)]
            except (IndexError, ValueError):
                pass

            guide = self._guide(game)
            if guide:
                for g in guide:
                    print(g, file=stdout)
            else:
                results = self._search(game)
                if results:
                    for i, r in enumerate(results):
                        print("[{0}]: {1}".format(i, r), file=stdout)
                else:
                    raise StopCommand("Can't find any games.")
        else:
            raise StopCommandWithHelp(self)

    def on_help(self):
        return "{} {}".format(
            self.bot.format("ach", Style.bold),
            self.bot.format("game", Style.underline)
        )
