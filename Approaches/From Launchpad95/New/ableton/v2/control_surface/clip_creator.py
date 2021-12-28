#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v2/control_surface/clip_creator.py
from __future__ import absolute_import, print_function, unicode_literals
import Live
_Q = Live.Song.Quantization

class ClipCreator(object):
    u"""
    Manages clip creation over all components.
    """
    grid_quantization = None
    is_grid_triplet = False
    fixed_length = 8
    legato_launch = True

    def create(self, slot, length = None, launch_quantization = None, legato_launch = None):
        assert slot.clip == None
        if length is None:
            length = self.fixed_length
        slot.create_clip(length)
        should_legato_launch = self.legato_launch if legato_launch is None else legato_launch
        if self.grid_quantization is not None:
            slot.clip.view.grid_quantization = self.grid_quantization
            slot.clip.view.grid_is_triplet = self.is_grid_triplet
        if launch_quantization is None or should_legato_launch:
            launch_quantization = _Q.q_no_q
        slot.fire(force_legato=should_legato_launch, launch_quantization=launch_quantization)
