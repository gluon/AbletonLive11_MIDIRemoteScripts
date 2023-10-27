# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\elements\touch.py
# Compiled at: 2023-06-30 09:18:52
# Size of source mod 2**32: 1950 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ...base import listenable_property, listens
from ...live import song
from . import ButtonElement

class TouchElement(ButtonElement):
    __events__ = ('assignment', )

    def __init__(self, *a, encoder=None, **k):
        (super().__init__)(*a, **k)
        self._TouchElement__on_parameter_changed.subject = encoder
        self._TouchElement__on_parameter_name_changed.subject = encoder
        self._TouchElement__on_parameter_value_changed.subject = encoder
        self._encoder = encoder

    @listenable_property
    def controlled_parameter(self):
        return self._encoder.mapped_object

    def receive_value(self, value):
        super().receive_value(value)
        if value:
            song().begin_undo_step()
        else:
            song().end_undo_step()

    @listens('parameter')
    def __on_parameter_changed(self):
        self.notify_assignment()

    @listens('parameter_name')
    def __on_parameter_name_changed(self):
        self.notify_controlled_parameter()

    @listens('parameter_value')
    def __on_parameter_value_changed(self):
        self.notify_controlled_parameter()