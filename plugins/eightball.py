import random

responses = [
    "It is certain",
    "It is decidedly so",
    "Without a doubt",
    "Yes – definitely",
    "You may rely on it",
    "As I see it, yes",
    "Most likely",
    "Outlook good",
    "Signs point to yes",
    "Yes",
    "Reply hazy, try again",
    "Ask again later",
    "Better not tell you now",
    "Cannot predict now",
    "Concentrate and ask again",
    "Don't count on it",
    "My reply is no",
    "My sources say no",
    "Outlook not so good",
    "Very doubtful",
]

class Plugin:
    def __call__(self, bot):
        bot.on_respond(r"(magic )?(eightball|8ball)(.*)", self.on_respond)
        bot.on_help("eightball", self.on_help)

    def on_respond(self, bot, msg, reply):
        reply(random.choice(responses))

    def on_help(self, bot, msg, reply):
        reply("Syntax: [magic] eightball|8ball [<request>]")
