import sys
import re

from textblob import TextBlob


class Plugin:
    matcher = re.compile(r'translate (?:from ([^ ]+) )?(?:to ([^ ]+) )?(.*)') 

    def on_command(self, bot, msg, stdin, stdout, reply):
        match = self.matcher.match(msg["message"])
        if not match:
            return
        from_lang = match.group(1) or None  # let autodetect decide
        to_lang   = match.group(2) or "en"
        message   = TextBlob(match.group(3))
        try:
            translated = message.translate(from_lang=from_lang, to=to_lang)
        except:
            return
        print(translated, file=stdout)
