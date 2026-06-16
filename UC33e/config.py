# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\UC33e\config.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 4492 bytes
from __future__ import absolute_import, print_function, unicode_literals
from .consts import *
TRANSPORT_CONTROLS = {
  'STOP': GENERIC_STOP,
  'PLAY': GENERIC_PLAY,
  'REC': GENERIC_REC,
  'LOOP': GENERIC_LOOP,
  'RWD': GENERIC_RWD,
  'FFWD': GENERIC_FFWD}
DEVICE_CONTROLS = (
 (
  GENERIC_ENC1, 0),
 (
  GENERIC_ENC2, 1),
 (
  GENERIC_ENC3, 2),
 (
  GENERIC_ENC4, 3),
 (
  GENERIC_ENC5, 4),
 (
  GENERIC_ENC6, 5),
 (
  GENERIC_ENC7, 6),
 (
  GENERIC_ENC8, 7))
VOLUME_CONTROLS = (
 (
  GENERIC_SLI1, 0),
 (
  GENERIC_SLI2, 1),
 (
  GENERIC_SLI3, 2),
 (
  GENERIC_SLI4, 3),
 (
  GENERIC_SLI5, 4),
 (
  GENERIC_SLI6, 5),
 (
  GENERIC_SLI7, 6),
 (
  GENERIC_SLI8, 7))
TRACKARM_CONTROLS = (
 GENERIC_BUT1,
 GENERIC_BUT2,
 GENERIC_BUT3,
 GENERIC_BUT4,
 GENERIC_BUT5,
 GENERIC_BUT6,
 GENERIC_BUT7,
 GENERIC_BUT8)
BANK_CONTROLS = {
  'TOGGLELOCK': GENERIC_BUT9,
  'BANKDIAL': -1,
  'NEXTBANK': GENERIC_PAD5,
  'PREVBANK': GENERIC_PAD1,
  'BANK1': -1,
  'BANK2': -1,
  'BANK3': -1,
  'BANK4': -1,
  'BANK5': -1,
  'BANK6': -1,
  'BANK7': -1,
  'BANK8': -1}
CONTROLLER_DESCRIPTIONS = {'INPUTPORT':'UC-33 USB MIDI Controller (Port 1)', 
 'OUTPUTPORT':'UC-33 USB MIDI Controller (Port 1)', 
 'CHANNEL':0}
MIXER_OPTIONS = {
  'NUMSENDS': 2,
  'SEND1': (-1, -1, -1, -1, -1, -1, -1, -1),
  'SEND2': (-1, -1, -1, -1, -1, -1, -1, -1),
  'MASTERVOLUME': 28}