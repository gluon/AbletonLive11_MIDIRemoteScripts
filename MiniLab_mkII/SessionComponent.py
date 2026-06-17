# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\MiniLab_mkII\SessionComponent.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 2603 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
from itertools import product
from _Framework.ClipSlotComponent import ClipSlotComponent as ClipSlotComponentBase
from _Framework.SceneComponent import SceneComponent as SceneComponentBase
from _Arturia.SessionComponent import SessionComponent as SessionComponentBase
EMPTY_VALUE = 0
TRIGGERED_TO_RECORD_VALUE = 1
RECORDING_VALUE = 1
TRIGGERED_TO_PLAY_VALUE = 4
STARTED_VALUE = 4
STOPPED_VALUE = 5

class ClipSlotComponent(ClipSlotComponentBase):

    def __init__(self, *a, **k):
        (super(ClipSlotComponent, self).__init__)(*a, **k)
        self._led = None

    def set_led(self, led):
        self._led = led

    def update(self):
        super(ClipSlotComponent, self).update()
        self._update_led()

    def _update_led(self):
        if self.is_enabled():
            if self._led != None:
                value_to_send = self._feedback_value()
                if value_to_send in (None, -1):
                    value_to_send = EMPTY_VALUE
                self._led.send_value((value_to_send,))

    def _feedback_value(self):
        if self._clip_slot != None:
            if self.has_clip():
                clip = self._clip_slot.clip
                if clip.is_triggered:
                    if clip.will_record_on_start:
                        return TRIGGERED_TO_RECORD_VALUE
                    return TRIGGERED_TO_PLAY_VALUE
                if clip.is_playing:
                    if clip.is_recording:
                        return RECORDING_VALUE
                    return STARTED_VALUE
                return STOPPED_VALUE


class SceneComponent(SceneComponentBase):
    clip_slot_component_type = ClipSlotComponent


class SessionComponent(SessionComponentBase):
    scene_component_type = SceneComponent

    def set_clip_slot_leds(self, leds):
        if leds:
            for led, (x, y) in leds.iterbuttons():
                scene = self.scene(y)
                slot = scene.clip_slot(x)
                slot.set_led(led)

        else:
            for x, y in product(range(self._num_tracks), range(self._num_scenes)):
                scene = self.scene(y)
                slot = scene.clip_slot(x)
                slot.set_led(None)