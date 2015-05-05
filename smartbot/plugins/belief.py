import random
import time
import threading

import smartbot.plugin


class Plugin(smartbot.plugin.Plugin):
    """You better believe it!"""
    names = ['belief']

    def __init__(self, believers):
        for believer in believers:
            args = (believer['target'], believer['person'],
                    believer['minimum'], believer['maximum'])
            threading.Thread(target=self.reminder_thread, args=args).start()

    def reminder_thread(self, target, person, minimum, maximum):
        while True:
            delay = random.randint(minimum, maximum)
            time.sleep(delay)
            msg = 'Oi, {}, you better believe it!'.format(person)
            self.bot.send(target, msg)

    def on_help(self):
        return "You better believe it!"
