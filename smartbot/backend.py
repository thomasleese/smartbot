class Backend:
    def __init__(self):
        self.storage = None
        self.event_listeners = []

    def add_event_listener(self, name, callback):
        self.event_listeners.append((name, callback))

    def dispatch_event(self, name, *event):
        for listener in self.event_listeners:
            if listener[0] == name:
                listener[1](*event)
