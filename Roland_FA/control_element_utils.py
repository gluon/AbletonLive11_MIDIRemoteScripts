#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Roland_FA/control_element_utils.py
from __future__ import absolute_import, print_function, unicode_literals
import Live
from ableton.v2.base import depends
from ableton.v2.control_surface import MIDI_CC_TYPE
from ableton.v2.control_surface.elements import ButtonElement, EncoderElement

@depends(skin=None)
def make_button(identifier, name, msg_type = MIDI_CC_TYPE, skin = None):
    return ButtonElement(True, msg_type, 0, identifier, name=name, skin=skin)


def make_encoder(identifier, name):
    return EncoderElement(MIDI_CC_TYPE, 0, identifier, Live.MidiMap.MapMode.absolute, name=name)
