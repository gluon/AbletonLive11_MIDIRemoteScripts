# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v3/control_surface/components/background.py
# Compiled at: 2022-01-28 05:06:24
# Size of source mod 2**32: 1598 bytes
from __future__ import absolute_import, print_function, unicode_literals
from future.utils import itervalues
from functools import partial
from ...base import nop
from .. import Component

class BackgroundComponent(Component):

    def __init__(self, name='Background', *a, **k):
        (super().__init__)(a, name=name, **k)
        self._control_slots = {}
        self._control_map = {}

    def __getattr__(self, name):
        if len(name) > 4:
            if name[:4] == 'set_':
                return partial(self._clear_control, name[4:])
        raise AttributeError(name)

    def _clear_control(self, name, control):
        slot = self._control_slots.get(name, None)
        if slot:
            del self._control_slots[name]
            self.disconnect_disconnectable(slot)
        if control:
            control.reset()
            self._control_map[name] = control
            self._control_slots[name] = self.register_slot(control, nop, 'value')
        elif name in self._control_map:
            del self._control_map[name]

    def update(self):
        super().update()
        if self.is_enabled():
            for control in itervalues(self._control_map):
                control.reset()