import io
import lxml.html
import requests
import unittest


class Plugin:
    def __init__(self):
        self.saved_items = {}

    def search(self, terms):
        url = "http://www.xboxachievements.com/search.php"
        page = requests.post(url, data={"search": terms})
        tree = lxml.html.fromstring(page.text)

        results = []
        elements = tree.cssselect(".bl_la_main .linkT")
        for i, element in enumerate(elements[::2]):
            game_id = element.get("href")[6:-10]
            self.saved_items[i] = game_id
            results.append(element.text_content())

        return results

    def guide(self, name):
        game_id = name.lower().replace(" ", "-")
        url = "http://www.xboxachievements.com/game/{0}/guide/".format(game_id)
        page = requests.get(url)
        tree = lxml.html.fromstring(page.text)

        li_elements = tree.cssselect("#col_l .bl_la_main_guide .showhide ul li")
        if li_elements:
            return [x.text_content().strip() for x in li_elements[:5]]
        else:
            elements = tree.cssselect("#col_l .bl_la_main_guide .showhide p")
            if not elements:
                elements = tree.cssselect("#col_l .bl_la_main_guide .showhide div div")

            if elements:
                info = []
                html = lxml.html.tostring(elements[0])
                lines = html.decode("utf-8").split("<br>")
                for line in lines[1:6]:
                    span = lxml.html.fragment_fromstring("<span>{0}</span>".format(line))
                    s = span.text_content().strip()
                    if s.startswith("-"):
                        s = s[1:]
                    info.append(s)
                return info

    def on_command(self, bot, msg, stdin, stdout, reply):
        game = " ".join(msg["args"][1:])
        if not game:
            game = stdin.read().strip()

        if game:
            try:
                game = self.saved_items[int(game)]
            except (IndexError, ValueError):
                pass

            guide = self.guide(game)
            if guide:
                for g in guide:
                    print(g, file=stdout)
            else:
                results = self.search(game)
                if results:
                    for i, r in enumerate(results):
                        print("[{0}]: {1}".format(i, r), file=stdout)
                else:
                    print("Can't find any games.", file=stdout)
        else:
            print(self.on_help(), file=stdout)

    def on_help(self):
        return "Usage: ach <game>"


class Test(unittest.TestCase):
    def setUp(self):
        self.plugin = Plugin()

    def test_no_game(self):
        stdout = io.StringIO()
        self.plugin.on_command(None, {"args": [None, "DHKLfskldjslfjsdklasjhlsJKLfsdhalfsdlk"]}, None, stdout, None)
        self.assertEqual(len(stdout.getvalue().strip().splitlines()), 1)

    def test_search(self):
        stdout = io.StringIO()
        self.plugin.on_command(None, {"args": [None, "portal"]}, None, stdout, None)
        self.assertEqual(len(stdout.getvalue().strip().splitlines()), 2)

        stdout = io.StringIO()
        self.plugin.on_command(None, {"args": [None, "half life"]}, None, stdout, None)
        self.assertEqual(len(stdout.getvalue().strip().splitlines()), 1)

        stdout = io.StringIO()
        self.plugin.on_command(None, {"args": [None, "grand theft"]}, None, stdout, None)
        self.assertEqual(len(stdout.getvalue().strip().splitlines()), 3)

    def test_search_then_guide(self):
        self.plugin.on_command(None, {"args": [None, "portal"]}, None, io.StringIO(), None)
        stdout = io.StringIO()
        self.plugin.on_command(None, {"args": [None, "0"]}, None, stdout, None)
        self.assertEqual(len(stdout.getvalue().strip().splitlines()), 5)

    def test_guide(self):
        stdout = io.StringIO()
        self.plugin.on_command(None, {"args": [None, "Portal 2"]}, None, stdout, None)
        self.assertEqual(len(stdout.getvalue().strip().splitlines()), 5)

    def test_help(self):
        self.assertTrue(self.plugin.on_help())

    def test_no_args(self):
        stdout = io.StringIO()
        self.plugin.on_command(None, {"args": [None]}, stdout, stdout, None)
        self.assertEqual(self.plugin.on_help(), stdout.getvalue().strip())
