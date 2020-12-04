#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Launchpad_Pro_MK3/session.py
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import duplicate_clip_loop
from ableton.v2.control_surface.components import SceneComponent as SceneComponentBase, SessionComponent as SessionComponentBase
from ableton.v2.control_surface.components.clip_slot import is_button_pressed
from ableton.v2.control_surface.control import ButtonControl
from novation.clip_slot import FixedLengthClipSlotComponent as ClipSlotComponentBase

class ClipSlotComponent(ClipSlotComponentBase):
    quantization_component = None

    def __init__(self, *a, **k):
        super(ClipSlotComponent, self).__init__(*a, **k)
        self._quantize_button = None
        self._double_button = None

    def set_quantize_button(self, button):
        self._quantize_button = button

    def set_double_button(self, button):
        self._double_button = button

    def _on_launch_button_pressed(self):
        if is_button_pressed(self._quantize_button):
            self._do_quantize_clip()
        elif is_button_pressed(self._double_button):
            self._do_double_clip()
        else:
            super(ClipSlotComponent, self)._on_launch_button_pressed()

    def _on_launch_button_released(self):
        self._update_launch_button_color()
        if is_button_pressed(self._quantize_button) or is_button_pressed(self._double_button):
            return
        super(ClipSlotComponent, self)._on_launch_button_released()

    def _do_quantize_clip(self):
        if self.quantization_component and self.has_clip():
            self.quantization_component.quantize_clip(self._clip_slot.clip)
            self.launch_button.color = u'Session.ActionTriggered'

    def _do_double_clip(self):
        if self.has_clip() and self._clip_slot.clip.is_midi_clip:
            duplicate_clip_loop(self._clip_slot.clip)
            self.launch_button.color = u'Session.ActionTriggered'

    def _on_clip_deleted(self):
        self.launch_button.color = u'Session.ActionTriggered'

    def _on_slot_selected(self):
        self.launch_button.color = u'Session.ActionTriggered'

    def _on_clip_duplicated(self):
        self.launch_button.color = u'Session.ActionTriggered'

    def _update_launch_button_color(self):
        if self.launch_button.is_pressed:
            return
        super(ClipSlotComponent, self)._update_launch_button_color()


class SceneComponent(SceneComponentBase):
    clip_slot_component_type = ClipSlotComponent

    def _on_launch_button_released(self):
        self._update_launch_button()
        super(SceneComponent, self)._on_launch_button_released()

    def _on_scene_selected(self):
        self.launch_button.color = u'Session.ActionTriggered'

    def _on_scene_deleted(self):
        self.launch_button.color = u'Session.ActionTriggered'

    def _on_scene_duplicated(self):
        self.launch_button.color = u'Session.ActionTriggered'

    def _update_launch_button(self):
        if self.launch_button.is_pressed:
            return
        super(SceneComponent, self)._update_launch_button()


class SessionComponent(SessionComponentBase):
    scene_component_type = SceneComponent
    managed_quantize_button = ButtonControl(color=u'Session.Quantize', pressed_color=u'Session.QuantizePressed')
    managed_double_button = ButtonControl(color=u'Session.Double', pressed_color=u'Session.DoublePressed')

    def set_managed_quantize_button(self, button):
        self.managed_quantize_button.set_control_element(button)
        self.set_modifier_button(button, u'quantize', clip_slots_only=True)

    def set_managed_double_button(self, button):
        self.managed_double_button.set_control_element(button)
        self.set_modifier_button(button, u'double', clip_slots_only=True)
