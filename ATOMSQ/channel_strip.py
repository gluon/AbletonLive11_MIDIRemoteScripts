from __future__ import absolute_import, print_function, unicode_literals
from ableton.v3.base import listens, liveobj_valid
from ableton.v3.control_surface.components import ChannelStripComponent as ChannelStripComponentBase
from .control import DisplayControl

class ChannelStripComponent(ChannelStripComponentBase):
    track_name_display = DisplayControl()

    def set_track(self, track):
        super().set_track(track)
        self._ChannelStripComponent__on_track_name_changed.subject = self._track

    def update(self):
        super().update()
        self._ChannelStripComponent__on_track_name_changed()

    @listens('name')
    def __on_track_name_changed(self):
        self.track_name_display.message = self._track.name if liveobj_valid(self._track) else ' - '