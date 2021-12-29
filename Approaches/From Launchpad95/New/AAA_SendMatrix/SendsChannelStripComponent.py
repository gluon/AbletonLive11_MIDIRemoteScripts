import Live
from _Framework.ChannelStripComponent import ChannelStripComponent
from .ConfigurableButtonElement import ConfigurableButtonElement
from itertools import chain


class SendsChannelStripComponent(ChannelStripComponent):

    """Subclass of channel strip component offering defaultbuttons for the timeables"""

    def __init__(self):
        ChannelStripComponent.__init__(self)
        self._default_send1_button = None
        self._default_send2_button = None

    def disconnect(self):
        """releasing references and removing listeners"""
        if self._track != None:
            sends = self._track.mixer_device.sends
            if len(sends) > 0 and sends[0].value_has_listener(self._on_send1_changed):
                sends[0].remove_value_listener(self._on_send1_changed)
            if len(sends) > 1 and sends[1].value_has_listener(self._on_send2_changed):
                sends[1].remove_value_listener(self._on_send2_changed)
        if self._default_send1_button != None:
            self._default_send1_button.remove_value_listener(self._default_send1_value)
            self._default_send1_button = None
        if self._default_send2_button != None:
            self._default_send2_button.remove_value_listener(self._default_send2_value)
            self._default_send2_button = None
        ChannelStripComponent.disconnect(self)

    def set_track(self, track):
        assert (track == None) or isinstance(track, Live.Track.Track)
        if track != self._track:
            if self._track != None:
                sends = self._track.mixer_device.sends
                if len(sends) > 0 and sends[0].value_has_listener(
                    self._on_send1_changed
                ):
                    sends[0].remove_value_listener(self._on_send1_changed)
                if len(sends) > 1 and sends[1].value_has_listener(
                    self._on_send2_changed
                ):
                    sends[1].remove_value_listener(self._on_send2_changed)
            ChannelStripComponent.set_track(self, track)
        else:
            self.update()

    def set_default_buttons(self, send1, send2):
        assert (send1 == None) or isinstance(send1, ConfigurableButtonElement)
        assert (send2 == None) or isinstance(send2, ConfigurableButtonElement)
        if send1 != self._default_send1_button:
            if self._default_send1_button != None:
                self._default_send1_button.remove_value_listener(
                    self._default_send1_value
                )
            self._default_send1_button = send1
            if self._default_send1_button != None:
                self._default_send1_button.add_value_listener(self._default_send1_value)
        if send2 != self._default_send2_button:
            if self._default_send2_button != None:
                self._default_send2_button.remove_value_listener(
                    self._default_send2_value
                )
            self._default_send2_button = send2
            if self._default_send2_button != None:
                self._default_send2_button.add_value_listener(self._default_send2_value)
        self.update()

    def set_send_controls(self, controls):
        assert (controls == None) or isinstance(controls, tuple)
        if controls != self._send_controls:
            self._send_controls = controls
            if self._send_controls != None:
                for control in self._send_controls:
                    if control != None:
                        control.reset()

            self.update()

    def update(self):
        ChannelStripComponent.update(self)
        if self._allow_updates:
            if self.is_enabled():
                if self._track != None:
                    sends = self._track.mixer_device.sends
                    if len(sends) > 0:
                        if not sends[0].value_has_listener(self._on_send1_changed):
                            sends[0].add_value_listener(self._on_send1_changed)
                        self._on_send1_changed()
                    elif self._default_send1_button != None:
                        self._default_send1_button.turn_off()
                    if len(sends) > 1:
                        if not sends[1].value_has_listener(self._on_send2_changed):
                            sends[1].add_value_listener(self._on_send2_changed)
                        self._on_send2_changed()
                    elif self._default_send2_button != None:
                        self._default_send2_button.turn_off()
                else:
                    if self._default_send1_button != None:
                        self._default_send1_button.reset()
                    if self._default_send2_button != None:
                        self._default_send2_button.reset()
                    if self._send_controls != None:
                        for send_control in self._send_controls:
                            if send_control != None:
                                send_control.reset()

    def _default_send1_value(self, value):
        assert self._default_send1_button != None
        assert value in range(128)
        if self.is_enabled() and (
            (self._track != None) and (len(self._track.mixer_device.sends) > 0)
        ):
            if (value != 0) or (not self._default_send1_button.is_momentary()):
                send1 = self._track.mixer_device.sends[0]
                if send1.is_enabled:
                    send1.value = send1.default_value

    def _default_send2_value(self, value):
        assert self._default_send2_button != None
        assert value in range(128)
        if self.is_enabled() and (
            (self._track != None) and (len(self._track.mixer_device.sends) > 1)
        ):
            if (value != 0) or (not self._default_send2_button.is_momentary()):
                send2 = self._track.mixer_device.sends[1]
                if send2.is_enabled:
                    send2.value = send2.default_value

    def _on_send1_changed(self):
        assert self._track != None
        sends = self._track.mixer_device.sends
        assert len(sends) > 0
        if self.is_enabled() and (self._default_send1_button != None):
            send1 = sends[0]
            if send1.value == send1.default_value:
                self._default_send1_button.turn_on()
            else:
                self._default_send1_button.turn_off()

    def _on_send2_changed(self):
        assert self._track != None
        sends = self._track.mixer_device.sends
        assert len(sends) > 1
        if self.is_enabled() and (self._default_send2_button != None):
            send2 = sends[1]
            if send2.value == send2.default_value:
                self._default_send2_button.turn_on()
            else:
                self._default_send2_button.turn_off()
