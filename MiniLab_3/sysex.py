# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\MiniLab_3\sysex.py
# Compiled at: 2022-12-08 12:23:09
# Size of source mod 2**32: 1358 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v3.control_surface.elements import SysexElement as SysexElementBase
from .midi import COMMAND_ID_TO_DAW_PROGRAM_ID

class SysexElement(SysexElementBase):

    def receive_value(self, value):
        if len(value) == 2:
            if value[0] in COMMAND_ID_TO_DAW_PROGRAM_ID:
                super().receive_value(int(value[1] == COMMAND_ID_TO_DAW_PROGRAM_ID[value[0]]))