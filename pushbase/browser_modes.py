# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\pushbase\browser_modes.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 5473 bytes
from __future__ import absolute_import, print_function, unicode_literals
import Live
from ableton.v2.base import depends, index_if, liveobj_valid
from ableton.v2.control_surface.mode import Mode
from .browser_util import get_selection_for_new_device
DeviceType = Live.Device.DeviceType

def can_browse_for_object(obj):
    return liveobj_valid(obj)


class BrowserHotswapMode(Mode):

    @depends(selection=None)
    def __init__(self, selection=None, application=None, *a, **k):
        (super(BrowserHotswapMode, self).__init__)(*a, **k)
        self._selection = selection
        self._application = application

    def can_hotswap(self):
        return can_browse_for_object(self._selection.selected_object) or can_browse_for_object(self._selection.selected_device)

    def enter_mode(self):
        try:
            self._set_hotswap_target(self._selection.selected_object)
        except RuntimeError:
            try:
                self._set_hotswap_target(self._selection.selected_device)
            except RuntimeError:
                pass

    def leave_mode(self):
        self._application.browser.hotswap_target = None

    def _set_hotswap_target(self, hotswap_object):
        self._application.browser.hotswap_target = hotswap_object
        self._application.view.show_view('Detail/DeviceChain')


class BrowserAddEffectMode(Mode):
    insert_left = False

    @depends(selection=None)
    def __init__(self, selection=None, browser=None, insert_left=None, application_view=None, *a, **k):
        (super(BrowserAddEffectMode, self).__init__)(*a, **k)
        self._selection = selection
        self._browser = browser
        self._application_view = application_view
        self._track_to_add_effect = None
        self._selection_for_insert = None
        if insert_left is not None:
            self.insert_left = insert_left

    def enter_mode(self):
        self._track_to_add_effect = self._selection.selected_track
        self._selection_for_insert = get_selection_for_new_device(self._selection, self.insert_left)
        self._track_to_add_effect.view.device_insert_mode = self.get_insert_mode()
        self._browser.filter_type = self.get_filter_type()
        if self._application_view.browse_mode:
            self._browser.hotswap_target = None

    def leave_mode(self):
        disabled = Live.Track.DeviceInsertMode.default
        self._track_to_add_effect.view.device_insert_mode = disabled
        self._browser.filter_type = Live.Browser.FilterType.disabled

    def get_insert_mode(self):
        if self.insert_left:
            return Live.Track.DeviceInsertMode.selected_left
        return Live.Track.DeviceInsertMode.selected_right

    def get_selection_for_insert(self):
        return self._selection_for_insert

    def get_filter_type(self):
        selected = self.get_selection_for_insert()
        chain = selected.canonical_parent if selected else self._selection.selected_track
        chain_len = len(chain.devices)
        index = index_if(lambda device: device == selected
, chain.devices)
        is_drum_pad = isinstance(chain.canonical_parent, Live.DrumPad.DrumPad)
        midi_support = chain.has_midi_input
        supports_instrument = is_drum_pad or (chain.has_midi_input) and ((chain.has_audio_output) or (isinstance(chain, Live.Track.Track)))
        if self.insert_left:
            left = chain.devices[index - 1] if index > 0 else None
            return filter_type_between(left, selected, midi_support, is_drum_pad, supports_instrument)
        right = chain.devices[index + 1] if index < chain_len - 1 else None
        return filter_type_between(selected, right, midi_support, is_drum_pad, supports_instrument)


def filter_type_between(left, right, supports_midi=False, is_drum_pad=False, supports_instrument=False):
    Types = Live.Browser.FilterType
    if right:
        if right.type in (DeviceType.instrument, DeviceType.midi_effect):
            return Types.midi_effect_hotswap
    if left:
        if left.type in (DeviceType.instrument, DeviceType.audio_effect):
            return Types.audio_effect_hotswap
    if supports_midi:
        if supports_instrument:
            if is_drum_pad:
                return Types.drum_pad_hotswap
            return Types.instrument_hotswap
        return Types.midi_effect_hotswap
    return Types.audio_effect_hotswap