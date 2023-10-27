# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\KONTROL49\config.py
# Compiled at: 2022-11-29 09:57:02
# Size of source mod 2**32: 5062 bytes
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
  'BANK1': 47,
  'BANK2': 46,
  'BANK3': 45,
  'BANK4': 44,
  'BANK5': 85,
  'BANK6': 86,
  'BANK7': 87,
  'BANK8': 88}
PAD_TRANSLATION = ((0, 0, 61, 9), (1, 0, 69, 9), (2, 0, 65, 9), (3, 0, 63, 9), (0, 1, 60, 9),
                   (1, 1, 59, 9), (2, 1, 57, 9), (3, 1, 55, 9), (0, 2, 49, 9), (1, 2, 51, 9),
                   (2, 2, 68, 9), (3, 2, 56, 9), (0, 3, 48, 9), (1, 3, 52, 9), (2, 3, 54, 9),
                   (3, 3, 58, 9))
CONTROLLER_DESCRIPTIONS = {
  'INPUTPORT': 'KONTROL49 (PORT B)',
  'OUTPUTPORT': 'KONTROL49 (CTRL)',
  'CHANNEL': 7,
  'PAD_TRANSLATION': PAD_TRANSLATION}
MIXER_OPTIONS = {
  'NUMSENDS': 2,
  'SEND1': (-1, -1, -1, -1, -1, -1, -1, -1),
  'SEND2': (-1, -1, -1, -1, -1, -1, -1, -1),
  'MASTERVOLUME': -1}