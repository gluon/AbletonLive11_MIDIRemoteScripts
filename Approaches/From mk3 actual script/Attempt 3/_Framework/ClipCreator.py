#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/_Framework/ClipCreator.py
from __future__ import absolute_import, print_function, unicode_literals
from builtins import object
import Live
_Q = Live.Song.Quantization

class ClipCreator(object):
    u"""
    Manages clip creation over all components.
    """
    grid_quantization = None
    is_grid_triplet = False
    fixed_length = 8

    def create(self, slot, length = None):
        assert slot.clip == None
        if length is None:
            length = self.fixed_length
        slot.create_clip(length)
        if self.grid_quantization != None:
            slot.clip.view.grid_quantization = self.grid_quantization
            slot.clip.view.grid_is_triplet = self.is_grid_triplet
        slot.fire(force_legato=True, launch_quantization=_Q.q_no_q)
