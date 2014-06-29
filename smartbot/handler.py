class Handler:
    def __init__(self, plugins):
        self.plugins = list(plugins)

    def find_plugin(self, name):
        for plugin in self.plugins:
            if name in plugin.names:
                return plugin

    def disable_plugin(self, name):
        plugin = self.find_plugin(name)
        if plugin is not None:
            self.plugins.remove(plugin)
