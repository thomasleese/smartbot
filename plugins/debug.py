import time

class Plugin:
    def __call__(self, bot):
        bot.on_respond(r"ping$", lambda bot, msg, reply: reply("PONG"))
        bot.on_respond(r"echo (.*)$", lambda bot, msg, reply: reply(msg["match"].group(1)))
        bot.on_respond(r"time$", lambda bot, msg, reply: reply(time.time()))
        bot.on_help("debug", self.on_help)

    def on_help(self, bot, msg, reply):
        reply("Syntax: ping | echo <msg> | time")
