#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Tranzport/consts.py
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
NOTE_OFF_STATUS = 128
NOTE_ON_STATUS = 144
CC_STATUS = 176
NUM_NOTES = 127
NUM_CC_NO = 127
NUM_CHANNELS = 15
NUM_PAGES = 4
PAGES_NAMES = ((u'P', u'o', u's', u'i', u't', u'i', u'o', u'n', u' ', u'&', u' ', u'T', u'e', u'm', u'p', u'o'),
 (u'C', u'l', u'i', u'p', u' ', u'&', u' ', u'T', u'e', u'm', u'p', u'o'),
 (u'V', u'o', u'l', u'u', u'm', u'e', u' ', u'&', u' ', u'P', u'a', u'n', u'n', u'i', u'n', u'g'),
 (u'L', u'o', u'o', u'p', u' ', u'S', u'e', u't', u't', u'i', u'n', u'g', u's'),
 (u'S', u'e', u'n', u'd', u' ', u'S', u'e', u't', u't', u'i', u'n', u'g', u's'))
TRANZ_NATIVE_MODE = (240, 0, 1, 64, 16, 1, 0, 247)
TRANZ_TRANS_SECTION = list(range(91, 96))
TRANZ_RWD = 91
TRANZ_FFWD = 92
TRANZ_STOP = 93
TRANZ_PLAY = 94
TRANZ_REC = 95
TRANZ_PREV_TRACK = 48
TRANZ_NEXT_TRACK = 49
TRANZ_ARM_TRACK = 0
TRANZ_MUTE_TRACK = 16
TRANZ_SOLO_TRACK = 8
TRANZ_ANY_SOLO = 115
TRANZ_TRACK_SECTION = (TRANZ_PREV_TRACK,
 TRANZ_NEXT_TRACK,
 TRANZ_ARM_TRACK,
 TRANZ_MUTE_TRACK,
 TRANZ_SOLO_TRACK,
 TRANZ_ANY_SOLO)
TRANZ_LOOP = 86
TRANZ_PUNCH_IN = 87
TRANZ_PUNCH_OUT = 88
TRANZ_PUNCH = 120
TRANZ_LOOP_SECTION = (TRANZ_LOOP,
 TRANZ_PUNCH_IN,
 TRANZ_PUNCH_OUT,
 TRANZ_PUNCH)
TRANZ_PREV_CUE = 84
TRANZ_ADD_CUE = 82
TRANZ_NEXT_CUE = 85
TRANZ_CUE_SECTION = (TRANZ_PREV_CUE, TRANZ_ADD_CUE, TRANZ_NEXT_CUE)
TRANZ_UNDO = 76
TRANZ_SHIFT = 121
TRANZ_DICT = {u'0': 48,
 u'1': 49,
 u'2': 50,
 u'3': 51,
 u'4': 52,
 u'5': 53,
 u'6': 54,
 u'7': 55,
 u'8': 56,
 u'9': 57,
 u'A': 65,
 u'B': 66,
 u'C': 67,
 u'D': 68,
 u'E': 69,
 u'F': 70,
 u'G': 71,
 u'H': 72,
 u'I': 73,
 u'J': 74,
 u'K': 75,
 u'L': 76,
 u'M': 77,
 u'N': 78,
 u'O': 79,
 u'P': 80,
 u'Q': 81,
 u'R': 82,
 u'S': 83,
 u'T': 84,
 u'U': 85,
 u'V': 86,
 u'W': 87,
 u'X': 88,
 u'Y': 89,
 u'Z': 90,
 u'a': 97,
 u'b': 98,
 u'c': 99,
 u'd': 100,
 u'e': 101,
 u'f': 102,
 u'g': 103,
 u'h': 104,
 u'i': 105,
 u'j': 106,
 u'k': 107,
 u'l': 108,
 u'm': 109,
 u'n': 110,
 u'o': 111,
 u'p': 112,
 u'q': 113,
 u'r': 114,
 u's': 115,
 u't': 116,
 u'u': 117,
 u'v': 118,
 u'w': 119,
 u'x': 120,
 u'y': 121,
 u'z': 122,
 u'@': 64,
 u' ': 32,
 u'.': 46,
 u',': 44,
 u':': 58,
 u';': 59,
 u'<': 60,
 u'>': 62,
 u'[': 91,
 u']': 93,
 u'_': 95,
 u'-': 16,
 u'|': 124,
 u'&': 38}
SYSEX_START = (240, 0, 1, 64, 16, 0)
SYSEX_END = (247,)
CLEAR_LINE = (32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32)
LED_ON = 127
LED_OFF = 0
