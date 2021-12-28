#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/novation/print_to_clip.py
from __future__ import absolute_import, print_function, unicode_literals
from __future__ import division
from builtins import range
from past.utils import old_div
from builtins import object
import Live
from operator import itemgetter
from ableton.v2.base import listens, liveobj_valid, task
from ableton.v2.control_surface import Component
from ableton.v2.control_surface.control import InputControl, SendValueControl

class MessageType(object):
    u"""
    The type of SysEx messages used in content transfers.
    """
    begin = 1
    data = 2
    end = 3


class Note(object):
    u"""
    The indexes of information about notes within note tuples.
    """
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
LIMITATION_ERROR_MESSAGE = u'Print to clip failed: No more scenes can be inserted for this version of Live.'
PACKET_ERROR_MESSAGE = u'Print to clip failed: Transmission error detected. Please try again.'

def sum_multi_byte_value(data_bytes, bits_per_byte = 7):
    return sum([ b << i * bits_per_byte for i, b in enumerate(reversed(data_bytes)) ])


def to_absolute_beat_time(data_bytes):
    return old_div(sum_multi_byte_value(data_bytes), TIME_FACTOR)


def create_note(note_data, start_offset):
    return (note_data[PITCH_INDEX],
     to_absolute_beat_time(note_data[START_POSITION_SLICE]) + start_offset,
     to_absolute_beat_time(note_data[LENGTH_SLICE]),
     note_data[VELOCITY_INDEX],
     False)


class PrintToClipComponent(Component):
    u"""
    Component that handles the print to clip functionality (whereby we receive SysEx
    messages that represent note data to write to a MIDI clip in Live) and workflow for
    Novation products.
    
    The print to clip SysEx API is as follows.
    
    CONTENT TRANSFER SYSEX MESSAGE FORMAT
    --------------------------------------------------------------------------------------
    | BYTE(S)             |  DESCRIPTION
    --------------------------------------------------------------------------------------
    | Message Type (0)    |  0x01 - Begin transfer
    |                     |
    |                     |  Indicates the start of a transfer.
    |                     |
    |                     |  0x02 - Data packet
    |                     |
    |                     |  Packet of data as part of the transfer.
    |                     |
    |                     |  0x03 - End transfer
    |                     |
    |                     |  Indicates the end of a transfer.
    |                     |
    --------------------------------------------------------------------------------------
    | Packet ID (1 - 8)   |  8 bytes indicating the packet ID as an integer. This will
    |                     |  be 0 for the Begin Transfer Message Type and increase by 1
    |                     |  for each subsequent packet.
    |                     |
    |                     |  This is used to validate that no packets were lost in the
    |                     |  transfer.
    |                     |
    --------------------------------------------------------------------------------------
    | Content Type (9)    |  Not used.
    |                     |
     --------------------------------------------------------------------------------------
    | Content Index (10)  |  Not used.
    |                     |
    --------------------------------------------------------------------------------------
    | Payload (11 - ?)    |  Multiple bytes that depend on the Message Type. The only
    |                     |  payload we care about is that of data packets. The contents
    |                     |  of those is described in the next table.
    |                     |
    --------------------------------------------------------------------------------------
    
    NOTES:
    A content transfer complete with note data requires at least 4 SysEx messages:
    - Begin transfer
    - Data packet containing note data
    - Data packet containing the end time of the clip to create
    - End transfer
    
    A content transfer without note data requires 3 messages and will create an empty clip:
    - Begin transfer
    - Data packet containing the end time of the clip to create
    - End transfer
    
    
    DATA PACKET FORMAT FOR PRINT TO CLIP
    --------------------------------------------------------------------------------------
    | BYTE(S)               |  DESCRIPTION
    --------------------------------------------------------------------------------------
    | Group Offset (0 - 2)  |  Specifies either the starting offset for all of the notes
    |                       |  that follow or the absolute length of the clip to create.
    |                       |
    |                       |  In the case of the latter, this will be the only bytes
    |                       |  we deal with.
    |                       |
    --------------------------------------------------------------------------------------
    | Start Time (3 - 4)    |  The start time of the note relative to the Group Offset.
    |                       |
    --------------------------------------------------------------------------------------
    | Length (5 - 6)        |  The length of the note.
    |                       |
    --------------------------------------------------------------------------------------
    | Pitch (7)             |  The pitch of the note.
    |                       |
    --------------------------------------------------------------------------------------
    | Velocity (8)          |  The velocity of the note.
    |                       |
    --------------------------------------------------------------------------------------
    
    NOTES:
    - Timing information is in ms and based on a tempo of 120 BPM.
    - Aside from the Group Offset, all other bytes can be repeated any number of times.
    """
    print_to_clip_control = InputControl()
    print_to_clip_enabler = SendValueControl()

    def __init__(self, *a, **k):
        super(PrintToClipComponent, self).__init__(*a, **k)
        self._clip_data = {}
        self._last_packet_id = -1
        self._reset_last_packet_id_task = self._tasks.add(task.sequence(task.wait(RESET_PACKET_ID_TASK_DELAY), task.run(self._reset_last_packet_id)))
        self._reset_last_packet_id_task.kill()
        self.__on_selected_track_changed.subject = self.song.view
        self.__on_selected_track_changed()

    @print_to_clip_control.value
    def print_to_clip_control(self, data_bytes, _):
        self._reset_last_packet_id_task.restart()
        packet_id = sum_multi_byte_value(data_bytes[PACKET_ID_SLICE], bits_per_byte=4)
        if packet_id != 0 and packet_id - 1 != self._last_packet_id:
            self.show_message(PACKET_ERROR_MESSAGE)
            return
        num_bytes = len(data_bytes)
        transfer_type = data_bytes[MESSAGE_TYPE_INDEX]
        if transfer_type == MessageType.begin:
            self._clip_data = {u'notes': []}
        elif transfer_type == MessageType.data and num_bytes >= MIN_DATA_PACKET_LENGTH:
            self._handle_data_packet(data_bytes)
        elif transfer_type == MessageType.end:
            self._print_data_to_clip()
        self._last_packet_id = packet_id

    def _handle_data_packet(self, data_bytes):
        payload = data_bytes[PAYLOAD_START_INDEX:]
        if len(payload) == BYTES_PER_GROUP_OFFSET:
            self._clip_data[u'length'] = to_absolute_beat_time(payload)
        else:
            group_offset = to_absolute_beat_time(payload[:BYTES_PER_GROUP_OFFSET])
            payload = payload[BYTES_PER_GROUP_OFFSET:]
            payload_length = len(payload)
            if payload_length % BYTES_PER_NOTE == 0:
                self._clip_data[u'notes'].extend([ create_note(payload[i:i + BYTES_PER_NOTE], group_offset) for i in range(0, payload_length, BYTES_PER_NOTE) ])

    def _reset_last_packet_id(self):
        self._last_packet_id = -1

    def _print_data_to_clip(self):
        if u'length' in self._clip_data:
            clip = self._create_clip(self._clip_data[u'length'])
            if liveobj_valid(clip):
                self._wrap_trailing_notes()
                note_data = sorted(self._clip_data[u'notes'], key=itemgetter(1))
                notes = tuple((Live.Clip.MidiNoteSpecification(pitch=note[Note.pitch], start_time=note[Note.start], duration=note[Note.length], velocity=note[Note.velocity], mute=note[Note.mute]) for note in note_data))
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
            return None

    def _wrap_trailing_notes(self):
        for note in self._clip_data[u'notes'][:]:
            note_end_position = note[Note.start] + note[Note.length]
            if note_end_position > self._clip_data[u'length']:
                wrapped_note_length = note_end_position - self._clip_data[u'length'] + WRAPPED_NOTE_OFFSET
                self._clip_data[u'notes'].append((note[Note.pitch],
                 -WRAPPED_NOTE_OFFSET,
                 wrapped_note_length,
                 note[Note.velocity],
                 note[Note.mute]))

    @listens(u'selected_track')
    def __on_selected_track_changed(self):
        can_print = self.song.view.selected_track.has_midi_input
        self.print_to_clip_control.enabled = can_print
        self.print_to_clip_enabler.value = int(can_print)
