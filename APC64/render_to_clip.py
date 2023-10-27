# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\APC64\render_to_clip.py
# Compiled at: 2023-09-17 09:50:55
# Size of source mod 2**32: 10336 bytes
from __future__ import absolute_import, print_function, unicode_literals
from typing import NamedTuple
from Live.Clip import MidiNoteSpecification
from ableton.v3.base import depends
from ableton.v3.control_surface import Component
from ableton.v3.control_surface.controls import InputControl
from ableton.v3.control_surface.display import Renderable
from ableton.v3.live import prepare_new_clip_slot
MIN_CLIP_LENGTH = 0.25
WRAPPED_NOTE_OFFSET = 0.01
PPQN_FACTOR = 96
START_MSG_LENGTH = 4
CLIP_LENGTH_SLICE = slice(2, 4)
PAYLOAD_START_INDEX = 2
NOTE_DATA_LENGTH = 4
POSITION_AND_TYPE_SLICE = slice(0, 2)
PITCH_INDEX = 2
VELOCITY_INDEX = 3
EVENT_TYPE_BIT = 13

def sum_bytes(data_bytes):
    return (data_bytes[0] << 7) + data_bytes[1]


def to_absolute_beat_time(ppqn_value):
    return abs(ppqn_value / PPQN_FACTOR)


def get_clip_length(data_bytes):
    return max(MIN_CLIP_LENGTH, to_absolute_beat_time(sum_bytes(data_bytes)))


def get_notes_to_render(note_ons, note_offs, clip_length):
    notes_to_render = []
    for note_on in note_ons:
        for i, note_off in enumerate(note_offs):
            if note_off.pitch == note_on.pitch:
                if note_off.position > note_on.position:
                    if note_off.position <= clip_length:
                        notes_to_render.append(MidiNoteSpecification(pitch=(note_on.pitch),
                          start_time=(note_on.position),
                          duration=(note_off.position - note_on.position),
                          velocity=(note_on.velocity),
                          mute=False))
                    else:
                        notes_to_render.extend(wrap_note(note_on, note_off, clip_length))
                    note_offs.pop(i)
                    break

    return notes_to_render


def wrap_note(note_on, note_off, clip_length):
    end_duration = clip_length - note_on.position
    start_duration = note_off.position - note_on.position - end_duration
    return [
     MidiNoteSpecification(pitch=(note_on.pitch),
       start_time=(-WRAPPED_NOTE_OFFSET),
       duration=(start_duration + WRAPPED_NOTE_OFFSET),
       velocity=(note_on.velocity),
       mute=False),
     MidiNoteSpecification(pitch=(note_on.pitch),
       start_time=(note_on.position),
       duration=(end_duration + WRAPPED_NOTE_OFFSET),
       velocity=(note_on.velocity),
       mute=False)]


def get_firmware_note_data(data_bytes):
    note_ons = []
    note_offs = []
    for index in range(0, len(data_bytes), NOTE_DATA_LENGTH):
        spec = get_firmware_note_specification(data_bytes[index:index + NOTE_DATA_LENGTH])
        if spec.is_note_on:
            note_ons.append(spec)
        else:
            note_offs.append(spec)

    return (
     note_ons, note_offs)


def get_firmware_note_specification(data_bytes):
    position_and_type = sum_bytes(data_bytes[POSITION_AND_TYPE_SLICE])
    event_type = position_and_type & 1 << EVENT_TYPE_BIT
    return FirmwareNoteSpecification(pitch=(data_bytes[PITCH_INDEX]),
      velocity=(data_bytes[VELOCITY_INDEX]),
      position=(to_absolute_beat_time(position_and_type - event_type)),
      is_note_on=(bool(event_type)))


class FirmwareNoteSpecification(NamedTuple):
    pitch: int
    velocity: int
    position: float
    is_note_on: bool


class RenderToClipComponent(Component, Renderable):
    start_control = InputControl()
    data_control = InputControl()
    end_control = InputControl()

    @depends(target_track=None)
    def __init__(self, target_track=None, *a, **k):
        (super().__init__)(a, name='Render_To_Clip', **k)
        self._target_track = target_track
        self._clip_length = MIN_CLIP_LENGTH
        self._note_on_events = []
        self._note_off_events = []

    @start_control.value
    def start_control(self, values, _):
        self._note_on_events = []
        self._note_off_events = []
        if len(values) == START_MSG_LENGTH:
            self._clip_length = get_clip_length(values[CLIP_LENGTH_SLICE])

    @data_control.value
    def data_control(self, values, _):
        if len(values) >= PAYLOAD_START_INDEX:
            payload = values[PAYLOAD_START_INDEX:]
            if len(payload) % NOTE_DATA_LENGTH == 0:
                note_ons, note_offs = get_firmware_note_data(payload)
                self._note_on_events.extend(note_ons)
                self._note_off_events.extend(note_offs)

    @end_control.value
    def end_control(self, *_):
        if self._note_on_events:
            if len(self._note_off_events) >= len(self._note_on_events):
                slot = self._get_slot_for_clip()
                if slot is None:
                    return
                slot.create_clip(self._clip_length)
                slot.clip.add_new_notes(get_notes_to_render(self._note_on_events, self._note_off_events, self._clip_length))
                slot.clip.deselect_all_notes()
                self.song.view.detail_clip = slot.clip
            else:
                self.notify(self.notifications.generic, 'ERROR\nCannot render\nthis sequence')
        else:
            self.notify(self.notifications.generic, 'INFO\nNo notes\nto render')

    def _get_slot_for_clip(self):
        if not self._target_track.target_track.has_midi_input:
            self.notify(self.notifications.generic, 'ERROR\nMIDI Track\nnot selected')
            return
        slot = prepare_new_clip_slot(self._target_track.target_track)
        if slot is None:
            self.notify(self.notifications.generic, 'ERROR\nCannot create\nnew Scene')
            return
        return slot