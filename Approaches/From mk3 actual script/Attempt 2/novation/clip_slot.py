#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/novation/clip_slot.py
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import const, depends
from ableton.v2.control_surface.components import ClipSlotComponent as ClipSlotComponentBase

class FixedLengthClipSlotComponent(ClipSlotComponentBase):

    @depends(fixed_length_recording=const(None))
    def __init__(self, fixed_length_recording, *a, **k):
        assert fixed_length_recording is not None
        super(FixedLengthClipSlotComponent, self).__init__(*a, **k)
        self._fixed_length_recording = fixed_length_recording

    def _do_launch_clip(self, fire_state):
        slot = self._clip_slot
        if self._fixed_length_recording.should_start_recording_in_slot(slot):
            self._fixed_length_recording.start_recording_in_slot(slot)
        else:
            super(FixedLengthClipSlotComponent, self)._do_launch_clip(fire_state)
