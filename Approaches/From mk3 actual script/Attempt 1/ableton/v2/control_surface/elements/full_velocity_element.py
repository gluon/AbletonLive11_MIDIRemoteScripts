#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v2/control_surface/elements/full_velocity_element.py
from __future__ import absolute_import, print_function, unicode_literals
from .proxy_element import ProxyElement

class NullFullVelocity(object):
    enabled = False


class FullVelocityElement(ProxyElement):

    def __init__(self, full_velocity = None, *a, **k):
        super(FullVelocityElement, self).__init__(proxied_object=full_velocity, proxied_interface=NullFullVelocity())
