# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v2/control_surface/components/clip_actions.py
# Compiled at: 2021-06-29 09:33:48
# Size of source mod 2**32: 3021 bytes
from __future__ import absolute_import, print_function, unicode_literals
import Live
from ...base import duplicate_clip_loop, listens, liveobj_valid
from ...control_surface import Component
from control_surface.control import ButtonControl

class ClipActionsComponent(Component):
    delete_button = ButtonControl(color='Action.Available')
    duplicate_button = ButtonControl(color='Action.Available')
    double_loop_button = ButtonControl(color='Action.Available')

    def __init__(self, *a, **k):
        (super(ClipActionsComponent, self).__init__)(*a, **k)
        view = self.song.view
        self._ClipActionsComponent__on_selected_scene_changed.subject = view
        self._ClipActionsComponent__on_selected_track_changed.subject = view
        self._ClipActionsComponent__on_selected_track_changed()

    @property
    def clip_slot(self):
        return self.song.view.highlighted_clip_slot

    @delete_button.released
    def delete_button(self, _):
        self.clip_slot.delete_clip()

    @duplicate_button.pressed
    def duplicate_button(self, _):
        clip_slot = self.clip_slot
        view = self.song.view
        track = view.selected_track
        try:
            source_index = list(track.clip_slots).index(clip_slot)
            target_index = track.duplicate_clip_slot(source_index)
            view.highlighted_clip_slot = track.clip_slots[target_index]
            view.detail_clip = view.highlighted_clip_slot.clip
            if clip_slot.clip.is_playing:
                view.highlighted_clip_slot.fire(force_legato=True,
                  launch_quantization=(Live.Song.Quantization.q_no_q))
        except (Live.Base.LimitationError, RuntimeError):
            pass

    @double_loop_button.pressed
    def double_loop_button(self, _):
        duplicate_clip_loop(self.clip_slot.clip)

    @listens('selected_scene')
    def __on_selected_scene_changed(self):
        self._update_clip_slot()

    @listens('selected_track')
    def __on_selected_track_changed(self):
        self._ClipActionsComponent__on_input_routing_type_changed.subject = self.song.view.selected_track
        self._update_clip_slot()

    @listens('input_routing_type')
    def __on_input_routing_type_changed(self):
        self._update_action_buttons()

    @listens('has_clip')
    def __on_has_clip_changed(self):
        self._update_action_buttons()

    def _update_clip_slot(self):
        self._ClipActionsComponent__on_has_clip_changed.subject = self.song.view.highlighted_clip_slot
        self._ClipActionsComponent__on_has_clip_changed()

    def _update_action_buttons(self):
        can_perform_clip_action = self._can_perform_clip_action()
        self.delete_button.enabled = can_perform_clip_action
        self.duplicate_button.enabled = can_perform_clip_action
        self.double_loop_button.enabled = can_perform_clip_action and self.clip_slot.clip.is_midi_clip

    def _can_perform_clip_action(self):
        clip_slot = self.clip_slot
        return liveobj_valid(clip_slot) and clip_slot.has_clip