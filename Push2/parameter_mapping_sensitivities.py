# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\parameter_mapping_sensitivities.py
# Compiled at: 2023-10-06 16:19:02
# Size of source mod 2**32: 7591 bytes
from __future__ import absolute_import, print_function, unicode_literals
from past.utils import old_div
from ableton.v2.control_surface import is_parameter_quantized
DEFAULT_SENSITIVITY_KEY = 'normal_sensitivity'
FINE_GRAINED_SENSITIVITY_KEY = 'fine_grained_sensitivity'
CONTINUOUS_MAPPING_SENSITIVITY = 1.0
FINE_GRAINED_CONTINUOUS_MAPPING_SENSITIVITY = 0.01
QUANTIZED_MAPPING_SENSITIVITY = old_div(1.0, 15.0)

def parameter_mapping_sensitivity(parameter):
    is_quantized = is_parameter_quantized(parameter, parameter and parameter.canonical_parent)
    if is_quantized:
        return QUANTIZED_MAPPING_SENSITIVITY
    return CONTINUOUS_MAPPING_SENSITIVITY


def fine_grain_parameter_mapping_sensitivity(parameter):
    is_quantized = is_parameter_quantized(parameter, parameter and parameter.canonical_parent)
    if is_quantized:
        return QUANTIZED_MAPPING_SENSITIVITY
    return FINE_GRAINED_CONTINUOUS_MAPPING_SENSITIVITY


PARAMETER_SENSITIVITIES = {'UltraAnalog':{'OSC1 Octave':{DEFAULT_SENSITIVITY_KEY: 0.05}, 
  'OSC2 Octave':{DEFAULT_SENSITIVITY_KEY: 0.05}, 
  'OSC1 Semi':{DEFAULT_SENSITIVITY_KEY: 0.05}, 
  'OSC1 Detune':{DEFAULT_SENSITIVITY_KEY: 0.5}, 
  'OSC2 Semi':{DEFAULT_SENSITIVITY_KEY: 0.05}, 
  'OSC2 Detune':{DEFAULT_SENSITIVITY_KEY: 0.5}}, 
 'LoungeLizard':{'Noise Pitch':{DEFAULT_SENSITIVITY_KEY: 0.5}, 
  'Damp Balance':{DEFAULT_SENSITIVITY_KEY: 0.5}, 
  'P Amp < Key':{DEFAULT_SENSITIVITY_KEY: 0.5}, 
  'Semitone':{DEFAULT_SENSITIVITY_KEY: 0.5}}, 
 'Collision':{'Res 1 Decay': {DEFAULT_SENSITIVITY_KEY: 0.5}}, 
 'InstrumentImpulse':{'1 Transpose':{DEFAULT_SENSITIVITY_KEY: 0.1}, 
  '2 Transpose':{DEFAULT_SENSITIVITY_KEY: 0.1}, 
  '3 Transpose':{DEFAULT_SENSITIVITY_KEY: 0.1}, 
  '4 Transpose':{DEFAULT_SENSITIVITY_KEY: 0.1}, 
  '5 Transpose':{DEFAULT_SENSITIVITY_KEY: 0.1}, 
  '6 Transpose':{DEFAULT_SENSITIVITY_KEY: 0.1}, 
  '7 Transpose':{DEFAULT_SENSITIVITY_KEY: 0.1}, 
  '8 Transpose':{DEFAULT_SENSITIVITY_KEY: 0.1}}, 
 'OriginalSimpler':{'Zoom':{DEFAULT_SENSITIVITY_KEY: 1}, 
  'Mode':{DEFAULT_SENSITIVITY_KEY: 0.5}, 
  'Playback':{DEFAULT_SENSITIVITY_KEY: 0.5}, 
  'Start':{DEFAULT_SENSITIVITY_KEY: 0.2}, 
  'End':{DEFAULT_SENSITIVITY_KEY: 0.2}, 
  'Sensitivity':{DEFAULT_SENSITIVITY_KEY: 0.5}, 
  'S Start':{DEFAULT_SENSITIVITY_KEY: 0.2}, 
  'S Length':{DEFAULT_SENSITIVITY_KEY: 0.2}, 
  'S Loop Length':{DEFAULT_SENSITIVITY_KEY: 0.2}, 
  'Transpose':{DEFAULT_SENSITIVITY_KEY: 0.1}, 
  'Detune':{DEFAULT_SENSITIVITY_KEY: 0.1}, 
  'Gain':{DEFAULT_SENSITIVITY_KEY: 0.1}, 
  'Env. Type':{DEFAULT_SENSITIVITY_KEY: 0.1}, 
  'Filter Freq':{DEFAULT_SENSITIVITY_KEY: 0.5}, 
  'Filt < Vel':{DEFAULT_SENSITIVITY_KEY: 0.5}, 
  'Filt < Key':{DEFAULT_SENSITIVITY_KEY: 0.5}, 
  'Filt < LFO':{DEFAULT_SENSITIVITY_KEY: 0.5}, 
  'Fe < Env':{DEFAULT_SENSITIVITY_KEY: 0.5}, 
  'L R < Key':{DEFAULT_SENSITIVITY_KEY: 0.5}, 
  'Vol < LFO':{DEFAULT_SENSITIVITY_KEY: 0.5}, 
  'Pan < Rnd':{DEFAULT_SENSITIVITY_KEY: 0.5}, 
  'Pan < LFO':{DEFAULT_SENSITIVITY_KEY: 0.5}, 
  'L Sync Rate':{DEFAULT_SENSITIVITY_KEY: 0.5}}, 
 'Operator':{'Oscillator':{DEFAULT_SENSITIVITY_KEY: 0.5}, 
  'A Coarse':{DEFAULT_SENSITIVITY_KEY: 0.1}, 
  'B Coarse':{DEFAULT_SENSITIVITY_KEY: 0.1}, 
  'C Coarse':{DEFAULT_SENSITIVITY_KEY: 0.1}, 
  'D Coarse':{DEFAULT_SENSITIVITY_KEY: 0.1}, 
  'LFO Sync':{DEFAULT_SENSITIVITY_KEY: 0.1}}, 
 'MidiArpeggiator':{'Style':{DEFAULT_SENSITIVITY_KEY: 0.1}, 
  'Synced Rate':{DEFAULT_SENSITIVITY_KEY: 0.1}, 
  'Offset':{DEFAULT_SENSITIVITY_KEY: 0.1}, 
  'Transp. Steps':{DEFAULT_SENSITIVITY_KEY: 0.1}, 
  'Transp. Dist.':{DEFAULT_SENSITIVITY_KEY: 0.5}, 
  'Repeats':{DEFAULT_SENSITIVITY_KEY: 0.1}, 
  'Ret. Interval':{DEFAULT_SENSITIVITY_KEY: 0.5}, 
  'Groove':{DEFAULT_SENSITIVITY_KEY: 0.1}, 
  'Retrigger Mode':{DEFAULT_SENSITIVITY_KEY: 0.1}}, 
 'MidiNoteLength':{'Synced Length': {DEFAULT_SENSITIVITY_KEY: 0.1}}, 
 'MidiScale':{'Base':{DEFAULT_SENSITIVITY_KEY: 0.5}, 
  'Transpose':{DEFAULT_SENSITIVITY_KEY: 0.5}}, 
 'Amp':{'Bass':{DEFAULT_SENSITIVITY_KEY: 0.5}, 
  'Middle':{DEFAULT_SENSITIVITY_KEY: 0.5}, 
  'Treble':{DEFAULT_SENSITIVITY_KEY: 0.5}, 
  'Presence':{DEFAULT_SENSITIVITY_KEY: 0.5}, 
  'Gain':{DEFAULT_SENSITIVITY_KEY: 0.5}, 
  'Volume':{DEFAULT_SENSITIVITY_KEY: 0.5}, 
  'Dry/Wet':{DEFAULT_SENSITIVITY_KEY: 0.5}}, 
 'AutoFilter':{'Frequency':{DEFAULT_SENSITIVITY_KEY: 1}, 
  'Env. Modulation':{DEFAULT_SENSITIVITY_KEY: 0.5}, 
  'LFO Sync Rate':{DEFAULT_SENSITIVITY_KEY: 0.1}, 
  'LFO Phase':{DEFAULT_SENSITIVITY_KEY: 0.5}, 
  'LFO Offset':{DEFAULT_SENSITIVITY_KEY: 0.5}}, 
 'AutoPan':{'Sync Rate': {DEFAULT_SENSITIVITY_KEY: 0.1}}, 
 'BeatRepeat':{'Grid':{DEFAULT_SENSITIVITY_KEY: 0.1}, 
  'Interval':{DEFAULT_SENSITIVITY_KEY: 0.1}, 
  'Offset':{DEFAULT_SENSITIVITY_KEY: 0.1}, 
  'Gate':{DEFAULT_SENSITIVITY_KEY: 0.1}, 
  'Pitch':{DEFAULT_SENSITIVITY_KEY: 0.1}, 
  'Variation':{DEFAULT_SENSITIVITY_KEY: 0.1}, 
  'Mix Type':{DEFAULT_SENSITIVITY_KEY: 0.1}, 
  'Grid':{DEFAULT_SENSITIVITY_KEY: 0.1}, 
  'Variation Type':{DEFAULT_SENSITIVITY_KEY: 0.1}}, 
 'Corpus':{'LFO Sync Rate': {DEFAULT_SENSITIVITY_KEY: 0.1}}, 
 'Eq8':{'Band':{DEFAULT_SENSITIVITY_KEY: 0.5}, 
  '1 Frequency A':{DEFAULT_SENSITIVITY_KEY: 0.4}, 
  '2 Frequency A':{DEFAULT_SENSITIVITY_KEY: 0.4}, 
  '3 Frequency A':{DEFAULT_SENSITIVITY_KEY: 0.4}, 
  '4 Frequency A':{DEFAULT_SENSITIVITY_KEY: 0.4}, 
  '5 Frequency A':{DEFAULT_SENSITIVITY_KEY: 0.4}, 
  '6 Frequency A':{DEFAULT_SENSITIVITY_KEY: 0.4}, 
  '7 Frequency A':{DEFAULT_SENSITIVITY_KEY: 0.4}, 
  '8 Frequency A':{DEFAULT_SENSITIVITY_KEY: 0.4}}, 
 'Flanger':{'Sync Rate': {DEFAULT_SENSITIVITY_KEY: 0.1}}, 
 'GrainDelay':{'Pitch': {DEFAULT_SENSITIVITY_KEY: 0.5}}, 
 'Phaser':{'LFO Sync Rate': {DEFAULT_SENSITIVITY_KEY: 0.1}}, 
 'PhaserNew':{'Mode': {DEFAULT_SENSITIVITY_KEY: 0.03}}, 
 'Resonator':{'II Pitch':{DEFAULT_SENSITIVITY_KEY: 0.5}, 
  'III Pitch':{DEFAULT_SENSITIVITY_KEY: 0.5}, 
  'IV Pitch':{DEFAULT_SENSITIVITY_KEY: 0.5}, 
  'V Pitch':{DEFAULT_SENSITIVITY_KEY: 0.5}}, 
 'InstrumentVector':{'Osc 1 Pitch':{DEFAULT_SENSITIVITY_KEY: 10.0, FINE_GRAINED_SENSITIVITY_KEY: 0.4}, 
  'Osc 2 Pitch':{DEFAULT_SENSITIVITY_KEY: 10.0, FINE_GRAINED_SENSITIVITY_KEY: 0.4}}, 
 'Shifter':{'Mode':{DEFAULT_SENSITIVITY_KEY: 0.05}, 
  'Pitch Bend Range':{DEFAULT_SENSITIVITY_KEY: 10.0}}, 
 'StringStudio':{'Octave':{DEFAULT_SENSITIVITY_KEY: 0.05}, 
  'Semitone':{DEFAULT_SENSITIVITY_KEY: 0.1}}, 
 'Transmute':{'Pitch Bend Range': {DEFAULT_SENSITIVITY_KEY: 10.0}}, 
 'Drift':{'PB Range': {DEFAULT_SENSITIVITY_KEY: 10.0}}}