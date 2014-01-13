import base64

class Plugin:
    def __call__(self, bot):
        bot.on_respond(r"(?:base64|b64) encode (.*)$", self.on_b64_encode)
        bot.on_respond(r"(?:base64|b64) decode (.*)$", self.on_b64_decode)
        bot.on_respond(r"(?:base32|b32) encode (.*)$", self.on_b32_encode)
        bot.on_respond(r"(?:base32|b32) decode (.*)$", self.on_b32_decode)
        bot.on_respond(r"(?:base16|b16) encode (.*)$", self.on_b16_encode)
        bot.on_respond(r"(?:base16|b16) decode (.*)$", self.on_b16_decode)
        bot.on_help("encoding", self.on_help)

    def on_b64_encode(self, bot, msg, reply):
        reply(str(base64.b64encode(bytes(msg["match"][0], "utf-8")), "utf-8"))

    def on_b64_decode(self, bot, msg, reply):
        reply(str(base64.b64decode(bytes(msg["match"][0], "utf-8")), "utf-8"))

    def on_b32_encode(self, bot, msg, reply):
        reply(str(base64.b32encode(bytes(msg["match"][0], "utf-8")), "utf-8"))

    def on_b32_decode(self, bot, msg, reply):
        reply(str(base64.b32decode(bytes(msg["match"][0], "utf-8")), "utf-8"))

    def on_b16_encode(self, bot, msg, reply):
        reply(str(base64.b16encode(bytes(msg["match"][0], "utf-8")), "utf-8"))

    def on_b16_decode(self, bot, msg, reply):
        reply(str(base64.b16decode(bytes(msg["match"][0], "utf-8")), "utf-8"))

    def on_help(self, bot, msg, reply):
        reply("Syntax: base64|b64|base32|b32|base16|b16 encode|decode <text>")
