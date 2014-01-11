import collections

ReadyEvent = collections.namedtuple("ReadyEvent", [ "bot" ])
JoinEvent = collections.namedtuple("JoinEvent", [ "bot", "user", "channel", "is_me" ])

class Bot:
    def __init__(self):
        self.storage = None
        self.backend = None
        self.plugins = [ ]

    def set_storage(self, storage):
        self.storage = storage

    def set_backend(self, backend):
        self.backend = backend
        self.backend.storage = self.storage

    def add_plugin(self, plugin):
        self.plugins.append(plugin)
        plugin(self)

    def set_plugins(self, plugins):
        self.plugins.clear()
        for plugin in plugins:
            self.add_plugin(plugin)

    def run(self):
        self.backend.run()

    def join(self, channel):
        self.backend.join(channel)

    def send(self, target, message):
        self.backend.send(target, message)

    def on_ready(self, callback):
        self.backend.add_event_listener("ready", lambda: callback(ReadyEvent(self)))

    def on_join(self, callback):
        self.backend.add_event_listener("join", lambda *args: callback(JoinEvent(self, *args)))
