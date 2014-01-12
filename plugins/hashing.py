import hashlib

class Plugin:
    def __call__(self, bot):
        bot.on_respond(r"(md5|sha|sha1|sha256|sha512) (.*)$", self.on_respond)
        bot.on_help("hashing", self.on_help)

    def on_respond(self, bot, msg, reply):
        hash = hashlib.new(msg["match"].group(1))
        hash.update(bytes(msg["match"].group(2), "utf-8"))
        reply(hash.hexdigest())

    def on_help(self, bot, msg, reply):
        reply("Syntax: md5|sha|sha1|sha256|sha512 <text>")
