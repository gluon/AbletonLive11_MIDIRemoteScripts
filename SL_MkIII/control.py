# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\SL_MkIII\control.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 2135 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.control import ConfigurableTextDisplayControl as ConfigurableTextDisplayControlBase
from ableton.v2.control_surface.control import Control
from ableton.v2.control_surface.control import TextDisplayControl as TextDisplayControlBase

class BinaryControl(Control):

    class State(Control.State):
        ON_VALUE = 1
        OFF_VALUE = 0

        def __init__(self, *a, **k):
            (super(BinaryControl.State, self).__init__)(*a, **k)
            self._is_on = False

        @property
        def is_on(self):
            return self._is_on

        @is_on.setter
        def is_on(self, value):
            if self._is_on != value:
                self._is_on = value
                self._send_current_value()

        def set_control_element(self, control_element):
            super(BinaryControl.State, self).set_control_element(control_element)
            self._send_current_value()

        def update(self):
            super(BinaryControl.State, self).update()
            self._send_current_value()

        def _send_current_value(self):
            if self._control_element:
                self._control_element.send_value(self.ON_VALUE if self.is_on else self.OFF_VALUE)


class TextDisplayControl(TextDisplayControlBase):

    class State(TextDisplayControlBase.State):

        def set_control_element(self, control_element):
            set_control_element(self, control_element)


class ConfigurableTextDisplayControl(ConfigurableTextDisplayControlBase):

    class State(ConfigurableTextDisplayControlBase.State):

        def set_control_element(self, control_element):
            set_control_element(self, control_element)


def set_control_element(self, control_element):
    Control.State.set_control_element(self, control_element)
    if control_element:
        control_element.set_data_sources(self._data_sources)