from __future__ import absolute_import, print_function, unicode_literals
from _Framework.MixerComponent import MixerComponent as MixerComponentBase

class MixerComponent(MixerComponentBase):

    def set_volume_control(self, control):
        self._selected_strip.set_volume_control(control)