#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Akai_Force_MPC/background.py
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.components import BackgroundComponent

class LightingBackgroundComponent(BackgroundComponent):

    def _clear_control(self, name, control):
        super(LightingBackgroundComponent, self)._clear_control(name, control)
        if control:
            control.set_light(u'Background.On')
