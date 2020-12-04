#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Launchkey_MK3/channel_strip.py
from __future__ import absolute_import, print_function, unicode_literals
from past.builtins import unicode
from ableton.v2.base import listens, liveobj_valid
from novation.channel_strip import ChannelStripComponent as ChannelStripComponentBase
from .control import DisplayControl

class ChannelStripComponent(ChannelStripComponentBase):
    volume_display = DisplayControl()
    pan_display = DisplayControl()
    send_a_display = DisplayControl()
    send_b_display = DisplayControl()

    def set_send_control(self, control, send_index):
        for sc in self._send_controls or []:
            if sc:
                sc.release_parameter()

        if not self._send_controls:
            self._send_controls = [None, None]
        self._send_controls[send_index] = control
        self.update()

    def set_track(self, track):
        super(ChannelStripComponent, self).set_track(track)
        track = track if liveobj_valid(track) else None
        self.__on_volume_value_changed.subject = track
        self.__on_pan_value_changed.subject = track
        self._update_volume_display()
        self._update_pan_display()

    def _track_color_changed(self):
        super(ChannelStripComponent, self)._track_color_changed()
        self._update_select_button()

    def update(self):
        super(ChannelStripComponent, self).update()
        mixer = self._track.mixer_device if liveobj_valid(self._track) else None
        self.__on_send_a_value_changed.subject = mixer.sends[0] if mixer and len(mixer.sends) else None
        self.__on_send_b_value_changed.subject = mixer.sends[1] if mixer and len(mixer.sends) > 1 else None
        self._update_send_display(self.send_a_display, 0)
        self._update_send_display(self.send_b_display, 1)

    def _update_select_button(self):
        if liveobj_valid(self._track) or self.empty_color is None:
            if self.song.view.selected_track == self._track:
                self.select_button.color = u'Mixer.TrackSelected'
            else:
                self.select_button.color = self._track_color_value
        else:
            self.select_button.color = self.empty_color

    @listens(u'mixer_device.volume.value')
    def __on_volume_value_changed(self):
        self._update_volume_display()

    @listens(u'mixer_device.panning.value')
    def __on_pan_value_changed(self):
        self._update_pan_display()

    @listens(u'value')
    def __on_send_a_value_changed(self):
        self._update_send_display(self.send_a_display, 0)

    @listens(u'value')
    def __on_send_b_value_changed(self):
        self._update_send_display(self.send_b_display, 1)

    def _update_volume_display(self):
        self.volume_display.message = unicode(self._track.mixer_device.volume) if liveobj_valid(self._track) else None

    def _update_pan_display(self):
        self.pan_display.message = unicode(self._track.mixer_device.panning) if liveobj_valid(self._track) else None

    def _update_send_display(self, display, send_index):
        message = None
        if liveobj_valid(self._track) and len(self._track.mixer_device.sends) > send_index:
            message = unicode(self._track.mixer_device.sends[send_index])
        display.message = message
