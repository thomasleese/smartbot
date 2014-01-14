characters = {
    "a": "ɐ",
    "A": "Ɐ",
    "b": "q",
    "c": "ɔ",
    "C": "Ɔ",
    "d": "p",
    "e": "ǝ",
    "E": "Ǝ",
    "f": "ɟ", 
    "g": "ƃ",
    "G": "Ƃ",
    "h": "ɥ",
    "H": "Ɥ",
    "i": "ı",
    "j": "ɾ",
    "J": "ɾ",
    "k": "ʞ",
    "K": "ʞ",
    "l": "ן",
    "L": "ן",
    "m": "ɯ",
    "M": "Ɯ",
    "n": "u",
    "r": "ɹ",
    "t": "ʇ",
    "T": "⊥",
    "v": "ʌ",
    "V": "Ʌ",
    "w": "ʍ",
    "W": "ʍ",
    "y": "ʎ",
    "Y": "ʎ",
    ".": "˙",
    "[": "]",
    "(": ")",
    "{": "}",
    "?": "¿",
    "!": "¡",
    "'": ",",
    "<": ">",
    "_": "‾",
    "\\": "/",
    ";": "؛",
    ",": "’",
    "‿": "⁀",
    "⁅": "⁆",
    "∴": "∵"
}

# for string.translate
real_characters = {}
for key, value in characters.items():
    real_characters[ord(key)] = ord(value)

class Plugin:
    def __call__(self, bot):
        bot.on_respond(r"flip (.+)$", self.on_respond)
        bot.on_help("flip", self.on_help)

    def on_respond(self, bot, msg, reply):
        reply(msg["match"][0][::-1].translate(real_characters))

    def on_help(self, bot, msg, reply):
        reply("Syntax: flip <text>")
