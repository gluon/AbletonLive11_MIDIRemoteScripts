#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/_Generic/testing/util.py
from __future__ import absolute_import, print_function, unicode_literals
import Live
from ableton.v2.base import const, nop
from ableton.v2.testing import count_calls

class MockControlSurface(object):
    instance_identifier = const(0)
    request_rebuild_midi_map = count_calls()
    show_message = nop
    send_midi = nop

    def __init__(self, *a, **k):
        super(MockControlSurface, self).__init__(*a, **k)
        self._song = Live.Song.Song(num_tracks=4, num_returns=2)

    def song(self):
        return self._song
