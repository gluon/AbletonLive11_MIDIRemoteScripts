#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/pushbase/melodic_pattern.py
from __future__ import absolute_import, print_function, unicode_literals
from __future__ import division
from builtins import str
from builtins import range
from past.utils import old_div
from ableton.v2.base import NamedTuple, lazy_attribute, memoize, find_if
from . import consts
from .matrix_maps import FEEDBACK_CHANNELS
import Live
CIRCLE_OF_FIFTHS = tuple([ 7 * k % 12 for k in range(12) ])
ROOT_NOTES = CIRCLE_OF_FIFTHS[0:6] + CIRCLE_OF_FIFTHS[-1:5:-1]
NOTE_NAMES = (u'C', u'D\u266d', u'D', u'E\u266d', u'E', u'F', u'G\u266d', u'G', u'A\u266d', u'A', u'B\u266d', u'B')

def pitch_index_to_string(index):
    if index is not None and 0 <= index < 128:
        return NOTE_NAMES[index % 12] + str(old_div(index, 12) - 2)
    return consts.CHAR_ELLIPSIS


class Scale(NamedTuple):
    name = u''
    notes = []

    def to_root_note(self, root_note):
        return Scale(name=NOTE_NAMES[root_note], notes=[ root_note + x for x in self.notes ])

    @memoize
    def scale_for_notes(self, notes):
        return [ self.to_root_note(b) for b in notes ]

    def __unicode__(self):
        return self.name

    def __str__(self):
        return str(self.name)

    def __eq__(self, other):
        if isinstance(other, Scale):
            return self.name == other.name and self.notes == other.notes
        return False

    def __hash__(self):
        return hash((self.name,))


SCALES = tuple([ Scale(name=x[0], notes=x[1]) for x in Live.Song.get_all_scales_ordered() ])

def scale_by_name(name):
    return find_if(lambda m: m.name == name, SCALES)


class NoteInfo(NamedTuple):
    index = None
    channel = 0
    color = u'NoteInvalid'


class MelodicPattern(NamedTuple):
    steps = [0, 0]
    scale = list(range(12))
    root_note = 0
    origin = [0, 0]
    chromatic_mode = False
    width = None
    height = None

    @lazy_attribute
    def extended_scale(self):
        if self.chromatic_mode:
            first_note = self.scale[0]
            return list(range(first_note, first_note + 12))
        else:
            return self.scale

    @property
    def is_aligned(self):
        return not self.origin[0] and not self.origin[1] and abs(self.root_note) % 12 == self.extended_scale[0]

    def note(self, x, y):
        if not self._boundary_reached(x, y):
            channel = y % len(FEEDBACK_CHANNELS) + FEEDBACK_CHANNELS[0]
            return self._get_note_info(self._octave_and_note(x, y), self.root_note, channel)
        return NoteInfo()

    def __getitem__(self, i):
        root_note = self.root_note
        if root_note <= -12:
            root_note = 0 if self.is_aligned else -12
        return self._get_note_info(self._octave_and_note_linear(i), root_note)

    def _boundary_reached(self, x, y):
        return self.width is not None and x >= self.width or self.height is not None and y >= self.height

    def _octave_and_note_by_index(self, index):
        scale = self.extended_scale
        scale_size = len(scale)
        octave = old_div(index, scale_size)
        note = scale[index % scale_size]
        return (octave, note)

    def _octave_and_note(self, x, y):
        index = self.steps[0] * (self.origin[0] + x) + self.steps[1] * (self.origin[1] + y)
        return self._octave_and_note_by_index(index)

    def _color_for_note(self, note):
        if note == self.scale[0]:
            return u'NoteBase'
        elif note in self.scale:
            return u'NoteScale'
        else:
            return u'NoteNotScale'

    def _get_note_info(self, octave_note, root_note, channel = 0):
        octave, note = octave_note
        note_index = 12 * octave + note + root_note
        if 0 <= note_index <= 127:
            return NoteInfo(index=note_index, channel=channel, color=self._color_for_note(note))
        else:
            return NoteInfo()

    def _octave_and_note_linear(self, i):
        origin = self.origin[0] or self.origin[1]
        index = origin + i
        return self._octave_and_note_by_index(index)
