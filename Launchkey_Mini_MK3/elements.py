from __future__ import absolute_import, print_function, unicode_literals
from builtins import object, range
from novation.launchkey_elements import LaunchkeyElements

class Elements(LaunchkeyElements):

    def __init__(self, *a, **k):
        (super(Elements, self).__init__)(*a, **k)
        self.record_button_with_shift = self.with_shift(self.record_button)
        self.scene_launch_button_with_shift = self.with_shift(self.scene_launch_buttons_raw[0])
        self.stop_solo_mute_button_with_shift = self.with_shift(self.scene_launch_buttons_raw[1])