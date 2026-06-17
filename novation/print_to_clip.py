# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\novation\print_to_clip.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 12661 bytes
from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import object, range
from past.utils import old_div
from operator import itemgetter
import Live
from ableton.v2.base import listens, liveobj_valid, task
from ableton.v2.control_surface import Component
from ableton.v2.control_surface.control import InputControl, SendValueControl

class MessageType(object):
    begin = 1
    data = 2
    end = 3


class Note(object):
    pitch = 0
    start = 1
    length = 2
    velocity = 3
    mute = 4


MESSAGE_TYPE_INDEX = 0
PACKET_ID_SLICE = slice(1, 9)
PAYLOAD_START_INDEX = 11
START_POSITION_SLICE = slice(0, 2)
LENGTH_SLICE = slice(2, 4)
PITCH_INDEX = 4
VELOCITY_INDEX = 5
MIN_DATA_PACKET_LENGTH = 13
BYTES_PER_GROUP_OFFSET = 3
BYTES_PER_NOTE = 6
TIME_FACTOR = 500.0
RESET_PACKET_ID_TASK_DELAY = 0.1
WRAPPED_NOTE_OFFSET = 0.1
LIMITATION_ERROR_MESSAGE = 'Print to clip failed: No more scenes can be inserted for this version of Live.'
PACKET_ERROR_MESSAGE = 'Print to clip failed: Transmission error detected. Please try again.'

def sum_multi_byte_value(data_bytes, bits_per_byte=7):
    return sum([b << i * bits_per_byte for i, b in enumerate(reversed(data_bytes))])


def to_absolute_beat_time(data_bytes):
    return old_div(sum_multi_byte_value(data_bytes), TIME_FACTOR)


def create_note(note_data, start_offset):
    return (
     note_data[PITCH_INDEX],
     to_absolute_beat_time(note_data[START_POSITION_SLICE]) + start_offset,
     to_absolute_beat_time(note_data[LENGTH_SLICE]),
     note_data[VELOCITY_INDEX],
     False)


class PrintToClipComponent(Component):
    print_to_clip_control = InputControl()
    print_to_clip_enabler = SendValueControl()

    def __init__(self, *a, **k):
        (super(PrintToClipComponent, self).__init__)(*a, **k)
        self._clip_data = {}
        self._last_packet_id = -1
        self._reset_last_packet_id_task = self._tasks.add(task.sequence(task.wait(RESET_PACKET_ID_TASK_DELAY), task.run(self._reset_last_packet_id)))
        self._reset_last_packet_id_task.kill()
        self._PrintToClipComponent__on_selected_track_changed.subject = self.song.view
        self._PrintToClipComponent__on_selected_track_changed()

    @print_to_clip_control.value
    def print_to_clip_control(self, data_bytes, _):
        self._reset_last_packet_id_task.restart()
        packet_id = sum_multi_byte_value((data_bytes[PACKET_ID_SLICE]), bits_per_byte=4)
        if packet_id != 0:
            if packet_id - 1 != self._last_packet_id:
                self.show_message(PACKET_ERROR_MESSAGE)
                return
        num_bytes = len(data_bytes)
        transfer_type = data_bytes[MESSAGE_TYPE_INDEX]
        if transfer_type == MessageType.begin:
            self._clip_data = {'notes': []}
        else:
            if transfer_type == MessageType.data and num_bytes >= MIN_DATA_PACKET_LENGTH:
                self._handle_data_packet(data_bytes)
            else:
                if transfer_type == MessageType.end:
                    self._print_data_to_clip()
        self._last_packet_id = packet_id

    def _handle_data_packet(self, data_bytes):
        payload = data_bytes[PAYLOAD_START_INDEX:]
        if len(payload) == BYTES_PER_GROUP_OFFSET:
            self._clip_data['length'] = to_absolute_beat_time(payload)
        else:
            group_offset = to_absolute_beat_time(payload[:BYTES_PER_GROUP_OFFSET])
            payload = payload[BYTES_PER_GROUP_OFFSET:]
            payload_length = len(payload)
            if payload_length % BYTES_PER_NOTE == 0:
                self._clip_data['notes'].extend([create_note(payload[i:i + BYTES_PER_NOTE], group_offset) for i in range(0, payload_length, BYTES_PER_NOTE)])

    def _reset_last_packet_id(self):
        self._last_packet_id = -1

    def _print_data_to_clip(self):
        if 'length' in self._clip_data:
            clip = self._create_clip(self._clip_data['length'])
            if liveobj_valid(clip):
                self._wrap_trailing_notes()
                note_data = sorted((self._clip_data['notes']), key=(itemgetter(1)))
                notes = tuple((Live.Clip.MidiNoteSpecification(pitch=(note[Note.pitch]), start_time=(note[Note.start]), duration=(note[Note.length]), velocity=(note[Note.velocity]), mute=(note[Note.mute])) for note in note_data))
                clip.add_new_notes(notes)

    def _create_clip(self, length):
        song = self.song
        view = song.view
        track = view.selected_track
        try:
            scene_index = list(song.scenes).index(view.selected_scene)
            scene_count = len(song.scenes)
            while track.clip_slots[scene_index].has_clip:
                scene_index += 1
                if scene_index == scene_count:
                    song.create_scene(scene_count)

            slot = track.clip_slots[scene_index]
            slot.create_clip(length)
            return slot.clip
        except Live.Base.LimitationError:
            self.show_message(LIMITATION_ERROR_MESSAGE)
            return

    def _wrap_trailing_notes(self):
        for note in self._clip_data['notes'][:]:
            note_end_position = note[Note.start] + note[Note.length]
            if note_end_position > self._clip_data['length']:
                wrapped_note_length = note_end_position - self._clip_data['length'] + WRAPPED_NOTE_OFFSET
                self._clip_data['notes'].append((
                 note[Note.pitch],
                 -WRAPPED_NOTE_OFFSET,
                 wrapped_note_length,
                 note[Note.velocity],
                 note[Note.mute]))

    @listens('selected_track')
    def __on_selected_track_changed(self):
        can_print = self.song.view.selected_track.has_midi_input
        self.print_to_clip_control.enabled = can_print
        self.print_to_clip_enabler.value = int(can_print)