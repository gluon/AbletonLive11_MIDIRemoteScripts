# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchpad_Pro_MK3\drum_group.py
# Compiled at: 2022-11-28 08:01:31
# Size of source mod 2**32: 3501 bytes
from __future__ import absolute_import, print_function, unicode_literals
from functools import partial
from ableton.v2.base import listens
from ableton.v2.control_surface.control import ButtonControl
from novation.drum_group import DrumGroupComponent as DrumGroupComponentBase
DEFAULT_SCROLL_POSITION = 9

class DrumGroupComponent(DrumGroupComponentBase):
    delete_button = ButtonControl(color='Action.Delete',
      pressed_color='Action.DeletePressed')

    def __init__(self, clip_actions, *a, **k):
        (super(DrumGroupComponent, self).__init__)(*a, **k)
        self._can_delete_clip = False
        self._clip_actions = clip_actions
        self._DrumGroupComponent__on_can_perform_actions_actions_changed.subject = self._clip_actions
        self._position_scroll._ensure_scroll_one_direction = partial(self._possibly_reset_scroll_position, self._position_scroll)
        self._position_scroll._update_scroll_buttons = partial(self._update_scroll_buttons, self._position_scroll)
        self._page_scroll._ensure_scroll_one_direction = partial(self._possibly_reset_scroll_position, self._page_scroll)
        self._page_scroll._update_scroll_buttons = partial(self._update_scroll_buttons, self._page_scroll)

    @delete_button.value
    def delete_button(self, value, button):
        self._set_control_pads_from_script(bool(value))
        if value:
            self._can_delete_clip = True
        else:
            if self._can_delete_clip:
                self._clip_actions.delete_clip()

    def delete_pitch(self, drum_pad):
        self._can_delete_clip = False
        self._clip_actions.delete_pitch(drum_pad.note)

    def _possibly_reset_scroll_position(self, scroll_component):
        if scroll_component.scroll_up_button.is_pressed:
            if scroll_component.scroll_down_button.is_pressed:
                scroll_component._scroll_task_up.kill()
                scroll_component._scroll_task_down.kill()
                self.position = DEFAULT_SCROLL_POSITION

    def _update_scroll_buttons(self, scroll_component):
        self._update_scroll_button(scroll_component.scroll_up_button, scroll_component.can_scroll_up())
        self._update_scroll_button(scroll_component.scroll_down_button, scroll_component.can_scroll_down())

    def _update_scroll_button(self, button, can_scroll):
        button.enabled = True
        button.color = 'DrumGroup.Navigation' if can_scroll else 'DefaultButton.Disabled'
        button.pressed_color = 'DrumGroup.NavigationPressed' if can_scroll else 'DefaultButton.Disabled'

    @listens('can_perform_clip_actions')
    def __on_can_perform_actions_actions_changed(self, can_perform_clip_actions):
        self.delete_button.enabled = can_perform_clip_actions