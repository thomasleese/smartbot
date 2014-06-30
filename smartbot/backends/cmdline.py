import smartbot
from ..formatting import *


class Backend(smartbot.Backend):
    def __init__(self):
        super().__init__()

    def run(self, name):
        self.on_connect.trigger()
        self.on_ready.trigger()

        while True:
            line = input("> ").strip()
            self.on_message.trigger({
                "sender": "stdin", "target": "stdout",
                "message": line, "reply_to": "stdin"
            })

        self.on_disconnect.trigger()

    def join(self, channel):
        print("Joining", channel)

    def send(self, target, message):
        print(target + ":", message)

    def format(self, text, properties):
        values = []

        if Style.bold in properties:
            values.append("1")
        if Style.italic in properties:
            values.append("3")
        if Style.underline in properties:
            values.append("4")
        if Colour.fg_white in properties:
            values.append("37")
        if Colour.fg_black in properties:
            values.append("30")
        if Colour.fg_blue in properties:
            values.append("34")
        if Colour.fg_green in properties:
            values.append("32")
        if Colour.fg_red in properties:
            values.append("31")
        if Colour.fg_purple in properties:
            values.append("35")
        if Colour.fg_yellow in properties:
            values.append("33")
        if Colour.fg_light_cyan in properties:
            values.append("36")
        if Colour.bg_white in properties:
            values.append("47")
        if Colour.bg_black in properties:
            values.append("40")
        if Colour.bg_blue in properties:
            values.append("44")
        if Colour.bg_green in properties:
            values.append("42")
        if Colour.bg_red in properties:
            values.append("41")
        if Colour.bg_purple in properties:
            values.append("45")
        if Colour.bg_yellow in properties:
            values.append("43")
        if Colour.bg_light_cyan in properties:
            values.append("46")

        return "\033[{}m{}\033[0m".format(";".join(values), text)
