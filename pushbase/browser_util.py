# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\pushbase\browser_util.py
# Compiled at: 2022-11-28 08:01:32
# Size of source mod 2**32: 1850 bytes
from __future__ import absolute_import, print_function, unicode_literals
import Live
FilterType = Live.Browser.FilterType
DeviceType = Live.Device.DeviceType

def filter_type_for_hotswap_target(target, default=FilterType.disabled):
    if isinstance(target, Live.Device.Device):
        if target.type == DeviceType.instrument:
            return FilterType.instrument_hotswap
        if target.type == DeviceType.audio_effect:
            return FilterType.audio_effect_hotswap
        if target.type == DeviceType.midi_effect:
            return FilterType.midi_effect_hotswap
        FilterType.disabled
    else:
        if isinstance(target, Live.DrumPad.DrumPad):
            return FilterType.drum_pad_hotswap
        if isinstance(target, Live.Chain.Chain):
            if target:
                return filter_type_for_hotswap_target(target.canonical_parent)
            return FilterType.disabled
    return default


def get_selection_for_new_device(selection, insert_left=False):
    selected = selection.selected_object
    if isinstance(selected, Live.DrumPad.DrumPad) and selected.chains and selected.chains[0].devices:
        index = 0 if insert_left else -1
        selected = selected.chains[0].devices[index]
    else:
        if not isinstance(selected, Live.Device.Device):
            selected = selection.selected_device
    return selected