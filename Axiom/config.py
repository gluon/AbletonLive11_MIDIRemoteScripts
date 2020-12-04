#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Axiom/config.py
from __future__ import absolute_import, print_function, unicode_literals
from .consts import *
from _Axiom.consts import PAD_TRANSLATION
TRANSPORT_CONTROLS = {u'STOP': GENERIC_STOP,
 u'PLAY': GENERIC_PLAY,
 u'REC': GENERIC_REC,
 u'LOOP': GENERIC_LOOP,
 u'RWD': GENERIC_RWD,
 u'FFWD': GENERIC_FFWD}
DEVICE_CONTROLS = (GENERIC_ENC5,
 GENERIC_ENC6,
 GENERIC_ENC7,
 GENERIC_ENC8,
 GENERIC_ENC1,
 GENERIC_ENC2,
 GENERIC_ENC3,
 GENERIC_ENC4)
VOLUME_CONTROLS = GENERIC_SLIDERS
TRACKARM_CONTROLS = (GENERIC_BUT1,
 GENERIC_BUT2,
 GENERIC_BUT3,
 GENERIC_BUT4,
 GENERIC_BUT5,
 GENERIC_BUT6,
 GENERIC_BUT7,
 GENERIC_BUT8)
BANK_CONTROLS = {u'TOGGLELOCK': GENERIC_BUT9,
 u'BANKDIAL': -1,
 u'NEXTBANK': -1,
 u'PREVBANK': -1,
 u'BANK1': -1,
 u'BANK2': -1,
 u'BANK3': -1,
 u'BANK4': -1,
 u'BANK5': -1,
 u'BANK6': -1,
 u'BANK7': -1,
 u'BANK8': -1}
CONTROLLER_DESCRIPTION = {u'INPUTPORT': u'USB Axiom',
 u'OUTPUTPORT': u'USB Axiom',
 u'CHANNEL': 0,
 u'PAD_TRANSLATION': PAD_TRANSLATION}
MIXER_OPTIONS = {u'NUMSENDS': 2,
 u'SEND1': (-1, -1, -1, -1, -1, -1, -1, -1),
 u'SEND2': (-1, -1, -1, -1, -1, -1, -1, -1),
 u'MASTERVOLUME': GENERIC_SLI9}
