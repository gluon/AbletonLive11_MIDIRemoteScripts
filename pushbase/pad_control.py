# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\pushbase\pad_control.py
# Compiled at: 2022-11-28 08:01:32
# Size of source mod 2**32: 1175 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.control import PlayableControl

class PadControl(PlayableControl):

    class State(PlayableControl.State):

        def __init__(self, sensitivity_profile=None, *a, **k):
            (super(PadControl.State, self).__init__)(*a, **k)
            self._sensitivity_profile = sensitivity_profile

        def _get_sensitivity_profile(self):
            return self._sensitivity_profile

        def _set_sensitivity_profile(self, value):
            self._sensitivity_profile = value
            self._update_sensitivity()

        sensitivity_profile = property(_get_sensitivity_profile, _set_sensitivity_profile)

        def set_control_element(self, control_element):
            super(PadControl.State, self).set_control_element(control_element)
            self._update_sensitivity()

        def _update_sensitivity(self):
            if self._control_element:
                if self._sensitivity_profile:
                    self._control_element.sensitivity_profile = self._sensitivity_profile