from __future__ import absolute_import, print_function, unicode_literals
from .simple_display import SimpleDisplayElement, adjust_string, as_ascii
from .sysex import NAME_LENGTH, NAME_TERMINATOR

class SceneNameDisplayElement(SimpleDisplayElement):

    def display_data(self, data):
        data_to_send = [
         len(data)]
        for scene in data:
            data_to_send.extend(as_ascii(adjust_string(scene.name, NAME_LENGTH).strip()))
            data_to_send.append(NAME_TERMINATOR)

        self._message_to_send = self._message_header + tuple(data_to_send) + self._message_tail
        self._request_send_message()