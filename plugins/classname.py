import lxml.html
import requests

class Plugin:
    def __call__(self, bot):
        bot.on_respond(r"class(( )?name)?", self.on_respond)
        bot.on_help("classname", self.on_help)

    def on_respond(self, bot, msg, reply):
        page = requests.get("http://classnamer.com/")
        tree = lxml.html.fromstring(page.text)
        classname = tree.cssselect("p#classname")[0].text_content()
        if classname:
            reply(classname)
        else:
            reply("No ClassName for you!")

    def on_help(self, bot, msg, reply):
        reply("Syntax: class[ ][name]")
