"""
observer
********

:Author: tobijjah
:Date: 02.06.19
"""


class Signal:
    def __init__(self, name):
        self.name = name

        self._handlers = list()

    def fire(self, *args, **kwargs):
        for handler in self._handlers:
            handler(*args, **kwargs)

    def connect(self, handler):
        if handler not in self._handlers:
            self._handlers.append(handler)

    def remove(self, handler):
        if handler in self._handlers:
            self._handlers.remove(handler)
