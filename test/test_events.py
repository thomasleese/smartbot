import os
import sys
import unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from smartbot import events


class TestEvents(unittest.TestCase):
    def test_empty(self):
        event = events.Event()
        self.assertEqual(len(event.trigger()), 0)

    def test_with_handlers(self):
        event = events.Event()
        event.register(lambda: None)
        self.assertEqual(len(event.trigger()), 1)

    def test_custom_comparator(self):
        comparator = lambda *args, **kwargs: False

        event = events.Event(default_comparator=comparator)
        event.register(lambda: None)
        self.assertEqual(len(event.trigger()), 0)

        event = events.Event()
        event.register(lambda: None)
        self.assertEqual(len(event.trigger(comparator=comparator)), 0)

    def test_default_comparator(self):
        event = events.Event()
        event.register(lambda *args, **kwargs: None, a=10)
        self.assertEqual(len(event.trigger()), 0)
        self.assertEqual(len(event.trigger(a=10)), 1)

    def test_decorator(self):
        event = events.Event()
        event()(lambda: None)
        self.assertEqual(len(event.trigger()), 1)
