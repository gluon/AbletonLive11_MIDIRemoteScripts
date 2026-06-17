# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\MPK261\MPK261.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 3109 bytes
from __future__ import absolute_import, print_function, unicode_literals
import _Framework.ControlSurface as ControlSurface
import _Framework.DrumRackComponent as DrumRackComponent
from _Framework.InputControlElement import MIDI_CC_TYPE, MIDI_NOTE_TYPE
import _Framework.Layer as Layer
from _Framework.MidiMap import MidiMap as MidiMapBase
from _Framework.MidiMap import make_button, make_encoder, make_slider
import _Framework.MixerComponent as MixerComponent
import _Framework.TransportComponent as TransportComponent

class MidiMap(MidiMapBase):

    def __init__(self, *a, **k):
        (super(MidiMap, self).__init__)(*a, **k)
        self.add_button('Play', 0, 118, MIDI_CC_TYPE)
        self.add_button('Record', 0, 119, MIDI_CC_TYPE)
        self.add_button('Stop', 0, 117, MIDI_CC_TYPE)
        self.add_button('Loop', 0, 114, MIDI_CC_TYPE)
        self.add_button('Forward', 0, 116, MIDI_CC_TYPE)
        self.add_button('Backward', 0, 115, MIDI_CC_TYPE)
        self.add_matrix('Sliders', make_slider, 0, [[12,13,14,15,16,17,18,19]], MIDI_CC_TYPE)
        self.add_matrix('Encoders', make_encoder, 0, [[22,23,24,25,26,27,28,29]], MIDI_CC_TYPE)
        self.add_matrix('Arm_Buttons', make_button, 0, [
         [
          32,33,34,35,36,37,38,39]], MIDI_CC_TYPE)
        self.add_matrix('Drum_Pads', make_button, 1, [
         [
          81, 83, 84, 86], [74, 76, 77, 79], [67, 69, 71, 72], [60, 62, 64, 65]], MIDI_NOTE_TYPE)


class MPK261(ControlSurface):

    def __init__(self, *a, **k):
        (super(MPK261, self).__init__)(*a, **k)
        with self.component_guard():
            midimap = MidiMap()
            drum_rack = DrumRackComponent(name='Drum_Rack',
              is_enabled=False,
              layer=Layer(pads=(midimap['Drum_Pads'])))
            drum_rack.set_enabled(True)
            transport = TransportComponent(name='Transport',
              is_enabled=False,
              layer=Layer(play_button=(midimap['Play']),
              record_button=(midimap['Record']),
              stop_button=(midimap['Stop']),
              seek_forward_button=(midimap['Forward']),
              seek_backward_button=(midimap['Backward']),
              loop_button=(midimap['Loop'])))
            transport.set_enabled(True)
            mixer_size = len(midimap['Sliders'])
            mixer = MixerComponent(mixer_size,
              name='Mixer',
              is_enabled=False,
              layer=Layer(volume_controls=(midimap['Sliders']),
              pan_controls=(midimap['Encoders']),
              arm_buttons=(midimap['Arm_Buttons'])))
            mixer.set_enabled(True)