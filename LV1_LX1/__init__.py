# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/LV1_LX1/__init__.py
# Compiled at: 2021-06-29 09:33:48
# Size of source mod 2**32: 169 bytes
from __future__ import absolute_import, print_function, unicode_literals
from .LV1_LX1 import LV1_LX1

def create_instance(c_instance):
    return LV1_LX1(c_instance)