# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\APC40\SessionComponent.py
# Compiled at: 2022-11-29 09:57:02
# Size of source mod 2**32: 1124 bytes
from __future__ import absolute_import, print_function, unicode_literals
from _Framework.Control import ButtonControl
from _APC.SessionComponent import SessionComponent as SessionComponentBase

class SessionComponent(SessionComponentBase):
    slot_launch_button = ButtonControl()
    selected_scene_launch_button = ButtonControl()

    def set_slot_launch_button(self, button):
        self.slot_launch_button.set_control_element(button)

    @slot_launch_button.pressed
    def slot_launch_button(self, button):
        clip_slot = self.song().view.highlighted_clip_slot
        if clip_slot:
            clip_slot.fire()

    def set_selected_scene_launch_button(self, button):
        self.selected_scene_launch_button.set_control_element(button)

    @selected_scene_launch_button.pressed
    def selected_scene_launch_button(self, button):
        scene = self.song().view.selected_scene
        if scene:
            scene.fire()