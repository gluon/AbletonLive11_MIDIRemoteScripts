import Live
from _Framework.ChannelStripComponent import ChannelStripComponent
from .ConfigurableButtonElement import ConfigurableButtonElement
from itertools import chain


class SendsChannelStripComponent(ChannelStripComponent):
    def __init__(self):
        ChannelStripComponent.__init__(self)
        self._default_send_buttons = {}

    def disconnect(self):
        """releasing references and removing listeners"""
        if self._track != None:
            sends = self._track.mixer_device.sends
            for send in sends:
                if sends[0].value_has_listener(self._on_send0_changed):
                    sends[0].remove_value_listener(self._on_send0_changed)
                if sends[1].value_has_listener(self._on_send1_changed):
                    sends[1].remove_value_listener(self._on_send1_changed)
                # TODO Add more sends
        for (
            default_send_button_idx,
            default_send_button,
        ) in self._default_send_buttons:
            if default_send_button != None:
                self._default_send_buttons[
                    default_send_button_idx
                ].remove_value_listener(
                    self._default_send_buttons[default_send_button_idx]
                )
                self._default_send_buttons[default_send_button_idx] = None
        ChannelStripComponent.disconnect(self)

    def set_track(self, track):
        assert (track == None) or isinstance(track, Live.Track.Track)
        if track != self._track:
            if self._track != None:
                sends = self._track.mixer_device.sends
                send_idx = 0
                for send in sends:
                    if send_idx == 0 and sends[send_idx].value_has_listener(
                        self._on_send0_changed
                    ):
                        sends[send_idx].remove_value_listener(self._on_send0_changed)
                    elif send_idx == 1 and sends[send_idx].value_has_listener(
                        self._on_send1_changed
                    ):
                        sends[send_idx].remove_value_listener(self._on_send1_changed)
                    send_idx += 1
                # TODO Add more sends
            ChannelStripComponent.set_track(self, track)
        else:
            self.update()

    def set_default_buttons(self, *send_buttons):
        if (
            send_buttons is not None
            and len(send_buttons) > 0
            and self._default_send_buttons is not None
            and len(self._default_send_buttons) > 0
        ):
            self._control_surface.log_message("It do happen!")
            send_button_idx = 0
            for send_button in send_buttons:
                assert (send_button == None) or isinstance(
                    send_button, ConfigurableButtonElement
                )
                if send_button != self._default_send_buttons[send_button_idx]:
                    if self._default_send_buttons[send_button_idx] != None:
                        self._default_send_buttons[
                            send_button_idx
                        ].remove_value_listener()
                    self._default_send_buttons[send_button_idx] = send_button
                    if self._default_send_buttons[send_button_idx] != None:
                        if send_button_idx == 0:
                            self._default_send_buttons[
                                send_button_idx
                            ].add_value_listener(self._default_send0_value)
                        elif send_button_idx == 1:
                            self._default_send_buttons[
                                send_button_idx
                            ].add_value_listener(self._default_send1_value)
                        # TODO Add more sends
                send_button_idx += 1
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
                    send_idx = 0
                    for send in sends:
                        if send_idx == 0 and not send.value_has_listener(
                            self._on_send0_changed
                        ):
                            send.add_value_listener(self._on_send0_changed)
                        elif send_idx == 1 and not send.value_has_listener(
                            self._on_send1_changed
                        ):
                            send.add_value_listener(self._on_send1_changed)
                        self._on_send_changed(send_idx)
                        send_idx += 1

                    # TODO turn off send buttons if they aren't sends there anymore!!
                    # elif self._default_send0_button != None:
                    #     self._default_send0_button.turn_off()
                    # elif self._default_send1_button != None:
                    #     self._default_send1_button.turn_off()
                else:
                    for default_send_button in self._default_send_buttons:
                        if self.default_send_button != None:
                            self.default_send_button.reset()
                        if self._send_controls != None:
                            for send_control in self._send_controls:
                                if send_control != None:
                                    send_control.reset()

    def _default_send_value(self, send_number, value):
        assert self._default_send_buttons[send_number] != None
        assert value in range(128)
        if self.is_enabled() and (
            (self._track != None) and (len(self._track.mixer_device.sends) > 0)
        ):
            if (value != 0) or (
                not self._default_send_buttons[send_number].is_momentary()
            ):
                send = self._track.mixer_device.sends[send_number]
                if send.is_enabled:
                    send.value = send.default_value

    def _default_send0_value(self, value):
        self._default_send_value(value, 0)

    def _default_send1_value(self, value):
        self._default_send_value(value, 1)

    # TODO add more sends

    def _on_send_changed(self, send_number):
        assert self._track != None
        sends = self._track.mixer_device.sends
        assert len(sends) > 0
        if self.is_enabled() and len(self._default_send_buttons) > send_number:
            if self._default_send_buttons[send_number] != None:
                send = sends[send_number]
                if send.value == send.default_value:
                    self._default_send_buttons[send_number].turn_on()
                else:
                    self._default_send_buttons[send_number].turn_off()

    def _on_send0_changed(self):
        self._on_send_changed(self, 0)

    def _on_send1_changed(self):
        self._on_send_changed(self, 0)
