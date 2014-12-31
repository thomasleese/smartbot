import random
import time

import smartbot
from smartbot import utils
from smartbot.exceptions import *
from smartbot.formatting import *


GOOD_JOKES = [
    "I want to write a mystery novel… or do I?",
    "I saw a documentary on how ships are kept together; it was riveting.",
    "There are two types of people I hate… racists and Norwegians.",
    "A cure for agoraphobics is just around the corner.",
    "In school I wanted to join the debating team… but someone talked me out of it.",
    "I went to my local library yesterday, and asked: “Have you got a book on handling rejection without killing?”",
    "My wife and I decided we don’t want children; if someone wants them, we’ll drop them off tomorrow.",
    "I was raised by my father; my mother left before I was born.",
    "I went to a therapy group to help me cope with loneliness, but no one else turned up.",
    "What is the big deal about trainspotters… I counted 27 of the losers today.",
    "Regarding my family, I’m the youngest of three; my parents are both older.",
    "I read today that 10 out of 2 people are dyslectic.",
    "There's a fine line between hyphenated words…",
    "I was sitting in traffic the other day… and I got run over.",
    "My uncle was crushed by a piano; his funeral was very low key.",
    "Did I already do my déjà vu joke?",
    "People say I have the legs of a dancer. But until they find the rest of the body, the cops have nothing on me, man!",
    "Have you ever imagined a world with no hypothetical situations?",
    "When I was a child my father attacked me with cameras; I still have flashbacks.",
    "I don’t think I got the job at Microsoft… they didn’t respond to my telegram.",
    "I'm not a competitive person… I'll be the first to admit it.",
    "I quit my job at the helium gas factory. I didn't like being spoken to in that voice. ",
    "I went to the zoo the other day, there was only one dog in it, it was a shitzu.",
    "I'm on a whiskey diet. I've lost three days already. ",
    "My mother-in-law fell down a wishing well, I was amazed, I never knew they worked. ",
    "I saw this bloke chatting up a cheetah; I thought, “He's trying to pull a fast one”.",
    "Slept like a log last night........ Woke up in the fireplace. ",
    "I tried water polo but my horse drowned. ",
    "Keep Britain Tidy – chop off Norfolk and Cornwall!",
    "Overall, I'd say my career as a photographer has been a bit of a blur.",
    "Militant feminists, I take my hat off to them, they don’t like that.",
    "I was mugged by a man on crutches, wearing camouflage. Ha ha, I thought, you can hide but you can't run.",
    "Michelle McMannus lost four stone - that’s like throwing a deck chair off the Titanic",
    "I’m a postmodern vegetarian. I eat meat ironically.",
    "I am not a vegetarian because I love animals. I am a vegetarian because I hate plants.",
    "I never forget a face, but in your case I’d be glad to make an exception.",
    "My wife sent her photograph to the Lonely Hearts Club. They sent it back saying they weren't that lonely.",
    "If you want to know what God thinks of money, just look at the people he gave it to.",
    "I don't like country music, but I don't mean to denigrate those who do. And for the people who like country music, denigrate means 'put down’.",
    "I wonder if illiterate people get the full effect of alphabet soup.",
    "It’s always funny until someone gets hurt. Then it’s just hilarious.",
    "Ever notice how people who believe in creationism look really un-evolved?",
    "I sleep eight hours a day and at least ten at night.",
]


class Plugin(smartbot.Plugin):
    """Tell a joke."""
    names = ["joke", "'joke'"]

    def _get_good_joke(self):
        return [random.choice(GOOD_JOKES)]

    def _get_bad_joke(self):
        url = "http://jokels.com/random_joke"
        session = utils.web.requests_session()
        res = session.get(url).json()
        return [res["joke"]["question"], res["joke"]["answer"]]

    def on_respond(self, msg, reply):
        if msg["message"].startswith("'joke'"):
            self.on_respond_bad(msg, reply)
        elif msg["message"].startswith("joke"):
            self.on_respond_good(msg, reply)

    def on_respond_good(self, msg, reply):
        for line in self._get_good_joke():
            reply(line)
            time.sleep(1)

    def on_respond_bad(self, msg, reply):
        for line in self._get_bad_joke():
            reply(line)
            time.sleep(1)

    def on_help(self):
        return "{}|{}".format(
            self.bot.format("joke", Style.bold),
            self.bot.format("'joke'", Style.bold)
        )
