# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\SL_MkIII\message.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 552 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface import Component
from .control import TextDisplayControl
NUM_MESSAGE_SEGMENTS = 2

class MessageComponent(Component):
    display = TextDisplayControl(segments=(('', ) * NUM_MESSAGE_SEGMENTS))

    def __call__(self, *messages):
        for index, message in zip(range(NUM_MESSAGE_SEGMENTS), messages):
            self.display[index] = message if message else ''