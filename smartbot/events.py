"""
The events subsystem is a fundamental part of SmartBot that governs a lot of
underlying logic.

An event is, in simple terms, a wrapper for a list of functions which can be
called, with some optional arguments, when an event happens.

You can control which functions get called by using a comparator, which is
just a function with three arguments, the event handler, the positional
arguments and the keyword arguments. The default comparator simply checks that
these are the same.
"""
import collections


"""
An event handler is a function which is registered with some event position
arguments and keyword arguments. This could have been implemented as function
attributes, however, a solution with encapsulation has been used to allow
the same function to be registered multiple times.
"""
Handler = collections.namedtuple('Handler', ['args', 'kwargs', 'function'])


"""
The default comparator checks that the handler args and kwargs are the samer as
the event ones.
"""
DEFAULT_COMPARATOR = lambda handler, args, kwargs: handler.args == args and \
                                                   handler.kwargs == kwargs


class Event:
    """
    An event holds a list of handlers and a default comparator. By registering
    a function (with some event args and kwargs), it can then be called later
    when an event gets triggered.

    If the default comparator is not passed, the module-level default
    comparator is used which is described above.
    """
    def __init__(self, default_comparator=None):
        self.handlers = []
        self.default_comparator = default_comparator or DEFAULT_COMPARATOR

    def __call__(self, *args, **kwargs):
        """
        Convinence method which allows an event handler to be registed by
        calling the event as a decorator.
        """
        def decorator(f):
            self.register(f)
            return f
        return decorator

    def register(self, function, *args, **kwargs):
        """Register a function as an event handler."""
        self.handlers.append(Handler(args, kwargs, function))

    def trigger(self, *args, comparator=None, **kwargs):
        """
        Trigger an event, causing all approriate event handlers to be executed.

        The arguments are passed directly to the function, and are also used by
        the comparator to check whether the function should be called in the
        first place.

        This function returns a list of handlers which were called. Whilst this
        is mainly used for unit-testing, it can be useful for users.
        """
        comparator = comparator or self.default_comparator
        called_handlers = []
        for handler in self.handlers:
            if comparator(handler, args, kwargs):
                handler.function(*args, **kwargs)
                called_handlers.append(handler)
        return called_handlers
