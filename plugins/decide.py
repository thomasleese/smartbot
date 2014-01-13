import random

class Plugin:
    def __call__(self, bot):
        bot.on_respond(r"decide \"(.*)\"$", self.on_respond_1)
        bot.on_respond(r"decide ([^\"]+)$", self.on_respond_2)
        bot.on_help("decide", self.on_help)

    def on_respond_1(self, bot, msg, reply):
        reply("I pick {0}.".format(random.choice(msg["match"][0].split("\" \""))))

    def on_respond_2(self, bot, msg, reply):
        reply("I pick {0}.".format(random.choice(msg["match"][0].split(" "))))

    def on_help(self, bot, msg, reply):
        reply("Syntax: decide \"option\" …")
