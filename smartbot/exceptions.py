class StopCommand(RuntimeError):
    """
    An exception that can be raise to halt the execution of a command, marking
    a user error somewhere.
    """
    pass


class StopCommandWithHelp(StopCommand):
    """
    A convinience StopCommandException which contains the plugin help as the
    message.
    """
    def __init__(self, plugin):
        super().__init__(plugin.on_help())
