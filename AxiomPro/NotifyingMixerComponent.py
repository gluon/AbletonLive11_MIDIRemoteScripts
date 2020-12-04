#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/AxiomPro/NotifyingMixerComponent.py
from __future__ import absolute_import, print_function, unicode_literals
from __future__ import division
from builtins import str
from past.utils import old_div
from _Framework.MixerComponent import MixerComponent
from _Framework.PhysicalDisplayElement import PhysicalDisplayElement

class NotifyingMixerComponent(MixerComponent):
    u""" Special mixer class that notifies an observer when reassigning parameters """

    def __init__(self, num_tracks):
        self._update_callback = None
        MixerComponent.__init__(self, num_tracks)
        self._bank_display = None

    def disconnect(self):
        MixerComponent.disconnect(self)
        self._update_callback = None

    def set_update_callback(self, callback):
        assert callback == None or dir(callback).count(u'im_func') is 1 or dir(callback).count(u'__func__') is 1
        self._update_callback = callback

    def set_bank_display(self, display):
        assert isinstance(display, PhysicalDisplayElement)
        self._bank_display = display

    def on_selected_track_changed(self):
        MixerComponent.on_selected_track_changed(self)
        selected_track = self.song().view.selected_track
        num_strips = len(self._channel_strips)
        if selected_track in self._tracks_to_use():
            track_index = list(self._tracks_to_use()).index(selected_track)
            new_offset = track_index - track_index % num_strips
            assert old_div(new_offset, num_strips) == int(old_div(new_offset, num_strips))
            self.set_track_offset(new_offset)

    def update(self):
        super(NotifyingMixerComponent, self).update()
        if self._update_callback != None:
            self._update_callback()

    def _tracks_to_use(self):
        return tuple(self.song().visible_tracks) + tuple(self.song().return_tracks)

    def _reassign_tracks(self):
        MixerComponent._reassign_tracks(self)
        if self._update_callback != None:
            self._update_callback()

    def _bank_up_value(self, value):
        old_offset = int(self._track_offset)
        MixerComponent._bank_up_value(self, value)
        if self._bank_display != None:
            if value != 0 and old_offset != self._track_offset:
                min_track = self._track_offset + 1
                max_track = min(len(self._tracks_to_use()), min_track + len(self._channel_strips))
                self._bank_display.display_message(u'Tracks ' + str(min_track) + u' - ' + str(max_track))
            else:
                self._bank_display.update()

    def _bank_down_value(self, value):
        old_offset = int(self._track_offset)
        MixerComponent._bank_down_value(self, value)
        if self._bank_display != None:
            if value != 0 and old_offset != self._track_offset:
                min_track = self._track_offset + 1
                max_track = min(len(self._tracks_to_use()), min_track + len(self._channel_strips))
                self._bank_display.display_message(u'Tracks ' + str(min_track) + u' - ' + str(max_track))
            else:
                self._bank_display.update()
