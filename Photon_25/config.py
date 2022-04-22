# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Photon_25/config.py
# Compiled at: 2022-01-27 16:28:16
# Size of source mod 2**32: 4270 bytes
from __future__ import absolute_import, print_function, unicode_literals
from .consts import *
TRANSPORT_CONTROLS = {'STOP':GENERIC_STOP, 
 'PLAY':GENERIC_PLAY, 
 'REC':GENERIC_REC, 
 'LOOP':GENERIC_LOOP, 
 'RWD':GENERIC_RWD, 
 'FFWD':GENERIC_FFWD}
DEVICE_CONTROLS = (
 GENERIC_ENC1,
 GENERIC_ENC2,
 GENERIC_ENC3,
 GENERIC_ENC4,
 GENERIC_ENC5,
 GENERIC_ENC6,
 GENERIC_ENC7,
 GENERIC_ENC8)
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
 'BANK1':-1, 
 'BANK2':-1, 
 'BANK3':-1, 
 'BANK4':-1, 
 'BANK5':-1, 
 'BANK6':-1, 
 'BANK7':-1, 
 'BANK8':-1}
CONTROLLER_DESCRIPTIONS = {'INPUTPORT':'Photon 25', 
 'OUTPUTPORT':'Photon 25', 
 'CHANNEL':0}
MIXER_OPTIONS = {'NUMSENDS':2, 
 'SEND1':(-1, -1, -1, -1, -1, -1, -1, -1), 
 'SEND2':(-1, -1, -1, -1, -1, -1, -1, -1), 
 'MASTERVOLUME':-1}