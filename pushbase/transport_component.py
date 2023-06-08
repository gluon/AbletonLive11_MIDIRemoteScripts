from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface import components

class TransportComponent(components.TransportComponent):

    def __init__(self, *a, **k):
        (super(TransportComponent, self).__init__)(*a, **k)
        self._metronome_toggle.view_transform = lambda v: 'Metronome.On' if v else 'Metronome.Off'