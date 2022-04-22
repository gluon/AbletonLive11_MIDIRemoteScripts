# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/_Framework/Signal.py
# Compiled at: 2022-01-27 16:28:16
# Size of source mod 2**32: 3054 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import object
from functools import partial
from .Util import find_if, nop

def default_combiner(results):
    for _ in results:
        pass


class Slot(object):

    def __init__(self, callback=None, *a, **k):
        (super(Slot, self).__init__)(*a, **k)
        self.callback = callback

    def __call__(self, *a, **k):
        return (self.callback)(*a, **k)

    def __eq__(self, other):
        return id(self) == id(other) or self.callback == other


class IdentifyingSlot(Slot):

    def __init__(self, sender=None, *a, **k):
        (super(IdentifyingSlot, self).__init__)(*a, **k)
        self.sender = sender

    def __call__(self, *a, **k):
        (self.callback)(*a + (self.sender,), **k)


class Signal(object):

    def __init__(self, combiner=default_combiner, sender=None, *a, **k):
        (super(Signal, self).__init__)(*a, **k)
        self._slots = []
        self._combiner = combiner

    def connect(self, slot, in_front=False, sender=None):
        if slot not in self._slots:
            slot = IdentifyingSlot(sender, slot) if sender is not None else Slot(slot)
            if in_front:
                self._slots.insert(0, slot)
            else:
                self._slots.append(slot)
        else:
            slot = find_if(lambda x: x == slot, self._slots)
        return slot

    def disconnect(self, slot):
        if slot in self._slots:
            self._slots.remove(slot)

    def disconnect_all(self):
        self._slots = []

    @property
    def count(self):
        return len(self._slots)

    def is_connected(self, slot):
        return slot in self._slots

    def __call__(self, *a, **k):
        return self._combiner(_slot_notification_generator(self._slots, a, k))


def _slot_notification_generator(slots, args, kws):
    for slot in slots:
        (yield slot(*args, **kws))


def short_circuit_combiner(slot_results):
    return find_if(nop, slot_results)


short_circuit_signal = partial(Signal, short_circuit_combiner)