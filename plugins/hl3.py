import random

responses = [
    "Of course not.",
    "I doubt it.",
    "No - Valve can't count to 3.",
    "What do you think?",
    "YES!!! - only joking, of course it ain't out."
]

class Plugin:
    def __call__(self, bot):
        bot.on_respond(r"(is )?(hl3|half-life 3|half life 3|hl 3)( out( yet)?)?(\?)?", self.on_respond)
        bot.on_help("hl3", self.on_help)

    def on_respond(self, bot, msg, reply):
        reply(random.choice(responses))

    def on_help(self, bot, msg, reply):
        reply("Is Half-Life 3 out?")
        reply("Syntax: [is] hl3 [out [yet]]")
