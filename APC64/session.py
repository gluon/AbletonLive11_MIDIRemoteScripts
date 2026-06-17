# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\APC64\session.py
# Compiled at: 2023-08-04 12:30:20
# Size of source mod 2**32: 3258 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v3.base import depends
from ableton.v3.control_surface.components import ClipSlotComponent as ClipSlotComponentBase
from ableton.v3.control_surface.components import SceneComponent as SceneComponentBase
from ableton.v3.control_surface.components import SessionComponent as SessionComponentBase
from ableton.v3.control_surface.controls import ButtonControl
from ableton.v3.live import action, liveobj_valid

class ClipSlotComponent(ClipSlotComponentBase):
    quantize_button = ButtonControl(color=None)

    @depends(settings_component=None)
    def __init__(self, settings_component=None, *a, **k):
        (super().__init__)(*a, **k)
        self._quantization = settings_component.quantization
        self._fixed_length = settings_component.fixed_length

    def do_launch_slot(self):
        if self._fixed_length.enabled:
            if liveobj_valid(self._clip_slot) and not self._clip_slot.is_group_slot:
                self._has_clip() or self._clip_slot.fire(record_length=(self._fixed_length.record_length))
            else:
                super()._do_launch_slot()

    def _do_launch_slot(self):
        self.do_launch_slot()

    def _on_launch_button_pressed(self):
        has_clip = self._has_clip()
        if has_clip and self.select_button.is_pressed and self.duplicate_button.is_pressed:
            action.duplicate_loop(self._clip_slot.clip)
        else:
            if has_clip and self.quantize_button.is_pressed:
                self._quantization.quantize_clip(self._clip_slot.clip)
            else:
                super()._on_launch_button_pressed()

    def _any_modifier_pressed(self):
        return super()._any_modifier_pressed() or self.quantize_button.is_pressed


class SceneComponent(SceneComponentBase):

    @depends(settings_component=None)
    def __init__(self, settings_component=None, *a, **k):
        (super().__init__)(*a, **k)
        self._fixed_length = settings_component.fixed_length

    def _do_launch_scene(self):
        if self._fixed_length.enabled:
            for slot in self._clip_slots:
                slot.do_launch_slot()

        else:
            super()._do_launch_scene()


class SessionComponent(SessionComponentBase):

    def __init__(self, *a, **k):
        (super().__init__)(a, clip_slot_component_type=ClipSlotComponent, scene_component_type=SceneComponent, **k)

    def set_quantize_button(self, button):
        self.set_modifier_button(button, 'quantize_button', clip_slots_only=True)