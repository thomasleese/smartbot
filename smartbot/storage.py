import yaml


class _Storage:
    def __getitem__(self, key):
        pass

    def __setitem__(self, key, value):
        pass

    def __delitem__(self, key):
        pass


class _DictionaryStorage(_Storage):
    def __init__(self):
        self.data = {}

    def __del__(self):
        self.commit()

    def commit(self):
        pass

    def get(self, key, default=None):
        return self.data.get(key, default)

    def setdefault(self, key, default=None):
        return self.data.setdefault(key, default)

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value
        self.commit()

    def __delitem__(self, key):
        del self.data[key]


class Memory(_DictionaryStorage):
    pass


class YAML(_DictionaryStorage):
    def __init__(self, filename="storage.yaml"):
        super().__init__()
        self.filename = filename

        try:
            with open(self.filename) as fd:
                self.data = yaml.load(fd.read())
        except FileNotFoundError:
            pass

        if not self.data:
            self.data = {}

    def commit(self):
        with open(self.filename, "w") as fd:
            fd.write(yaml.dump(self.data))
