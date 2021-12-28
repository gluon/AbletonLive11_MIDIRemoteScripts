#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v2/control_surface/control/sysex.py
from __future__ import absolute_import, print_function, unicode_literals
from .control import Control, control_color

class ColorSysexControl(Control):

    class State(Control.State):
        color = control_color(u'DefaultButton.Disabled')

        def __init__(self, color = None, *a, **k):
            super(ColorSysexControl.State, self).__init__(*a, **k)
            if color is not None:
                self.color = color

        def set_control_element(self, control_element):
            super(ColorSysexControl.State, self).set_control_element(control_element)
            self._send_current_color()

        def update(self):
            super(ColorSysexControl.State, self).update()
            self._send_current_color()

        def _send_current_color(self):
            if self._control_element:
                self._control_element.set_light(self.color)

    def __init__(self, *a, **k):
        super(ColorSysexControl, self).__init__(extra_args=a, extra_kws=k)
