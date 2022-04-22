# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v2/control_surface/elements/full_velocity_element.py
# Compiled at: 2021-06-29 09:33:48
# Size of source mod 2**32: 466 bytes
from __future__ import absolute_import, print_function, unicode_literals
from .proxy_element import ProxyElement

class NullFullVelocity(object):
    enabled = False


class FullVelocityElement(ProxyElement):

    def __init__(self, full_velocity=None, *a, **k):
        super(FullVelocityElement, self).__init__(proxied_object=full_velocity,
          proxied_interface=(NullFullVelocity()))