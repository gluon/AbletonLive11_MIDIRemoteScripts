from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import liveobj_valid
from novation.channel_strip import ChannelStripComponent as ChannelStripComponentBase

class ChannelStripComponent(ChannelStripComponentBase):

    def _track_color_changed(self):
        super(ChannelStripComponent, self)._track_color_changed()
        self._update_select_button()

    def _update_select_button(self):
        if liveobj_valid(self._track) or self.empty_color is None:
            if self.song.view.selected_track == self._track:
                self.select_button.color = self._track_color_value
            else:
                self.select_button.color = 'Mixer.TrackNotSelected'
        else:
            self.select_button.color = self.empty_color