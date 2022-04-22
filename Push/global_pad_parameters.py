# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Push/global_pad_parameters.py
# Compiled at: 2022-01-27 16:28:16
# Size of source mod 2**32: 1348 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface import Component
from . import sysex

class GlobalPadParameters(Component):

    def __init__(self, aftertouch_threshold=0, *a, **k):
        (super(GlobalPadParameters, self).__init__)(*a, **k)
        self._pad_parameter_element = None
        self._aftertouch_threshold = aftertouch_threshold

    def _get_aftertouch_threshold(self):
        return self._aftertouch_threshold

    def _set_aftertouch_threshold(self, value):
        self._aftertouch_threshold = value
        self._update_pad_parameter_element()

    aftertouch_threshold = property(_get_aftertouch_threshold, _set_aftertouch_threshold)

    def set_pad_parameter(self, element):
        self._pad_parameter_element = element
        self._update_pad_parameter_element()

    def _update_pad_parameter_element(self):
        if self._pad_parameter_element:
            self._pad_parameter_element.send_value(sysex.make_pad_parameter_message(aftertouch_threshold=(self._aftertouch_threshold)))

    def update(self):
        super(GlobalPadParameters, self).update()
        if self.is_enabled():
            self._update_pad_parameter_element()