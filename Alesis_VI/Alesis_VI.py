from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
import _Framework.ButtonElement as ButtonElement
import _Framework.ControlSurface as ControlSurface
from _Framework.InputControlElement import MIDI_CC_TYPE
import _Framework.Layer as Layer
from _Framework.MidiMap import MidiMap as MidiMapBase
from _Framework.MidiMap import make_encoder
import _Framework.MixerComponent as MixerComponent
import _Framework.TransportComponent as TransportComponent

class MidiMap(MidiMapBase):

    def __init__(self, *a, **k):
        (super(MidiMap, self).__init__)(*a, **k)
        self.add_momentary_button('Stop', 0, 118, MIDI_CC_TYPE)
        self.add_momentary_button('Play', 0, 119, MIDI_CC_TYPE)
        self.add_momentary_button('Loop', 0, 115, MIDI_CC_TYPE)
        self.add_momentary_button('Record', 0, 114, MIDI_CC_TYPE)
        self.add_momentary_button('Forward', 0, 117, MIDI_CC_TYPE)
        self.add_momentary_button('Backward', 0, 116, MIDI_CC_TYPE)
        self.add_matrix('Volume_Encoders', make_encoder, 0, [
         list(range(20, 32)) + [35, 41, 46, 47]], MIDI_CC_TYPE)

    def add_momentary_button(self, name, channel, number, midi_message_type):
        self[name] = ButtonElement(True, midi_message_type, channel, number, name=name)


class Alesis_VI(ControlSurface):

    def __init__(self, *a, **k):
        (super(Alesis_VI, self).__init__)(*a, **k)
        with self.component_guard():
            midimap = MidiMap()
            transport = TransportComponent(name='Transport',
              is_enabled=False,
              layer=Layer(play_button=(midimap['Play']),
              stop_button=(midimap['Stop']),
              loop_button=(midimap['Loop']),
              record_button=(midimap['Record']),
              seek_forward_button=(midimap['Forward']),
              seek_backward_button=(midimap['Backward'])))
            mixer_size = len(midimap['Volume_Encoders'])
            mixer = MixerComponent(mixer_size,
              name='Mixer',
              is_enabled=False,
              layer=Layer(volume_controls=(midimap['Volume_Encoders'])))
            transport.set_enabled(True)
            mixer.set_enabled(True)