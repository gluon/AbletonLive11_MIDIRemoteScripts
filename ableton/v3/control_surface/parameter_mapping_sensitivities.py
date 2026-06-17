# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\parameter_mapping_sensitivities.py
# Compiled at: 2023-08-04 12:30:20
# Size of source mod 2**32: 4842 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ..live import is_parameter_quantized, liveobj_valid
DEFAULT_CONTINUOUS_PARAMETER_SENSITIVITY = 1.0
DEFAULT_QUANTIZED_PARAMETER_SENSITIVITY = 0.1
FINE_GRAIN_SENSITIVITY_FACTOR = 0.1
QUANTIZED_SENSITIVITY_FACTOR = 8

def get_base_quantized_sensitivity(parameter):
    v_range = parameter.max - parameter.min
    is_on_off_parameter = v_range == 1.0
    if is_on_off_parameter:
        return 1.0
    return v_range / QUANTIZED_SENSITIVITY_FACTOR


def parameter_mapping_sensitivities(continuous_parameter_sensitivity=DEFAULT_CONTINUOUS_PARAMETER_SENSITIVITY, quantized_parameter_sensitivity=DEFAULT_QUANTIZED_PARAMETER_SENSITIVITY):
    described_sensitivities = create_sensitivities(quantized_parameter_sensitivity)

    def inner(parameter, device):
        default = continuous_parameter_sensitivity
        is_quantized = False
        if liveobj_valid(parameter):
            is_quantized = is_parameter_quantized(parameter, device)
            try:
                default = described_sensitivities[device.class_name][parameter.name]
            except KeyError:
                if is_quantized:
                    default = get_base_quantized_sensitivity(parameter) * quantized_parameter_sensitivity

            return (
             default,
             default if is_quantized else default * FINE_GRAIN_SENSITIVITY_FACTOR)

    return inner


def create_sensitivities(quantized_parameter_sensitivity):
    q_min = quantized_parameter_sensitivity / 2
    q_default = quantized_parameter_sensitivity
    q_median = quantized_parameter_sensitivity * 3
    q_max = quantized_parameter_sensitivity * 6
    return {'BeatRepeat':{'Pitch': q_default}, 
     'GrainDelay':{'Pitch': q_median}, 
     'InstrumentImpulse':{
       '1 Transpose': q_median,
       '2 Transpose': q_median,
       '3 Transpose': q_median,
       '4 Transpose': q_median,
       '5 Transpose': q_median,
       '6 Transpose': q_median,
       '7 Transpose': q_median,
       '8 Transpose': q_median,
       'Global Transpose': q_median}, 
     'LoungeLizard':{'Semitone': q_default}, 
     'MidiArpeggiator':{'Transp. Dist.': q_median}, 
     'MidiScale':{'Transpose': q_median}, 
     'MultiSampler':{'O Coarse': q_median}, 
     'Operator':{
       'A Coarse': q_median,
       'B Coarse': q_median,
       'C Coarse': q_median,
       'D Coarse': q_median}, 
     'OriginalSimpler':{
       'Transpose': q_median,
       'Start': q_median,
       'End': q_median,
       'Nudge': q_median,
       'Slice by': q_median,
       'Playback': q_median,
       'Sensitivity': q_max,
       'Division': q_median,
       'Regions': q_max}, 
     'Resonator':{
       'I Note': q_median,
       'II Pitch': q_median,
       'III Pitch': q_median,
       'IV Pitch': q_median,
       'V Pitch': q_median}, 
     'StringStudio':{'Octave':q_min, 
      'Semitone':q_default}, 
     'UltraAnalog':{
       'OSC1 Octave': q_min,
       'OSC1 Semi': q_default,
       'OSC2 Octave': q_min,
       'OSC2 Semi': q_default}}