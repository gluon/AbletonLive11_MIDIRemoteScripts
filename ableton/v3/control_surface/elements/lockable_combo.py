# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\elements\lockable_combo.py
# Compiled at: 2023-08-04 12:30:20
# Size of source mod 2**32: 628 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.elements import ComboElement

class LockableComboElement(ComboElement):

    def _modifier_is_valid(self, mod):
        return self.owns_control_element(mod) and (mod.is_pressed) or ((hasattr(mod, 'is_locked')) and (mod.is_locked))