#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ATOM/lighting.py
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface import Component
from ableton.v2.control_surface.control import ButtonControl

class LightingComponent(Component):
    shift_button = ButtonControl(color=u'DefaultButton.Off', pressed_color=u'DefaultButton.On')
    zoom_button = ButtonControl(color=u'DefaultButton.Off', pressed_color=u'DefaultButton.On')
