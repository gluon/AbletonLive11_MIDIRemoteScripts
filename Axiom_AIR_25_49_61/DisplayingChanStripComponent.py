from __future__ import absolute_import, print_function, unicode_literals
import _Framework.ButtonElement as ButtonElement
import _Framework.ChannelStripComponent as ChannelStripComponent
from .consts import *

class DisplayingChanStripComponent(ChannelStripComponent):

    def __init__(self):
        ChannelStripComponent.__init__(self)
        self._name_display = None
        self._value_display = None

    def disconnect(self):
        ChannelStripComponent.disconnect(self)
        self._name_display = None
        self._value_display = None

    def set_name_display(self, name_display):
        self._name_display = name_display

    def set_value_display(self, value_display):
        self._value_display = value_display

    def set_arm_button(self, button):
        if button != self._arm_button:
            if self._arm_button != None:
                self._arm_button.remove_value_listener(self._arm_value)
                self._arm_button.reset()
            self._arm_pressed = False
            self._arm_button = button
            if self._arm_button != None:
                self._arm_button.add_value_listener(self._arm_value)
            self.update()

    def _on_mute_changed(self):
        if self._mute_button != None:
            if self._track != None and self._track != self.song().master_track:
                self._mute_button.set_on_off_values(AMB_FULL, AMB_LOW)
            else:
                self._mute_button.set_on_off_values(AMB_LOW, LED_OFF)
        ChannelStripComponent._on_mute_changed(self)

    def _on_solo_changed(self):
        if self._solo_button != None:
            if self._track != None and self._track != self.song().master_track:
                self._solo_button.set_on_off_values(AMB_FULL, AMB_LOW)
            else:
                self._solo_button.set_on_off_values(AMB_LOW, LED_OFF)
        ChannelStripComponent._on_solo_changed(self)

    def _on_arm_changed(self):
        if self._arm_button != None:
            if self._track != None and self._track in self.song().tracks:
                self._arm_button.set_on_off_values(RED_FULL, RED_LOW)
            else:
                self._arm_button.set_on_off_values(RED_LOW, LED_OFF)
        ChannelStripComponent._on_arm_changed(self)

    def _mute_value(self, value):
        ChannelStripComponent._mute_value(self, value)
        if self._track != None:
            if self._track != self.song().master_track:
                if self._name_display != None:
                    if self._value_display != None:
                        if value != 0:
                            self._name_display.display_message('Mute :')
                            self._value_display.send_midi(DISPLAY_WORD_ON) if self._track.mute else self._value_display.send_midi(DISPLAY_WORD_OFF)

    def _solo_value(self, value):
        ChannelStripComponent._solo_value(self, value)
        if self._track != None:
            if self._track != self.song().master_track:
                if self._name_display != None:
                    if self._value_display != None:
                        if value != 0:
                            self._name_display.display_message('Solo :')
                            self._value_display.send_midi(DISPLAY_WORD_ON) if self._track.solo else self._value_display.send_midi(DISPLAY_WORD_OFF)

    def _arm_value(self, value):
        ChannelStripComponent._arm_value(self, value)
        if self._track != None:
            if self._track != self.song().master_track:
                if self._name_display != None:
                    if self._value_display != None:
                        if self._track not in self.song().return_tracks:
                            if value != 0:
                                self._name_display.display_message('Arm :')
                                self._value_display.send_midi(DISPLAY_WORD_ON) if self._track.arm else self._value_display.send_midi(DISPLAY_WORD_OFF)