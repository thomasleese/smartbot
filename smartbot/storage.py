import yaml

class Storage:
    def __getitem__(self, key):
        pass

    def __setitem__(self, key, value):
        pass

    def __delitem__(self, key):
        pass

class DictionaryStorage(Storage):
    def __init__(self):
        self.data = {}

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __delitem__(self, key):
        del self.data[key]

class YAML(DictionaryStorage):
    def __init__(self, filename="storage.yaml"):
        super().__init__()
        self.filename = filename

        try:
            with open(self.filename) as fd:
                self.data = yaml.load(fd.read())
        except FileNotFoundError:
            pass

    def __del__(self):
        with open(self.filename, "w") as fd:
            fd.write(yaml.dump(self.data))
