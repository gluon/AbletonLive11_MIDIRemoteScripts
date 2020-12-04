#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Roland_FA/transport.py
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.control import ButtonControl
from ableton.v2.control_surface.components import TransportComponent as TransportComponentBase

class TransportComponent(TransportComponentBase):
    jump_to_start_button = ButtonControl()

    @jump_to_start_button.pressed
    def jump_to_start_button(self, _):
        self.song.current_song_time = 0.0
