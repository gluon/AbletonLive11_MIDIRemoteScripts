from __future__ import absolute_import, print_function, unicode_literals
import _Framework.MixerComponent as MixerComponent
from .SelectChanStripComponent import SelectChanStripComponent

class SpecialMixerComponent(MixerComponent):

    def _create_strip(self):
        return SelectChanStripComponent()

    def set_bank_up_button(self, button):
        self.set_bank_buttons(button, self._bank_down_button)

    def set_bank_down_button(self, button):
        self.set_bank_buttons(self._bank_up_button, button)