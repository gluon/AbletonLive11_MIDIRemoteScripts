#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/novation/clip_actions.py
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import duplicate_clip_loop
from ableton.v2.control_surface.components import ClipActionsComponent as ClipActionsComponentBase
from .blinking_button import BlinkingButtonControl

class ClipActionsComponent(ClipActionsComponentBase):
    quantization_component = None
    quantize_button = BlinkingButtonControl(color=u'Action.Quantize', blink_on_color=u'Action.QuantizePressed', blink_off_color=u'Action.Quantize')
    double_loop_button = BlinkingButtonControl(color=u'Action.Double', blink_on_color=u'Action.DoublePressed', blink_off_color=u'Action.Double')
    __events__ = (u'can_perform_clip_actions',)

    def __init__(self, *a, **k):
        super(ClipActionsComponent, self).__init__(*a, **k)
        self.delete_button.color = u'Action.Delete'
        self.delete_button.pressed_color = u'Action.DeletePressed'
        self.duplicate_button.color = u'Action.Duplicate'
        self.duplicate_button.pressed_color = u'Action.DuplicatePressed'

    @quantize_button.pressed
    def quantize_button(self, _):
        if self.quantization_component:
            self.quantization_component.quantize_clip(self.clip_slot.clip)
            self.quantize_button.start_blinking()

    @double_loop_button.pressed
    def double_loop_button(self, _):
        duplicate_clip_loop(self.clip_slot.clip)
        self.double_loop_button.start_blinking()

    def delete_pitch(self, pitch):
        clip = self.clip_slot.clip
        loop_length = clip.loop_end - clip.loop_start
        clip.remove_notes_extended(from_time=clip.loop_start, from_pitch=pitch, time_span=loop_length, pitch_span=1)

    def delete_clip(self):
        self.clip_slot.delete_clip()

    def _update_action_buttons(self):
        super(ClipActionsComponent, self)._update_action_buttons()
        can_perform_clip_action = self._can_perform_clip_action()
        self.quantize_button.enabled = can_perform_clip_action
        self.notify_can_perform_clip_actions(can_perform_clip_action)
