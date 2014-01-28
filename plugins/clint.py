import random
import requests
import time
import urllib.parse

quotes = [
    "I don't think it's nice you laughing.",
    "See my mule don't like people laughing, get's the crazy idea you're laughing at him.",
    "Get 3 coffins ready.",
    "When you hang a man you better look at him.",
    "Get off my lawn.",
    "I reckon so",
    "That's a fact.",
    "Do you feel lucky?",
    "Smith, and Wesson, and Me",
    "I know what you're thinking: did he fire Six shots, or only Five? Well to tell you the truth in all this excitment I've kinda lost track myself.",
    "Well do you, punk?",
    "Go Ahead, make my day.",
    "You still here?",
    "Man's got to know his limitations.",
    "Well I'm all broken up about that mans rights.",
    "If you want a guarentee, buy a toaster.",
    "With all due respect sir, you're begining to bore the hell out of me.",
    "What?",
    "What?",
    "What?",
    "Why what?",
    "I'm an American, I don't even know why the hell I'm here.",
    "Swell.",
    "Marvelous.",
    "Dying 'aint much of a living boy.",
    "'cause I ain't got nothing better to do, that's why.",
    "This isn't my town.",
    "You don't remember me, do you?",
]

class Plugin:
    def __call__(self, bot):
        bot.on_respond(r"(?:give me |gimme )?clint$", self.on_respond)
        bot.on_help("joke", self.on_help)

    def on_respond(self, bot, msg, reply):
        reply(random.choice(quotes))

    def on_help(self, bot, msg, reply):
        reply("Syntax: [give me] clint")
