import lxml.html
import requests

class Plugin:
    def __call__(self, bot):
        bot.on_respond(r"(?:xbox )?ach(?:ievements)? (.*)", self.on_respond)
        bot.on_help("xboxachievements", self.on_help)

    def on_respond(self, bot, msg, reply):
        game_id = msg["match"][0].lower().replace(" ", "-")
        url = "http://www.xboxachievements.com/game/{0}/guide/".format(game_id)
        page = requests.get(url)
        tree = lxml.html.fromstring(page.text)
        elements = tree.cssselect("#col_l .bl_la_main_guide .showhide p")
        if not elements:
            elements = tree.cssselect("#col_l .bl_la_main_guide .showhide div div")

        if elements:
            html = lxml.html.tostring(elements[0])
            lines = html.decode("utf-8").split("<br>")
            for line in lines[1:6]:
                span = lxml.html.fragment_fromstring("<span>{0}</span>".format(line))
                reply(span.text_content().strip()[1:])
        else:
            reply("Can't find the game.")

    def on_help(self, bot, msg, reply):
        reply("Display information from http://www.xboxachievements.com/.")
        reply("Syntax: [xbox] ach[ievements] <game>")
