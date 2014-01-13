import collections
import functools
import re

class Bot:
    def __init__(self, name):
        self.name = name
        self.storage = None
        self.backend = None
        self.plugins = []
        self.help_topics = []

    def set_storage(self, storage):
        self.storage = storage

    def set_backend(self, backend):
        self.backend = backend
        backend(self)

    def add_plugin(self, plugin):
        self.plugins.append(plugin)
        plugin(self)

    def set_plugins(self, plugins):
        self.plugins.clear()
        for plugin in plugins:
            self.add_plugin(plugin)

    def run(self):
        self.on_respond(r"help$", lambda bot, msg, reply: reply("Help about: {0}".format(", ".join(self.help_topics))))
        self.backend.run()

    # event handlers
    def on_ready(self, callback):
        try:
            self.backend.add_event_listener("ready", lambda: callback(self))
        except Exception as e:
            pass

    def on_join(self, callback):
        def on_join(msg):
            msg["is_me"] = msg["user"] == self.name
            try:
                callback(self, msg)
            except Exception as e:
                pass

        self.backend.add_event_listener("join", on_join)

    def on_hear(self, regex, callback):
        def on_message(msg):
            msg["match"] = re.findall(regex, msg["message"])
            if msg["match"]:
                reply = functools.partial(self.send, msg["reply_to"])
                try:
                    callback(self, msg, reply)
                except Exception as e:
                    reply(e)

        self.backend.add_event_listener("message", on_message)

    def on_respond(self, regex, callback):
        new_regex = r"^(?:" + self.name + r"[:,]?|!)\s*(?:" + regex + ")"
        self.on_hear(new_regex, callback)

    def on_help(self, name, callback):
        self.help_topics.append(name)
        self.on_respond("help " + name + "$", callback)

    # actions
    def join(self, channel):
        self.backend.join(channel)

    def send(self, target, message):
        self.backend.send(target, str(message))
