from smartbot.formatting import *


class Plugin:
    def on_command(self, bot, msg, stdin, stdout, reply):
        styles = [x for x in dir(Style) if not callable(x) and not x.startswith("__")]
        colours = [x for x in dir(Colour) if not callable(x) and not x.startswith("__")]

        for style in styles:
            print(bot.format(style, getattr(Style, style)), end=",", file=stdout)

        print(file=stdout)

        for colour in colours:
            print(bot.format(colour, getattr(Colour, colour)), end=",", file=stdout)

    def on_help(self):
        return "Usage: debug"
