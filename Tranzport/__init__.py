# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Tranzport/__init__.py
# Compiled at: 2021-11-23 12:54:43
# Size of source mod 2**32: 834 bytes
from __future__ import absolute_import, print_function, unicode_literals
from .Tranzport import Tranzport

def create_instance(c_instance):
    return Tranzport(c_instance)


def exit_instance():
    pass