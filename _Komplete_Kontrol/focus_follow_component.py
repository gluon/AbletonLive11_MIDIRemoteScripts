# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_Komplete_Kontrol\focus_follow_component.py
# Compiled at: 2023-10-06 07:41:29
# Size of source mod 2**32: 2245 bytes
from __future__ import absolute_import, print_function, unicode_literals
from itertools import chain
import Live
from ableton.v2.base import listens, listens_group, liveobj_valid
from ableton.v2.control_surface import Component, find_instrument_devices, find_instrument_meeting_requirement
from ableton.v2.control_surface.control import SendValueControl
KK_NAME_PREFIX = 'Komplete Kontrol'

class FocusFollowComponent(Component):
    focus_follow_control = SendValueControl()

    def __init__(self, *a, **k):
        (super(FocusFollowComponent, self).__init__)(*a, **k)
        self._track = None
        self._FocusFollowComponent__on_selected_track_changed.subject = self.song.view
        self._FocusFollowComponent__on_selected_track_changed()

    @listens('selected_track')
    def __on_selected_track_changed(self):
        track = self.song.view.selected_track
        self._track = track if track.has_midi_input else None
        self.update()

    @listens_group('chains')
    def __on_chains_changed(self, _):
        self.update()

    @listens_group('devices')
    def __on_devices_changed(self, _):
        self.update()

    def update(self):
        super(FocusFollowComponent, self).update()
        self._update_listeners()
        self._update_komplete_kontrol_instance()

    def _update_listeners(self):
        devices = list(find_instrument_devices(self._track))
        racks = [d for d in devices if d.can_have_chains]
        chains = list(chain([self._track], *[d.chains for d in racks]))
        self._FocusFollowComponent__on_chains_changed.replace_subjects(racks)
        self._FocusFollowComponent__on_devices_changed.replace_subjects(chains)

    def _update_komplete_kontrol_instance(self):
        instance = find_instrument_meeting_requirement(lambda d: isinstance(d, Live.PluginDevice.PluginDevice) and d.name.startswith(KK_NAME_PREFIX)
, self._track)
        param_name = ''
        names = instance.get_parameter_names(end=1) if liveobj_valid(instance) else None
        if names:
            param_name = names[0]
        self.focus_follow_control.value = tuple([ord(n) for n in param_name])