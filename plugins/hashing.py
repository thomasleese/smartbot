import hashlib


class Plugin:
    def __call__(self, bot):
        bot.on_respond(r"(md5|sha|sha1|sha256|sha512) (.*)$", self.on_respond)
        bot.on_help("hashing", self.on_help)

    def on_respond(self, bot, msg, reply):
        match = msg["match"][0]
        h = hashlib.new(match[0])
        h.update(bytes(match[1], "utf-8"))
        reply(h.hexdigest())

    def on_help(self, bot, msg, reply):
        reply("Syntax: md5|sha|sha1|sha256|sha512 <text>")
