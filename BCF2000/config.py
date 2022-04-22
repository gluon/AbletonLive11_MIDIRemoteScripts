# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/BCF2000/config.py
# Compiled at: 2022-01-27 16:28:16
# Size of source mod 2**32: 4291 bytes
from __future__ import absolute_import, print_function, unicode_literals
from .consts import *
TRANSPORT_CONTROLS = {'STOP':GENERIC_STOP, 
 'PLAY':GENERIC_PLAY, 
 'REC':GENERIC_REC, 
 'LOOP':GENERIC_LOOP, 
 'RWD':GENERIC_RWD, 
 'FFWD':GENERIC_FFWD}
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
  GENERIC_SLI1, -1),
 (
  GENERIC_SLI2, -1),
 (
  GENERIC_SLI3, -1),
 (
  GENERIC_SLI4, -1),
 (
  GENERIC_SLI5, -1),
 (
  GENERIC_SLI6, -1),
 (
  GENERIC_SLI7, -1),
 (
  GENERIC_SLI8, -1))
TRACKARM_CONTROLS = (
 GENERIC_BUT1,
 GENERIC_BUT2,
 GENERIC_BUT3,
 GENERIC_BUT4,
 GENERIC_BUT5,
 GENERIC_BUT6,
 GENERIC_BUT7,
 GENERIC_BUT8)
BANK_CONTROLS = {'TOGGLELOCK':GENERIC_BUT9, 
 'BANKDIAL':-1, 
 'NEXTBANK':GENERIC_PAD5, 
 'PREVBANK':GENERIC_PAD1, 
 'BANK1':65, 
 'BANK2':66, 
 'BANK3':67, 
 'BANK4':68, 
 'BANK5':69, 
 'BANK6':70, 
 'BANK7':71, 
 'BANK8':72}
CONTROLLER_DESCRIPTIONS = {'INPUTPORT':'BCF2000', 
 'OUTPUTPORT':'BCF2000',  'CHANNEL':0}
MIXER_OPTIONS = {'NUMSENDS':2, 
 'SEND1':(-1, -1, -1, -1, -1, -1, -1, -1), 
 'SEND2':(-1, -1, -1, -1, -1, -1, -1, -1), 
 'MASTERVOLUME':-1}