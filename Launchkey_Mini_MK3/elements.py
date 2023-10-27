# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchkey_Mini_MK3\elements.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 682 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import object, range
from novation.launchkey_elements import LaunchkeyElements

class Elements(LaunchkeyElements):

    def __init__(self, *a, **k):
        (super(Elements, self).__init__)(*a, **k)
        self.record_button_with_shift = self.with_shift(self.record_button)
        self.scene_launch_button_with_shift = self.with_shift(self.scene_launch_buttons_raw[0])
        self.stop_solo_mute_button_with_shift = self.with_shift(self.scene_launch_buttons_raw[1])