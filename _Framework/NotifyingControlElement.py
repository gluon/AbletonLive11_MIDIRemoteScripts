from __future__ import absolute_import, print_function, unicode_literals
from .ControlElement import ControlElement
from .SubjectSlot import Subject, SubjectEvent

class NotifyingControlElement(Subject, ControlElement):
    __subject_events__ = (
     SubjectEvent(name='value',
       doc=' Called when the control element receives a MIDI value\n                             from the hardware '),)