#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/_Komplete_Kontrol/sysex.py
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface import midi
HEADER = (midi.SYSEX_START,
 0,
 33,
 9,
 0,
 0,
 68,
 67,
 1,
 0)
TRACK_TYPE_DISPLAY_HEADER = HEADER + (64,)
TRACK_CHANGED_DISPLAY_HEADER = HEADER + (65, 0, 0)
TRACK_SELECT_DISPLAY_HEADER = HEADER + (66,)
TRACK_MUTE_DISPLAY_HEADER = HEADER + (67,)
TRACK_SOLO_DISPLAY_HEADER = HEADER + (68,)
TRACK_ARM_DISPLAY_HEADER = HEADER + (69,)
TRACK_VOLUME_DISPLAY_HEADER = HEADER + (70, 0)
TRACK_PANNING_DISPLAY_HEADER = HEADER + (71, 0)
TRACK_NAME_DISPLAY_HEADER = HEADER + (72, 0)
TRACK_METER_DISPLAY_HEADER = HEADER + (73, 2, 0)
TRACK_MUTED_VIA_SOLO_DISPLAY_HEADER = HEADER + (74,)
EMPTY_TRACK_TYPE_VALUE = 0
DEFAULT_TRACK_TYPE_VALUE = 1
MASTER_TRACK_TYPE_VALUE = 6
