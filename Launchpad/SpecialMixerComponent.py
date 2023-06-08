from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
import Live
import _Framework.ButtonElement as ButtonElement
import _Framework.MixerComponent as MixerComponent
from .DefChannelStripComponent import DefChannelStripComponent

class SpecialMixerComponent(MixerComponent):

    def __init__(self, num_tracks, num_returns=0):
        MixerComponent.__init__(self, num_tracks, num_returns)
        self._unarm_all_button = None
        self._unsolo_all_button = None
        self._unmute_all_button = None

    def disconnect(self):
        if self._unarm_all_button != None:
            self._unarm_all_button.remove_value_listener(self._unarm_all_value)
            self._unarm_all_button = None
        if self._unsolo_all_button != None:
            self._unsolo_all_button.remove_value_listener(self._unsolo_all_value)
            self._unsolo_all_button = None
        if self._unmute_all_button != None:
            self._unmute_all_button.remove_value_listener(self._unmute_all_value)
            self._unmute_all_button = None
        MixerComponent.disconnect(self)

    def set_global_buttons(self, unarm_all, unsolo_all, unmute_all):
        if self._unarm_all_button != None:
            self._unarm_all_button.remove_value_listener(self._unarm_all_value)
        self._unarm_all_button = unarm_all
        if self._unarm_all_button != None:
            self._unarm_all_button.add_value_listener(self._unarm_all_value)
            self._unarm_all_button.turn_off()
        if self._unsolo_all_button != None:
            self._unsolo_all_button.remove_value_listener(self._unsolo_all_value)
        self._unsolo_all_button = unsolo_all
        if self._unsolo_all_button != None:
            self._unsolo_all_button.add_value_listener(self._unsolo_all_value)
            self._unsolo_all_button.turn_off()
        if self._unmute_all_button != None:
            self._unmute_all_button.remove_value_listener(self._unmute_all_value)
        self._unmute_all_button = unmute_all
        if self._unmute_all_button != None:
            self._unmute_all_button.add_value_listener(self._unmute_all_value)
            self._unmute_all_button.turn_off()

    def _create_strip(self):
        return DefChannelStripComponent()

    def _unarm_all_value(self, value):
        if not (value != 0 or self._unarm_all_button.is_momentary()):
            for track in self.song().tracks:
                if track.can_be_armed:
                    if track.arm:
                        track.arm = False

    def _unsolo_all_value(self, value):
        if not (value != 0 or self._unsolo_all_button.is_momentary()):
            for track in tuple(self.song().tracks) + tuple(self.song().return_tracks):
                if track.solo:
                    track.solo = False

    def _unmute_all_value(self, value):
        if not (value != 0 or self._unmute_all_button.is_momentary()):
            for track in tuple(self.song().tracks) + tuple(self.song().return_tracks):
                if track.mute:
                    track.mute = False