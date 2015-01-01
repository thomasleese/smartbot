import smartbot.plugin
from smartbot.utils.web import sprunge
from smartbot.exceptions import StopCommand


class Plugin(smartbot.plugin.Plugin):
    """Upload piped content to sprunge."""
    names = ["sprunge"]

    def on_command(self, msg, stdin, stdout, reply):
        contents = stdin.read().strip()
        if contents:
            print(sprunge(contents), file=stdout)
        else:
            raise StopCommand("Expected input on stdin.")
