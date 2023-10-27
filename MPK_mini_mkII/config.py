# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\MPK_mini_mkII\config.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 4791 bytes
from __future__ import absolute_import, print_function, unicode_literals
from .consts import *
TRANSPORT_CONTROLS = {
  'STOP': -1,
  'PLAY': -1,
  'REC': -1,
  'LOOP': -1,
  'RWD': -1,
  'FFWD': -1}
DEVICE_CONTROLS = (
 GENERIC_ENC1,
 GENERIC_ENC2,
 GENERIC_ENC3,
 GENERIC_ENC4,
 GENERIC_ENC5,
 GENERIC_ENC6,
 GENERIC_ENC7,
 GENERIC_ENC8)
VOLUME_CONTROLS = ((-1, -1), (-1, -1), (-1, -1), (-1, -1), (-1, -1), (-1, -1), (-1, -1),
                   (-1, -1))
TRACKARM_CONTROLS = (-1, -1, -1, -1, -1, -1, -1, -1)
BANK_CONTROLS = {
  'TOGGLELOCK': -1,
  'BANKDIAL': -1,
  'NEXTBANK': -1,
  'PREVBANK': -1,
  'BANK1': -1,
  'BANK2': -1,
  'BANK3': -1,
  'BANK4': -1,
  'BANK5': -1,
  'BANK6': -1,
  'BANK7': -1,
  'BANK8': -1}
PAD_TRANSLATION = ((0, 0, 40, 9), (1, 0, 38, 9), (2, 0, 46, 9), (3, 0, 44, 9), (0, 1, 37, 9),
                   (1, 1, 36, 9), (2, 1, 42, 9), (3, 1, 82, 9), (0, 2, 49, 9), (1, 2, 55, 9),
                   (2, 2, 51, 9), (3, 2, 53, 9), (0, 3, 48, 9), (1, 3, 47, 9), (2, 3, 45, 9),
                   (3, 3, 43, 9))
CONTROLLER_DESCRIPTION = {
  'INPUTPORT': 'MPK mini',
  'OUTPUTPORT': 'MPK mini',
  'CHANNEL': -1,
  'PAD_TRANSLATION': PAD_TRANSLATION}
MIXER_OPTIONS = {
  'NUMSENDS': 2,
  'SEND1': (-1, -1, -1, -1, -1, -1, -1, -1),
  'SEND2': (-1, -1, -1, -1, -1, -1, -1, -1),
  'MASTERVOLUME': -1}