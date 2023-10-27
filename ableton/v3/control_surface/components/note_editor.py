# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\components\note_editor.py
# Compiled at: 2023-10-06 14:17:18
# Size of source mod 2**32: 23076 bytes
from __future__ import absolute_import, print_function, unicode_literals
from math import inf
from Live.Clip import MidiNoteSpecification
from ...base import EventObject, clamp, depends, in_range, listenable_property, listens
from ...live import liveobj_changed, liveobj_valid
from .. import Component
from ..controls import ButtonControl, control_matrix
from ..skin import LiveObjSkinEntry
PROPERTY_RANGE_KEYS = ('pitch', 'start_time', 'duration', 'velocity')
RELATIVE_OFFSET = 0.24
DEFAULT_HEIGHT = 4
DEFAULT_WIDTH = 4
DEFAULT_VELOCITY = 100
DEFAULT_START_NOTE = 36
DEFAULT_STEP_TRANSLATION_CHANNEL = 1

def get_notes(clip, pitches, time, length, all_pitches=False):
    if len(pitches) > 1 or all_pitches:
        return clip.get_notes_extended(from_time=time,
          from_pitch=0,
          time_span=length,
          pitch_span=128)
    return clip.get_notes_extended(from_time=time,
      from_pitch=(pitches[0]),
      time_span=length,
      pitch_span=1)


def remove_notes(clip, pitches, time, length, all_pitches=False):
    if len(pitches) > 1 or all_pitches:
        clip.remove_notes_extended(from_time=time,
          from_pitch=0,
          time_span=length,
          pitch_span=128)
    else:
        clip.remove_notes_extended(from_time=time,
          from_pitch=(pitches[0]),
          time_span=length,
          pitch_span=1)


def property_ranges_for_notes(notes, start_time, property_ranges):
    for note in notes:
        note_values = [
         note.pitch, note.start_time, note.duration, note.velocity]
        note_values[1] -= start_time
        for key, value in zip(PROPERTY_RANGE_KEYS, note_values):
            if not property_ranges:
                property_ranges = {key: (inf, -inf) for key in PROPERTY_RANGE_KEYS}
            else:
                min_value, max_value = property_ranges[key]
                property_ranges[key] = (min(value, min_value), max(value, max_value))

    return property_ranges


class PitchProvider(EventObject):
    pitches = listenable_property.managed([DEFAULT_START_NOTE])
    is_polyphonic = listenable_property.managed(False)


class TimeStep:

    def __init__(self, start, length, *a, **k):
        (super().__init__)(*a, **k)
        self.start = start
        self.length = length

    @property
    def offset(self):
        return self.length * RELATIVE_OFFSET

    def left_boundary(self):
        return max(0, self.start - self.length * 0.2)

    def right_boundary(self):
        return max(0, self.start + self.length * 0.7)

    def filter_notes(self, notes):
        return list(filter(self.includes_note, notes))

    def clamp(self, time):
        return clamp(time, self.left_boundary(), self.right_boundary())

    def includes_note(self, note):
        return self.includes_time(note.start_time)

    def includes_time(self, time):
        return in_range(time - self.start + self.offset, 0, self.length)

    def connected_time_ranges(self):
        return [
         (
          self.start - self.offset, self.length)]


class StepButtonControl(ButtonControl):

    class State(ButtonControl.State):
        x = property(lambda self: self.coordinate[1]
)
        y = property(lambda self: self.coordinate[0]
)
        is_active = False


class NoteEditorComponent(Component):
    __events__ = ('clip_notes', )
    matrix = control_matrix(StepButtonControl)

    @depends(target_track=None,
      sequencer_clip=None,
      full_velocity=None,
      grid_resolution=None)
    def __init__(self, name='Note_Editor', translation_channel=DEFAULT_STEP_TRANSLATION_CHANNEL, full_velocity=None, target_track=None, sequencer_clip=None, grid_resolution=None, *a, **k):
        (super().__init__)(a, name=name, **k)
        self._full_velocity = full_velocity
        self._translation_channel = translation_channel
        self._page_time = 0.0
        self._pitches = [
         DEFAULT_START_NOTE]
        self._pitch_provider = PitchProvider()
        self._clip_notes = []
        self._clip = None
        self._sequencer_clip = sequencer_clip
        self._active_steps = []
        self._grid_resolution = grid_resolution
        self._NoteEditorComponent__on_resolution_changed.subject = self._grid_resolution
        self._nudge_offset = 0
        self._duration_offset = 0
        self._velocity_offset = 0
        self._pitch_offset = 0
        self._triplet_factor = 1.0
        self._is_triplet = False
        self._update_from_grid()
        self._target_track = target_track
        self._NoteEditorComponent__on_target_track_color_changed.subject = target_track
        self._NoteEditorComponent__on_sequencer_clip_changed.subject = sequencer_clip
        self._NoteEditorComponent__on_sequencer_clip_changed()

    @property
    def width(self):
        if self.matrix.width:
            return self.matrix.width
        return DEFAULT_WIDTH

    @property
    def height(self):
        if self.matrix.height:
            return self.matrix.height
        return DEFAULT_HEIGHT

    @property
    def step_count(self):
        return self.width * self.height

    @property
    def step_length(self):
        return self._grid_resolution.step_length

    @property
    def can_change_page(self):
        return not self._active_steps

    @property
    def page_time(self):
        return self._page_time

    @page_time.setter
    def page_time(self, time):
        if time != self._page_time:
            self._page_time = time
            self.page_time_changed()
            self._NoteEditorComponent__on_clip_notes_changed()

    @listenable_property
    def page_length(self):
        return self.step_count * self.step_length * self._triplet_factor

    @listenable_property
    def active_steps(self):
        return list(map(self._get_step_time_range, self._active_steps))

    @listenable_property
    def pitch_provider(self):
        return self._pitch_provider

    @pitch_provider.setter
    def pitch_provider(self, provider):
        self._pitch_provider = provider
        self._NoteEditorComponent__on_provider_polyphony_changed.subject = provider
        self._NoteEditorComponent__on_provided_pitches_changed.subject = provider
        self._NoteEditorComponent__on_provided_pitches_changed(provider.pitches if provider else [])
        self.notify_pitch_provider()

    def set_clip(self, clip):
        if liveobj_changed(clip, self._clip):
            self._clip = clip
            if self.can_change_page:
                self.page_time = 0.0
            self._NoteEditorComponent__on_clip_notes_changed.subject = clip
            self._NoteEditorComponent__on_clip_notes_changed()

    def set_pitches(self, pitches):
        if pitches != self._pitches:
            self._pitches = pitches
            enabled = self._can_edit()
            for button in self.matrix:
                button.enabled = enabled

            if enabled:
                self._NoteEditorComponent__on_clip_notes_changed()

    def set_pitch_offset(self, value):
        self._modify_note_property('_pitch_offset', value)

    def set_duration_offset(self, value):
        self._modify_note_property('_duration_offset', value)

    def set_velocity_offset(self, value):
        self._modify_note_property('_velocity_offset', value)

    def set_nudge_offset(self, value):
        self._modify_note_property('_nudge_offset', value)

    def set_matrix(self, matrix):
        self.matrix.set_control_element(matrix)
        for button in self.matrix:
            button.channel = self._translation_channel

        self._update_editor_matrix()

    def is_pitch_active(self, pitch):
        if self._has_clip():
            for step in self.active_steps:
                if get_notes(self._clip, (pitch,), step[0], step[1]):
                    return True

        return False

    def toggle_pitch_for_all_active_steps(self, pitch):
        for step in self._active_steps:
            time, _, pitches = self._get_notes_info_from_step(step)
            if pitch not in pitches:
                self._add_new_note_in_step(pitch, time)
            else:
                time_step = self._time_step(self._get_step_start_time(step))
                for time, length in time_step.connected_time_ranges():
                    remove_notes(self._clip, (pitch,), time, length)

    def can_nudge_by_offset(self, offset):
        for step in self.active_steps:
            notes = self._time_step(step[0]).filter_notes(self._clip_notes)
            time_step = self._time_step(step[0])
            for note in notes:
                new_start_time = time_step.clamp(note.start_time + offset)
                if new_start_time != note.start_time:
                    if in_range(new_start_time, time_step.left_boundary(), time_step.right_boundary()):
                        return True

        return False

    def get_note_property_ranges(self):
        property_ranges = {}
        if self._active_steps:
            for step in self._active_steps:
                start_time = self._get_step_start_time(step)
                property_ranges = property_ranges_for_notes(self._time_step(start_time).filter_notes(self._clip_notes), start_time, property_ranges)

        return property_ranges

    def page_time_changed(self):
        pass

    def _time_step(self, time):
        return TimeStep(time, self.step_length)

    def _can_edit(self):
        return len(self._pitches) != 0

    def _has_clip(self):
        return liveobj_valid(self._clip)

    def _can_press_or_release_step(self, step):
        width = self.width * self._triplet_factor if self._is_triplet else self.width
        return self._can_edit() and step.x < width and step.y < self.height

    def _get_step_start_time(self, step):
        step_time = step.x + step.y * self.width * self._triplet_factor
        return self._page_time + step_time * self.step_length

    def _get_step_time_range(self, step):
        time = self._get_step_start_time(step)
        return (
         time, time + self.step_length)

    def _get_notes_info_from_step(self, step):
        time = self._get_step_start_time(step)
        notes = self._time_step(time).filter_notes(self._clip_notes)
        pitches = [note.pitch for note in notes]
        return (
         time, notes, pitches)

    def _get_clip_notes_time_range(self):
        return (
         self._page_time - self._time_step(0).offset, self.page_length)

    @matrix.pressed
    def matrix(self, pad):
        self._on_pad_pressed(pad)

    def _on_pad_pressed(self, pad):
        if self.is_enabled():
            if not self._has_clip():
                self.set_clip(self._sequencer_clip.create_clip())
                self._update_from_grid()
            if self._can_press_or_release_step(pad):
                pad.is_active = True
                self._refresh_active_steps()

    @matrix.released_immediately
    def matrix(self, pad):
        self._on_pad_released(pad, can_add_or_remove=True)

    @matrix.released_delayed
    def matrix(self, pad):
        self._on_pad_released(pad)

    def _on_pad_released(self, pad, **k):
        if self.is_enabled():
            if self._can_press_or_release_step(pad):
                (self._on_release_step)(pad, **k)

    def _on_release_step(self, step, can_add_or_remove=False):
        if step.is_active:
            if can_add_or_remove:
                self._delete_notes_in_step(step)
                for pitch in self._pitches:
                    self._add_note_in_step(step, pitch)

        step.is_active = False
        self._refresh_active_steps()

    def _refresh_active_steps(self):
        self._active_steps = [s for s in self.matrix if s.is_active]
        self.notify_active_steps()

    def _release_active_steps(self):
        for step in self.matrix:
            self._on_release_step(step)

    def _add_note_in_step(self, step, pitch):
        if self._has_clip():
            time, notes, _ = self._get_notes_info_from_step(step)
            if not notes:
                self._add_new_note_in_step(pitch, time)

    def _add_new_note_in_step(self, pitch, time):
        velocity = 127 if self._full_velocity.enabled else DEFAULT_VELOCITY
        note = MidiNoteSpecification(pitch=pitch,
          start_time=time,
          duration=(self.step_length),
          velocity=velocity,
          mute=False)
        self._clip.add_new_notes((note,))
        self._clip.deselect_all_notes()

    def _delete_notes_in_step(self, step):
        if self._has_clip():
            if self._can_edit():
                time_step = self._time_step(self._get_step_start_time(step))
                for time, length in time_step.connected_time_ranges():
                    remove_notes(self._clip, self._pitches, time, length, self._pitch_provider.is_polyphonic)

    def _modify_note_property(self, note_property, value):
        if self.is_enabled():
            setattr(self, note_property, getattr(self, note_property) + value)
            if self._active_steps:
                if self._has_clip():
                    if self._can_edit():
                        self._modify_step_notes(self._active_steps)
                        self._clip.apply_note_modifications(self._clip_notes)
                        self._update_editor_matrix()
                        self.notify_active_steps()
            self._reset_modifications()

    def _reset_modifications(self):
        self._pitch_offset = 0
        self._velocity_offset = 0
        self._duration_offset = 0
        self._nudge_offset = 0

    def _modify_step_notes(self, steps):
        notes = self._clip_notes
        for step in steps:
            time_step = self._time_step(self._get_step_start_time(step))
            for note in notes:
                self._modify_note(time_step, self._duration_offset, self._nudge_offset, note)

    def _modify_note(self, time_step, duration_offset, nudge_offset, note):
        if time_step.includes_time(note.start_time):
            note.start_time = time_step.clamp(note.start_time + nudge_offset)
            note.duration = max(time_step.length * 0.1, note.duration + duration_offset)
            note.velocity = clamp(note.velocity + self._velocity_offset, 1, 127)
            note.pitch = clamp(note.pitch + self._pitch_offset, 0, 127)

    def _update_from_grid(self):
        quantization, self._is_triplet = self._grid_resolution.clip_grid
        self._triplet_factor = 1.0 if (not self._is_triplet) else 0.75
        if self._has_clip():
            self._clip.view.grid_quantization = quantization
            self._clip.view.grid_is_triplet = self._is_triplet

    def update(self):
        super().update()
        self._update_editor_matrix()

    def _update_editor_matrix(self):
        if self.is_enabled():
            visible_steps = self._visible_steps()
            for index, button in enumerate(self.matrix):
                button.color = LiveObjSkinEntry(self._get_color_for_step(index, visible_steps), self._target_track.target_track)

    def _get_color_for_step(self, index, visible_steps):
        color = 'NoteEditor.StepDisabled'
        if self._has_clip() and index in visible_steps:
            notes = visible_steps[index].filter_notes(self._clip_notes)
            color = 'NoteEditor.StepEmpty'
            if len(notes) > 0:
                if any((n.mute for n in notes)):
                    color = 'NoteEditor.StepMuted'
                else:
                    color = 'NoteEditor.StepFilled'
        else:
            if index in visible_steps:
                color = 'NoteEditor.NoClip'
        return self._get_alternate_color_for_step(index, visible_steps) or color

    def _get_alternate_color_for_step(self, index, visible_steps):
        pass

    def _visible_steps(self):
        steps_per_page = self.step_count
        step_length = self.step_length
        indices = list(range(steps_per_page))
        if self._is_triplet:
            width = self.width
            columns_to_omit = [width - i - 1 for i in reversed(range(width // 3))]
            indices = [k for k in indices if k % width not in columns_to_omit]
        return {index: self._time_step(self._page_time + k * step_length) for k, index in }

    @listens('notes')
    def __on_clip_notes_changed(self):
        self._clip_notes = []
        if self._has_clip():
            if self._can_edit():
                start, length = self._get_clip_notes_time_range()
                self._clip_notes = get_notes(self._clip, self._pitches, start, length, self._pitch_provider.is_polyphonic)
        self._update_editor_matrix()
        self.notify_clip_notes()

    @listens('clip')
    def __on_sequencer_clip_changed(self):
        self.set_clip(self._sequencer_clip.clip)

    @listens('target_track.color')
    def __on_target_track_color_changed(self):
        self._update_editor_matrix()

    @listens('pitches')
    def __on_provided_pitches_changed(self, pitches):
        self.set_pitches(pitches)

    @listens('is_polyphonic')
    def __on_provider_polyphony_changed(self, _):
        self._NoteEditorComponent__on_clip_notes_changed()

    @listens('index')
    def __on_resolution_changed(self, *_):
        self._release_active_steps()
        self._update_from_grid()
        self.notify_page_length()
        self._NoteEditorComponent__on_clip_notes_changed()