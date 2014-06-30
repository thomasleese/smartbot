from .events import Event

class Backend:
    def __init__(self):
        self.storage = None
        self.event_listeners = []

        self.on_connect = Event()
        self.on_disconnect = Event()
        self.on_ready = Event()
        self.on_join = Event()
        self.on_message = Event()
