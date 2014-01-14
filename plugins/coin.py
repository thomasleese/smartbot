import random

class Plugin:
    def __call__(self, bot):
        bot.on_respond(r"(throw|flip|toss)( a)? coin", self.on_respond)
        bot.on_help("coin", self.on_help)

    def on_respond(self, bot, msg, reply):
        reply(random.choice([ "Heads", "Tails" ]))

    def on_help(self, bot, msg, reply):
        reply("Throws coins.")
        reply("Syntax: throw|flip|toss [a] coin")
