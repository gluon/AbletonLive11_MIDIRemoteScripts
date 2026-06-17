# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v2\control_surface\elements\playhead_element.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 709 bytes
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

    def __init__(self, playhead=None, *a, **k):
        super(PlayheadElement, self).__init__(proxied_object=playhead,
          proxied_interface=(NullPlayhead()))

    def reset(self):
        self.track = None