import argparse

from textblob import TextBlob

import smartbot.plugin
from smartbot.formatting import Style


class Plugin(smartbot.plugin.Plugin):
    """Perform a Google translation."""
    names = ["translate"]

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-from","--from-language", default=None, nargs="?")  # let autodetect decide
    parser.add_argument("-to"  ,"--to-language",   default="en", nargs="?")
    parser.add_argument("message", nargs="*")

    def on_command(self, msg, stdin, stdout, reply):
        # pre-process args
        # this might mess up if "from" or "to" is left out and
        # the message contains "from" or "to"
        self._push_character(msg["args"], "from", "-", 1)
        self._push_character(msg["args"], "to",   "-", 1)

        try:
            args = self.parser.parse_args(msg["args"][1:])
        except (argparse.ArgumentError, SystemExit):
            return

        # get message from the appropriate place
        if args.message:
            message = " ".join(args.message)
        else:
            message = stdin.read().strip()

        # translate
        from_lang = args.from_language
        to_lang   = args.to_language
        message   = TextBlob(message)
        try:
            translated = message.translate(from_lang=from_lang, to=to_lang)
        except:
            pass
        else:
            print(translated, file=stdout)

    def on_help(self):
        return "{} [from {}] [to {}] [{}]".format(
            super().on_help(),
            self.bot.format("language", Style.underline),
            self.bot.format("language", Style.underline),
            self.bot.format("text", Style.underline)
        )

    @staticmethod
    def _push_character(args, target, character, n):
        try:
            i = args.index(target)
            args[i] = (character * n) + args[i]
        except ValueError:
            pass
