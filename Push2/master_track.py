# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\master_track.py
# Compiled at: 2022-11-28 08:01:31
# Size of source mod 2**32: 1599 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import listens
from ableton.v2.control_surface import Component
from ableton.v2.control_surface.control import ToggleButtonControl

class MasterTrackComponent(Component):
    toggle_button = ToggleButtonControl()

    def __init__(self, tracks_provider=None, *a, **k):
        (super(MasterTrackComponent, self).__init__)(*a, **k)
        self._tracks_provider = tracks_provider
        self._MasterTrackComponent__on_selected_item_changed.subject = self._tracks_provider
        self._previous_selection = self._tracks_provider.selected_item
        self._update_button_state()

    @listens('selected_item')
    def __on_selected_item_changed(self, *a):
        self._update_button_state()
        if not self._is_on_master():
            self._previous_selection = self._tracks_provider.selected_item

    def _update_button_state(self):
        self.toggle_button.is_toggled = self._is_on_master()

    @toggle_button.toggled
    def toggle_button(self, toggled, button):
        if toggled:
            self._previous_selection = self._tracks_provider.selected_item
            self._tracks_provider.selected_item = self.song.master_track
        else:
            self._tracks_provider.selected_item = self._previous_selection
        self._update_button_state()

    def _is_on_master(self):
        return self._tracks_provider.selected_item == self.song.master_track