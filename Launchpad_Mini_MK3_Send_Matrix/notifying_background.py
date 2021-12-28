#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Launchpad_Mini_MK3/notifying_background.py
from __future__ import absolute_import, print_function, unicode_literals
from functools import partial
from ableton.v2.control_surface.components import BackgroundComponent

class NotifyingBackgroundComponent(BackgroundComponent):
    __events__ = (u'value',)

    def register_slot(self, control, *a):
        super(BackgroundComponent, self).register_slot(control, partial(self.__on_control_value, control), u'value')

    def __on_control_value(self, control, value):
        self.notify_value(control, value)
