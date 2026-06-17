# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\APC20\BackgroundComponent.py
# Compiled at: 2022-11-28 08:01:31
# Size of source mod 2**32: 611 bytes
from __future__ import absolute_import, print_function, unicode_literals
from _Framework.BackgroundComponent import BackgroundComponent as BackgroundComponentBase
from _Framework.Util import nop

class BackgroundComponent(BackgroundComponentBase):

    def _clear_control(self, name, control):
        if control:
            control.add_value_listener(nop)
        else:
            if name in self._control_map:
                self._control_map[name].remove_value_listener(nop)
        super(BackgroundComponent, self)._clear_control(name, control)