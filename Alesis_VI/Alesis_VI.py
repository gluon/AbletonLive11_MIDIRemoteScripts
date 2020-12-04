#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Alesis_VI/Alesis_VI.py
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
from _Framework.ControlSurface import ControlSurface
from _Framework.MidiMap import make_encoder, MidiMap as MidiMapBase
from _Framework.InputControlElement import MIDI_CC_TYPE
from _Framework.ButtonElement import ButtonElement
from _Framework.Layer import Layer
from _Framework.TransportComponent import TransportComponent
from _Framework.MixerComponent import MixerComponent

class MidiMap(MidiMapBase):

    def __init__(self, *a, **k):
        super(MidiMap, self).__init__(*a, **k)
        self.add_momentary_button(u'Stop', 0, 118, MIDI_CC_TYPE)
        self.add_momentary_button(u'Play', 0, 119, MIDI_CC_TYPE)
        self.add_momentary_button(u'Loop', 0, 115, MIDI_CC_TYPE)
        self.add_momentary_button(u'Record', 0, 114, MIDI_CC_TYPE)
        self.add_momentary_button(u'Forward', 0, 117, MIDI_CC_TYPE)
        self.add_momentary_button(u'Backward', 0, 116, MIDI_CC_TYPE)
        self.add_matrix(u'Volume_Encoders', make_encoder, 0, [list(range(20, 32)) + [35,
          41,
          46,
          47]], MIDI_CC_TYPE)

    def add_momentary_button(self, name, channel, number, midi_message_type):
        assert name not in list(self.keys())
        self[name] = ButtonElement(True, midi_message_type, channel, number, name=name)


class Alesis_VI(ControlSurface):

    def __init__(self, *a, **k):
        super(Alesis_VI, self).__init__(*a, **k)
        with self.component_guard():
            midimap = MidiMap()
            transport = TransportComponent(name=u'Transport', is_enabled=False, layer=Layer(play_button=midimap[u'Play'], stop_button=midimap[u'Stop'], loop_button=midimap[u'Loop'], record_button=midimap[u'Record'], seek_forward_button=midimap[u'Forward'], seek_backward_button=midimap[u'Backward']))
            mixer_size = len(midimap[u'Volume_Encoders'])
            mixer = MixerComponent(mixer_size, name=u'Mixer', is_enabled=False, layer=Layer(volume_controls=midimap[u'Volume_Encoders']))
            transport.set_enabled(True)
            mixer.set_enabled(True)
