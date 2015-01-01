import smartbot.storage


class Storage(smartbot.storage.Storage):
    def __init__(self):
        self.data = {}

    def get(self, key, default=None):
        return self.data.get(key, default)

    def setdefault(self, key, default=None):
        if key not in self.data:
            self[key] = default
        return self[key]

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __delitem__(self, key):
        del self.data[key]
