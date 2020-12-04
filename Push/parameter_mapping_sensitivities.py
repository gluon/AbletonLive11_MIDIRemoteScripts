#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Push/parameter_mapping_sensitivities.py
from __future__ import absolute_import, print_function, unicode_literals
from past.utils import old_div
from ableton.v2.base import liveobj_valid
from ableton.v2.control_surface import is_parameter_quantized
DEFAULT_SENSITIVITY_KEY = u'normal_sensitivity'
FINE_GRAINED_SENSITIVITY_KEY = u'fine_grained_sensitivity'
CONTINUOUS_MAPPING_SENSITIVITY = 2.0
FINE_GRAINED_CONTINUOUS_MAPPING_SENSITIVITY = 0.01
QUANTIZED_MAPPING_SENSITIVITY = old_div(1.0, 15.0)
PARAMETER_SENSITIVITIES = {u'UltraAnalog': {u'OSC1 Octave': {DEFAULT_SENSITIVITY_KEY: 0.05},
                  u'OSC2 Octave': {DEFAULT_SENSITIVITY_KEY: 0.05},
                  u'OSC1 Semi': {DEFAULT_SENSITIVITY_KEY: 0.05},
                  u'OSC1 Detune': {DEFAULT_SENSITIVITY_KEY: 0.5},
                  u'OSC2 Semi': {DEFAULT_SENSITIVITY_KEY: 0.05},
                  u'OSC2 Detune': {DEFAULT_SENSITIVITY_KEY: 0.5}},
 u'LoungeLizard': {u'Noise Pitch': {DEFAULT_SENSITIVITY_KEY: 0.5},
                   u'Damp Balance': {DEFAULT_SENSITIVITY_KEY: 0.5},
                   u'P Amp < Key': {DEFAULT_SENSITIVITY_KEY: 0.5},
                   u'Semitone': {DEFAULT_SENSITIVITY_KEY: 0.1}},
 u'Collision': {u'Res 1 Decay': {DEFAULT_SENSITIVITY_KEY: 0.5}},
 u'InstrumentImpulse': {u'1 Transpose': {DEFAULT_SENSITIVITY_KEY: 0.1},
                        u'2 Transpose': {DEFAULT_SENSITIVITY_KEY: 0.1},
                        u'3 Transpose': {DEFAULT_SENSITIVITY_KEY: 0.1},
                        u'4 Transpose': {DEFAULT_SENSITIVITY_KEY: 0.1},
                        u'5 Transpose': {DEFAULT_SENSITIVITY_KEY: 0.1},
                        u'6 Transpose': {DEFAULT_SENSITIVITY_KEY: 0.1},
                        u'7 Transpose': {DEFAULT_SENSITIVITY_KEY: 0.1},
                        u'8 Transpose': {DEFAULT_SENSITIVITY_KEY: 0.1}},
 u'OriginalSimpler': {u'Mode': {DEFAULT_SENSITIVITY_KEY: 0.1},
                      u'Playback': {DEFAULT_SENSITIVITY_KEY: 0.5},
                      u'Start': {DEFAULT_SENSITIVITY_KEY: 0.2},
                      u'End': {DEFAULT_SENSITIVITY_KEY: 0.2},
                      u'Sensitivity': {DEFAULT_SENSITIVITY_KEY: 0.5},
                      u'S Start': {DEFAULT_SENSITIVITY_KEY: 0.2},
                      u'S Length': {DEFAULT_SENSITIVITY_KEY: 0.2},
                      u'S Loop Length': {DEFAULT_SENSITIVITY_KEY: 0.2},
                      u'Transpose': {DEFAULT_SENSITIVITY_KEY: 0.1},
                      u'Detune': {DEFAULT_SENSITIVITY_KEY: 0.1},
                      u'Gain': {DEFAULT_SENSITIVITY_KEY: 0.1},
                      u'Env. Type': {DEFAULT_SENSITIVITY_KEY: 0.1},
                      u'Filter Freq': {DEFAULT_SENSITIVITY_KEY: 0.5},
                      u'Filt < Vel': {DEFAULT_SENSITIVITY_KEY: 0.5},
                      u'Filt < Key': {DEFAULT_SENSITIVITY_KEY: 0.5},
                      u'Filt < LFO': {DEFAULT_SENSITIVITY_KEY: 0.5},
                      u'Fe < Env': {DEFAULT_SENSITIVITY_KEY: 0.5},
                      u'LR < Key': {DEFAULT_SENSITIVITY_KEY: 0.5},
                      u'Vol < LFO': {DEFAULT_SENSITIVITY_KEY: 0.5},
                      u'Pan < RND': {DEFAULT_SENSITIVITY_KEY: 0.5},
                      u'Pan < LFO': {DEFAULT_SENSITIVITY_KEY: 0.5},
                      u'L Sync Rate': {DEFAULT_SENSITIVITY_KEY: 0.5}},
 u'Operator': {u'A Coarse': {DEFAULT_SENSITIVITY_KEY: 0.05},
               u'B Coarse': {DEFAULT_SENSITIVITY_KEY: 0.05},
               u'C Coarse': {DEFAULT_SENSITIVITY_KEY: 0.05},
               u'D Coarse': {DEFAULT_SENSITIVITY_KEY: 0.05},
               u'LFO Sync': {DEFAULT_SENSITIVITY_KEY: 0.1}},
 u'MidiArpeggiator': {u'Style': {DEFAULT_SENSITIVITY_KEY: 0.1},
                      u'Synced Rate': {DEFAULT_SENSITIVITY_KEY: 0.1},
                      u'Offset': {DEFAULT_SENSITIVITY_KEY: 0.1},
                      u'Transp. Steps': {DEFAULT_SENSITIVITY_KEY: 0.1},
                      u'Transp. Dist.': {DEFAULT_SENSITIVITY_KEY: 0.1},
                      u'Repeats': {DEFAULT_SENSITIVITY_KEY: 0.1},
                      u'Ret. Interval': {DEFAULT_SENSITIVITY_KEY: 0.1},
                      u'Groove': {DEFAULT_SENSITIVITY_KEY: 0.1},
                      u'Retrigger Mode': {DEFAULT_SENSITIVITY_KEY: 0.1}},
 u'MidiNoteLength': {u'Synced Length': {DEFAULT_SENSITIVITY_KEY: 0.1}},
 u'MidiScale': {u'Base': {DEFAULT_SENSITIVITY_KEY: 0.05},
                u'Transpose': {DEFAULT_SENSITIVITY_KEY: 0.1}},
 u'Amp': {u'Bass': {DEFAULT_SENSITIVITY_KEY: 0.5},
          u'Middle': {DEFAULT_SENSITIVITY_KEY: 0.5},
          u'Treble': {DEFAULT_SENSITIVITY_KEY: 0.5},
          u'Presence': {DEFAULT_SENSITIVITY_KEY: 0.5},
          u'Gain': {DEFAULT_SENSITIVITY_KEY: 0.5},
          u'Volume': {DEFAULT_SENSITIVITY_KEY: 0.5},
          u'Dry/Wet': {DEFAULT_SENSITIVITY_KEY: 0.5}},
 u'AutoFilter': {u'Frequency': {DEFAULT_SENSITIVITY_KEY: 1},
                 u'Env. Modulation': {DEFAULT_SENSITIVITY_KEY: 0.5},
                 u'LFO Sync Rate': {DEFAULT_SENSITIVITY_KEY: 0.1},
                 u'LFO Phase': {DEFAULT_SENSITIVITY_KEY: 0.5},
                 u'LFO Offset': {DEFAULT_SENSITIVITY_KEY: 0.5}},
 u'AutoPan': {u'Sync Rate': {DEFAULT_SENSITIVITY_KEY: 0.1}},
 u'BeatRepeat': {u'Grid': {DEFAULT_SENSITIVITY_KEY: 0.1},
                 u'Interval': {DEFAULT_SENSITIVITY_KEY: 0.1},
                 u'Offset': {DEFAULT_SENSITIVITY_KEY: 0.1},
                 u'Gate': {DEFAULT_SENSITIVITY_KEY: 0.1},
                 u'Pitch': {DEFAULT_SENSITIVITY_KEY: 0.1},
                 u'Variation': {DEFAULT_SENSITIVITY_KEY: 0.1},
                 u'Mix Type': {DEFAULT_SENSITIVITY_KEY: 0.1},
                 u'Grid': {DEFAULT_SENSITIVITY_KEY: 0.1},
                 u'Variation Type': {DEFAULT_SENSITIVITY_KEY: 0.1}},
 u'Corpus': {u'LFO Sync Rate': {DEFAULT_SENSITIVITY_KEY: 0.1}},
 u'Eq8': {u'Band': {DEFAULT_SENSITIVITY_KEY: 0.5},
          u'1 Frequency A': {DEFAULT_SENSITIVITY_KEY: 0.4},
          u'2 Frequency A': {DEFAULT_SENSITIVITY_KEY: 0.4},
          u'3 Frequency A': {DEFAULT_SENSITIVITY_KEY: 0.4},
          u'4 Frequency A': {DEFAULT_SENSITIVITY_KEY: 0.4},
          u'5 Frequency A': {DEFAULT_SENSITIVITY_KEY: 0.4},
          u'6 Frequency A': {DEFAULT_SENSITIVITY_KEY: 0.4},
          u'7 Frequency A': {DEFAULT_SENSITIVITY_KEY: 0.4},
          u'8 Frequency A': {DEFAULT_SENSITIVITY_KEY: 0.4}},
 u'Flanger': {u'Sync Rate': {DEFAULT_SENSITIVITY_KEY: 0.1}},
 u'GrainDelay': {u'Pitch': {DEFAULT_SENSITIVITY_KEY: 0.1}},
 u'Phaser': {u'LFO Sync Rate': {DEFAULT_SENSITIVITY_KEY: 0.1}},
 u'Resonator': {u'II Pitch': {DEFAULT_SENSITIVITY_KEY: 0.1},
                u'III Pitch': {DEFAULT_SENSITIVITY_KEY: 0.1},
                u'IV Pitch': {DEFAULT_SENSITIVITY_KEY: 0.1},
                u'V Pitch': {DEFAULT_SENSITIVITY_KEY: 0.1}},
 u'InstrumentVector': {u'Osc 1 Pitch': {DEFAULT_SENSITIVITY_KEY: 5.0,
                                        FINE_GRAINED_SENSITIVITY_KEY: 0.4},
                       u'Osc 2 Pitch': {DEFAULT_SENSITIVITY_KEY: 5.0,
                                        FINE_GRAINED_SENSITIVITY_KEY: 0.4}}}

def sensitivity_mapping_for_parameter(parameter, fine_grain = False):
    is_quantized = is_parameter_quantized(parameter, parameter and parameter.canonical_parent)
    if is_quantized:
        return QUANTIZED_MAPPING_SENSITIVITY
    if fine_grain:
        return FINE_GRAINED_CONTINUOUS_MAPPING_SENSITIVITY
    return CONTINUOUS_MAPPING_SENSITIVITY


def parameter_mapping_sensitivity(parameter, device_class = None):
    parameter_name = parameter.name if liveobj_valid(parameter) else u''
    try:
        return PARAMETER_SENSITIVITIES[device_class][parameter_name][DEFAULT_SENSITIVITY_KEY]
    except KeyError:
        return sensitivity_mapping_for_parameter(parameter)


def fine_grain_parameter_mapping_sensitivity(parameter, device_class = None):
    parameter_name = parameter.name if liveobj_valid(parameter) else u''
    try:
        return PARAMETER_SENSITIVITIES[device_class][parameter_name][FINE_GRAINED_SENSITIVITY_KEY]
    except KeyError:
        return sensitivity_mapping_for_parameter(parameter, fine_grain=True)
