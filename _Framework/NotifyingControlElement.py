# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_Framework\NotifyingControlElement.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 599 bytes
from __future__ import absolute_import, print_function, unicode_literals
from .ControlElement import ControlElement
from .SubjectSlot import Subject, SubjectEvent

class NotifyingControlElement(Subject, ControlElement):
    __subject_events__ = (
     SubjectEvent(name='value',
       doc=' Called when the control element receives a MIDI value\n                             from the hardware '),)