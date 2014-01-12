class Plugin:
    def __call__(self, bot):
        bot.on_hear(r"bring( your)? daughter( to)? work( day)?", self.on_respond_1)
        bot.on_hear(r"(vital )?organ donor", self.on_respond_2)
        bot.on_hear(r"(the )?cake is( a)? lie", self.on_respond_3)
        bot.on_hear(r"(weighted )?companion cube", self.on_respond_4)
        bot.on_help("glados", self.on_help)

    def on_respond_1(self, bot, msg, reply):
        reply("Remember, the Aperture Science 'Bring Your Daughter to Work Day' is the perfect time to have her tested.")

    def on_respond_2(self, bot, msg, reply):
        reply("Did you know you can donate one or all of your vital organs to the Aperture Science Self-Esteem Fund for Girls? It's true!")

    def on_respond_3(self, bot, msg, reply):
        reply("The Enrichment Center is required to remind you that you will be baked, and then there will be cake.")

    def on_respond_4(self, bot, msg, reply):
        reply("We at the Enrichment Center would like to remind you that the Weighted Companion Cube will never threaten to stab you, and in fact, cannot speak.")

    def on_help(self, bot, msg, reply):
        reply("She's listening…")
