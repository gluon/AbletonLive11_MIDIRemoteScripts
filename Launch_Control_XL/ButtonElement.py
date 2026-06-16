# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launch_Control_XL\ButtonElement.py
# Compiled at: 2022-11-29 09:57:02
# Size of source mod 2**32: 972 bytes
from __future__ import absolute_import, print_function, unicode_literals
from _Framework.ButtonElement import OFF_VALUE, ON_VALUE
from _Framework.ButtonElement import ButtonElement as ButtonElementBase

class ButtonElement(ButtonElementBase):
    _on_value = None
    _off_value = None

    def reset(self):
        self._on_value = None
        self._off_value = None
        super(ButtonElement, self).reset()

    def set_on_off_values(self, on_value, off_value):
        self._on_value = on_value
        self._off_value = off_value

    def send_value(self, value, **k):
        if value is ON_VALUE and self._on_value is not None:
            self._skin[self._on_value].draw(self)
        else:
            if value is OFF_VALUE and self._off_value is not None:
                self._skin[self._off_value].draw(self)
            else:
                (super(ButtonElement, self).send_value)(value, **k)