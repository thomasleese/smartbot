import yaml

import smartbot.storage


class Storage(smartbot.storage.Storage):
    def __init__(self, filename="storage.yaml"):
        self.data = {}
        self.filename = filename

        try:
            with open(self.filename) as fd:
                self.data = yaml.load(fd.read())
        except FileNotFoundError:
            pass

        if not self.data:
            self.data = {}

    def __del__(self):
        self.commit()

    def commit(self):
        with open(self.filename, "w") as fd:
            fd.write(yaml.dump(self.data))

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
        self.commit()

    def __delitem__(self, key):
        del self.data[key]
