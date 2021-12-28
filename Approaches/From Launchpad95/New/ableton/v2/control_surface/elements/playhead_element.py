#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v2/control_surface/elements/playhead_element.py
from __future__ import absolute_import, print_function, unicode_literals
from ...base import nop
from .proxy_element import ProxyElement

class NullPlayhead(object):
    notes = []
    start_time = 0.0
    step_length = 1.0
    velocity = 0.0
    wrap_around = False
    track = None
    clip = None
    set_feedback_channels = nop


class PlayheadElement(ProxyElement):

    def __init__(self, playhead = None, *a, **k):
        super(PlayheadElement, self).__init__(proxied_object=playhead, proxied_interface=NullPlayhead())

    def reset(self):
        self.track = None
