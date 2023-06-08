from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.elements import SysexElement

class IdentifyingSysexElement(SysexElement):

    def receive_value(self, _):
        value = self._msg_sysex_identifier[3]
        self.notify_value(value)