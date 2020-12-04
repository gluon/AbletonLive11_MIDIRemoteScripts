#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/pushbase/step_seq_component.py
from __future__ import absolute_import, print_function, unicode_literals
from itertools import chain, starmap
from ableton.v2.base import forward_property, listenable_property, listens, liveobj_valid
from ableton.v2.control_surface import Component
from ableton.v2.control_surface.components import AccentComponent
from ableton.v2.control_surface.elements import to_midi_value
from .loop_selector_component import LoopSelectorComponent
from .playhead_component import PlayheadComponent
from .note_editor_paginator import NoteEditorPaginator
from .matrix_maps import PLAYHEAD_FEEDBACK_CHANNELS
from .step_duplicator import StepDuplicatorComponent

class StepSeqComponent(Component):
    u"""
    This component represents one of the sequencing mechanisms for Push, which has one
    NoteEditorComponent associated with a single pitch. The component mostly manages
    distributing control elements to sub-components, which then provide the logic for
    this layout.
    """

    def __init__(self, clip_creator = None, skin = None, grid_resolution = None, note_editor_component = None, instrument_component = None, *a, **k):
        super(StepSeqComponent, self).__init__(*a, **k)
        assert clip_creator is not None
        assert skin is not None
        assert instrument_component is not None
        assert note_editor_component is not None
        self._grid_resolution = grid_resolution
        self._note_editor = note_editor_component
        self._loop_selector = LoopSelectorComponent(parent=self, clip_creator=clip_creator, default_size=16)
        self._instrument = instrument_component
        self.paginator = NoteEditorPaginator([self._note_editor], parent=self)
        self._step_duplicator = StepDuplicatorComponent(parent=self)
        self._note_editor.set_step_duplicator(self._step_duplicator)
        self._loop_selector.set_step_duplicator(self._step_duplicator)
        self._loop_selector.set_paginator(self.paginator)
        self._on_pressed_pads_changed.subject = self._instrument
        self._on_selected_notes_changed.subject = self._instrument.selected_notes_provider
        self._on_detail_clip_changed.subject = self.song.view
        self.__on_grid_resolution_changed.subject = self._grid_resolution
        self._on_page_index_changed.subject = self.paginator
        self._on_page_length_changed.subject = self.paginator
        self._on_active_steps_changed.subject = self._note_editor
        self._on_modify_all_notes_changed.subject = self._note_editor
        self._detail_clip = None
        self._playhead = None
        self._playhead_component = PlayheadComponent(parent=self, grid_resolution=grid_resolution, paginator=self.paginator, follower=self._loop_selector, notes=chain(*starmap(range, ((92, 100),
         (84, 92),
         (76, 84),
         (68, 76)))), triplet_notes=chain(*starmap(range, ((92, 98),
         (84, 90),
         (76, 82),
         (68, 74)))), feedback_channels=PLAYHEAD_FEEDBACK_CHANNELS)
        self._accent_component = AccentComponent(parent=self)
        self.__on_accent_mode_changed.subject = self._accent_component
        self._skin = skin
        self._playhead_color = u'NoteEditor.Playhead'

    next_loop_page_button = forward_property(u'_loop_selector')(u'next_page_button')
    prev_loop_page_button = forward_property(u'_loop_selector')(u'prev_page_button')

    def set_playhead(self, playhead):
        self._playhead = playhead
        self._playhead_component.set_playhead(playhead)
        self._update_playhead_color()

    def set_full_velocity(self, full_velocity):
        self._accent_component.set_full_velocity(full_velocity)
        self.__on_accent_mode_changed()

    def set_accent_button(self, accent_button):
        self._accent_component.accent_button.set_control_element(accent_button)

    def _get_playhead_color(self):
        return self._playhead_color

    def _set_playhead_color(self, value):
        self._playhead_color = u'NoteEditor.' + value
        self._update_playhead_color()

    playhead_color = property(_get_playhead_color, _set_playhead_color)

    @listenable_property
    def editing_note_regions(self):
        return self._note_editor.editing_note_regions

    @listenable_property
    def editable_pitches(self):
        return self._note_editor.editing_notes

    @listenable_property
    def step_length(self):
        return self._grid_resolution.step_length

    @listenable_property
    def row_start_times(self):
        return self._note_editor.get_row_start_times()

    @listens(u'index')
    def __on_grid_resolution_changed(self, *a):
        if self.is_enabled():
            self.notify_row_start_times()
            self.notify_step_length()

    @listens(u'page_index')
    def _on_page_index_changed(self):
        if self.is_enabled():
            self.notify_row_start_times()

    @listens(u'page_length')
    def _on_page_length_changed(self):
        if self.is_enabled():
            self.notify_row_start_times()

    @listens(u'active_steps')
    def _on_active_steps_changed(self):
        if self.is_enabled():
            self.notify_editing_note_regions()

    @listens(u'modify_all_notes')
    def _on_modify_all_notes_changed(self):
        if self.is_enabled():
            self.notify_editing_note_regions()

    @listens(u'activated')
    def __on_accent_mode_changed(self):
        self._note_editor.full_velocity = self._accent_component.activated

    def _is_triplet_quantization(self):
        return self._grid_resolution.clip_grid[1]

    def _update_playhead_color(self):
        if self.is_enabled() and self._skin and self._playhead:
            self._playhead.velocity = to_midi_value(self._skin[self._playhead_color])

    def set_select_button(self, button):
        self._instrument.select_button.set_control_element(button)
        self._loop_selector.select_button.set_control_element(button)

    def set_mute_button(self, button):
        self._note_editor.mute_button.set_control_element(button)

    def set_delete_button(self, button):
        self._instrument.delete_button.set_control_element(button)
        self._loop_selector.delete_button.set_control_element(button)

    def set_loop_selector_matrix(self, matrix):
        self._loop_selector.set_loop_selector_matrix(matrix)

    def set_short_loop_selector_matrix(self, matrix):
        self._loop_selector.set_short_loop_selector_matrix(matrix)

    def set_duplicate_button(self, button):
        self._step_duplicator.button.set_control_element(button)

    def set_button_matrix(self, matrix):
        self._note_editor.set_matrix(matrix)

    def set_quantization_buttons(self, buttons):
        self._grid_resolution.quantization_buttons.set_control_element(buttons)

    def set_velocity_control(self, control):
        self._note_editor.set_velocity_control(control)

    def set_length_control(self, control):
        self._note_editor.set_length_control(control)

    def set_nudge_control(self, control):
        self._note_editor.set_nudge_control(control)

    def update(self):
        super(StepSeqComponent, self).update()
        if self.is_enabled():
            self._on_selected_notes_changed(self._instrument.selected_notes_provider.selected_notes)
            self._update_playhead_color()
            self._on_detail_clip_changed()
            self.notify_row_start_times()
            self.notify_step_length()

    @listens(u'detail_clip')
    def _on_detail_clip_changed(self):
        clip = self.song.view.detail_clip
        clip = clip if liveobj_valid(clip) and clip.is_midi_clip else None
        self._detail_clip = clip
        self._note_editor.set_detail_clip(clip)
        self._loop_selector.set_detail_clip(clip)
        self._playhead_component.set_clip(self._detail_clip)

    @listens(u'selected_notes')
    def _on_selected_notes_changed(self, notes):
        if self.is_enabled():
            self._note_editor.editing_notes = notes
            self.notify_editable_pitches()

    @listens(u'pressed_pads')
    def _on_pressed_pads_changed(self, _):
        self._note_editor.modify_all_notes_enabled = len(self._instrument.pressed_pads) > 0


class DrumStepSeqComponent(StepSeqComponent):

    def set_solo_button(self, button):
        self._instrument.set_solo_button(button)

    def set_mute_button(self, button):
        super(DrumStepSeqComponent, self).set_mute_button(button)
        self._instrument.set_mute_button(button)
