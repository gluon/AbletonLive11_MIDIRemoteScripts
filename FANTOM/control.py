# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.0 (v3.7.0:1bf9cc5093, Jun 26 2018, 23:26:24) 
# [Clang 6.0 (clang-600.0.57)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/FANTOM/control.py
# Compiled at: 2021-08-05 15:33:19
# Size of source mod 2**32: 1018 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.control import Control

class DisplayControl(Control):

    class State(Control.State):

        def __init__(self, *a, **k):
            (super(DisplayControl.State, self).__init__)(*a, **k)
            self._data = ''

        @property
        def data(self):
            return self._data

        @data.setter
        def data(self, data):
            self._data = data
            self._send_current_data()

        def set_control_element(self, control_element):
            super(DisplayControl.State, self).set_control_element(control_element)
            self._send_current_data()

        def update(self):
            super(DisplayControl.State, self).update()
            self._send_current_data()

        def _send_current_data(self):
            if self._control_element:
                self._control_element.display_data(self._data)