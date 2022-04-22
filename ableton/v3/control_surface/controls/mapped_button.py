# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v3/control_surface/controls/mapped_button.py
# Compiled at: 2022-01-27 16:28:17
# Size of source mod 2**32: 1495 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ...base import EventObject, listens, liveobj_valid, toggle_or_cycle_parameter_value
from . import ButtonControl as ButtonControlBase

class MappableButton(EventObject):

    def __init__(self, *a, **k):
        (super().__init__)(*a, **k)
        self._parameter = None

    def disconnect(self):
        self._parameter = None
        super().disconnect()

    @property
    def mapped_parameter(self):
        return self._parameter

    @mapped_parameter.setter
    def mapped_parameter(self, parameter):
        self._parameter = parameter if liveobj_valid(parameter) else None
        self.enabled = self._parameter is not None
        self._MappableButton__on_parameter_value_changed.subject = self._parameter
        self._MappableButton__on_parameter_value_changed()

    @listens('value')
    def __on_parameter_value_changed(self):
        self.is_on = liveobj_valid(self._parameter) and self._parameter.value


class MappedButtonControl(ButtonControlBase):

    class State(ButtonControlBase.State, MappableButton):

        def __init__(self, *a, **k):
            (super().__init__)(*a, **k)
            self.enabled = False

        def _call_listener(self, listener_name, *_):
            if listener_name == 'pressed':
                toggle_or_cycle_parameter_value(self.mapped_parameter)