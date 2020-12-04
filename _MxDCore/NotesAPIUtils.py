#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/_MxDCore/NotesAPIUtils.py
from __future__ import absolute_import, print_function, unicode_literals
REQUIRED_MIDI_NOTE_ATTRS = (u'pitch', u'start_time', u'duration')

def midi_note_to_dict(note):
    return {u'note_id': note.note_id,
     u'pitch': note.pitch,
     u'start_time': note.start_time,
     u'duration': note.duration,
     u'velocity': note.velocity,
     u'mute': int(note.mute),
     u'probability': note.probability,
     u'velocity_deviation': note.velocity_deviation,
     u'release_velocity': note.release_velocity}


def midi_notes_to_notes_dict(notes):
    return {u'notes': [ midi_note_to_dict(note) for note in notes ]}


def verify_note_specification_requirements(note_specification):
    missing_keys = set(REQUIRED_MIDI_NOTE_ATTRS) - set(note_specification.keys())
    if len(missing_keys) > 0:
        raise RuntimeError(u'Missing required keys: ', u', '.join(missing_keys))
