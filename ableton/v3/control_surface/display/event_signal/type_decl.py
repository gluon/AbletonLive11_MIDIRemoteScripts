# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\display\event_signal\type_decl.py
# Compiled at: 2023-06-08 07:52:37
# Size of source mod 2**32: 516 bytes
from __future__ import absolute_import, print_function, unicode_literals
from typing import Callable, TypeVar
from ..state import State
from ..type_decl import Event
EventSignalDataType = TypeVar('EventSignalDataType')
EventSignalFn = Callable[([State, Event], EventSignalDataType)]