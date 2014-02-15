import random
import shlex


class Plugin:
    def __call__(self, bot):
        bot.on_respond(r"decide (.*)$", self.on_respond)
        bot.on_help("decide", self.on_help)

    def on_respond(self, bot, msg, reply):
        choices = shlex.split(msg["match"][0])
        reply("I pick {0}.".format(random.choice(choices)))

    def on_help(self, bot, msg, reply):
        reply("Syntax: decide 'option' …")
