# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\MPD18\config.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 5264 bytes
from __future__ import absolute_import, print_function, unicode_literals
from .consts import *
TRANSPORT_CONTROLS = {
  'STOP': GENERIC_STOP,
  'PLAY': GENERIC_PLAY,
  'REC': GENERIC_REC,
  'LOOP': GENERIC_LOOP,
  'RWD': GENERIC_RWD,
  'FFWD': GENERIC_FFWD,
  'NORELEASE': 0}
DEVICE_CONTROLS = (
 (
  GENERIC_ENC1, 0),
 (
  GENERIC_ENC2, 0),
 (
  GENERIC_ENC3, 0),
 (
  GENERIC_ENC4, 0),
 (
  GENERIC_ENC5, 0),
 (
  GENERIC_ENC6, 0),
 (
  GENERIC_ENC7, 0),
 (
  GENERIC_ENC8, 0))
VOLUME_CONTROLS = (
 (
  GENERIC_SLI1, 0),
 (
  GENERIC_SLI2, 0),
 (
  GENERIC_SLI3, 0),
 (
  GENERIC_SLI4, 0),
 (
  GENERIC_SLI5, 0),
 (
  GENERIC_SLI6, 0),
 (
  GENERIC_SLI7, 0),
 (
  GENERIC_SLI8, 0))
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
PAD_TRANSLATION = ((0, 0, 48, 0), (1, 0, 49, 0), (2, 0, 50, 0), (3, 0, 51, 0), (0, 1, 44, 0),
                   (1, 1, 45, 0), (2, 1, 46, 0), (3, 1, 47, 0), (0, 2, 40, 0), (1, 2, 41, 0),
                   (2, 2, 42, 0), (3, 2, 43, 0), (0, 3, 36, 0), (1, 3, 37, 0), (2, 3, 38, 0),
                   (3, 3, 39, 0))
CONTROLLER_DESCRIPTION = {
  'INPUTPORT': 'Akai MPD18',
  'OUTPUTPORT': 'Akai MPD18',
  'CHANNEL': 0,
  'PAD_TRANSLATION': PAD_TRANSLATION}
MIXER_OPTIONS = {
  'NUMSENDS': 2,
  'SEND1': (-1, -1, -1, -1, -1, -1, -1, -1),
  'SEND2': (-1, -1, -1, -1, -1, -1, -1, -1),
  'MASTERVOLUME': 1}