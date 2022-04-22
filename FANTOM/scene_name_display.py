# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/FANTOM/scene_name_display.py
# Compiled at: 2022-01-27 16:28:16
# Size of source mod 2**32: 705 bytes
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