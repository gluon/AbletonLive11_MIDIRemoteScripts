#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/pushbase/track_frozen_mode.py
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import listens
from ableton.v2.control_surface.mode import ModesComponent

class TrackFrozenModesComponent(ModesComponent):

    def __init__(self, default_mode = None, frozen_mode = None, *a, **k):
        super(TrackFrozenModesComponent, self).__init__(*a, **k)
        assert default_mode is not None
        assert frozen_mode is not None
        self.add_mode(u'default', default_mode)
        self.add_mode(u'frozen', frozen_mode)
        self._on_selected_track_is_frozen_changed.subject = self.song.view
        if self.is_enabled():
            self._update_selected_mode()

    def _update_selected_mode(self):
        self.selected_mode = u'frozen' if self.song.view.selected_track.is_frozen else u'default'

    @listens(u'selected_track.is_frozen')
    def _on_selected_track_is_frozen_changed(self):
        self._update_selected_mode()

    def update(self):
        super(TrackFrozenModesComponent, self).update()
        if self.is_enabled():
            self._update_selected_mode()
