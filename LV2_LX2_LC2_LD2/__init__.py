# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\LV2_LX2_LC2_LD2\__init__.py
# Compiled at: 2022-11-29 09:57:02
# Size of source mod 2**32: 215 bytes
from __future__ import absolute_import, print_function, unicode_literals
import Live
from .LV2_LX2_LC2_LD2 import LV2_LX2_LC2_LD2

def create_instance(c_instance):
    return LV2_LX2_LC2_LD2(c_instance)