# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchpad_MK2\MixerComponent.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 6296 bytes
from __future__ import absolute_import, print_function, unicode_literals
from _Framework.Control import ButtonControl
from _Framework.MixerComponent import MixerComponent as MixerComponentBase
from . import consts
from .ChannelStripComponent import ChannelStripComponent

class MixerComponent(MixerComponentBase):
    unmute_all_button = ButtonControl(color='Mixer.Mute.Off',
      pressed_color='Mixer.Mute.On')
    unsolo_all_button = ButtonControl(color='Mixer.Solo.Off',
      pressed_color='Mixer.Solo.On')
    unarm_all_button = ButtonControl(color='Mixer.Arm.Off', pressed_color='Mixer.Arm.On')

    def __init__(self, enable_skinning=False, *a, **k):
        (super(MixerComponent, self).__init__)(*a, **k)
        self._volume_on_value = 127
        self._volume_off_value = 0
        self._pan_on_value = 127
        self._pan_off_value = 0
        if enable_skinning:
            self._enable_skinning()

    def _create_strip(self):
        return ChannelStripComponent()

    def _enable_skinning(self):
        self.set_volume_values('Mixer.Volume.On', 'Mixer.Volume.Off')
        self.set_pan_values('Mixer.Pan.On', 'Mixer.Pan.Off')
        for strip in self._channel_strips:
            strip.empty_color = 'Mixer.Disabled'
            strip.set_arm_values('Mixer.Arm.On', 'Mixer.Arm.Off')
            strip.set_solo_values('Mixer.Solo.On', 'Mixer.Solo.Off')
            strip.set_mute_values('Mixer.Mute.On', 'Mixer.Mute.Off')

    def set_volume_values(self, volume_on_value, volume_off_value):
        self._volume_on_value = volume_on_value
        self._volume_off_value = volume_off_value

    def set_pan_values(self, pan_on_value, pan_off_value):
        self._pan_on_value = pan_on_value
        self._pan_off_value = pan_off_value

    def set_volume_controls(self, controls):
        if controls is not None:
            for control in controls:
                if control is not None:
                    control.set_channel(consts.VOLUME_MODE_CHANNEL)

        super(MixerComponent, self).set_volume_controls(controls)
        if controls is not None:
            for index, control in enumerate(controls):
                control.index = index
                control.type = consts.FADER_STANDARD_TYPE
                control.color = self._volume_on_value

    def set_pan_controls(self, controls):
        if controls is not None:
            for control in controls:
                if control is not None:
                    control.set_channel(consts.PAN_MODE_CHANNEL)

        super(MixerComponent, self).set_pan_controls(controls)
        if controls is not None:
            for index, control in enumerate(controls):
                control.index = index
                control.type = consts.FADER_BIPOLAR_TYPE
                control.color = self._pan_on_value

    def set_send_a_controls(self, controls):
        self._set_send_controls(controls, 0)

    def set_send_b_controls(self, controls):
        self._set_send_controls(controls, 1)

    def _set_send_controls(self, controls, send_index):
        translation_channel = 0
        if send_index == 0:
            translation_channel = consts.SEND_A_MODE_CHANNEL
        else:
            if send_index == 1:
                translation_channel = consts.SEND_B_MODE_CHANNEL
        if controls is not None:
            for index, control in enumerate(controls):
                if control is not None:
                    self.channel_strip(index).set_send_controls((None, ) * send_index + (control,))
                    control.set_channel(translation_channel)
                    control.index = index
                    control.type = consts.FADER_STANDARD_TYPE
                    control.color = 'Sends.Send%d.On' % send_index

        else:
            for strip in self._channel_strips:
                strip.set_send_controls(None)

    def set_volume_reset_buttons(self, buttons):
        if buttons is not None:
            for index, strip in enumerate(self._channel_strips):
                strip.volume_reset_button.set_control_element(buttons.get_button(index, 0))

        else:
            for strip in self._channel_strips:
                strip.volume_reset_button.set_control_element(None)

    def set_pan_reset_buttons(self, buttons):
        if buttons is not None:
            for index, strip in enumerate(self._channel_strips):
                strip.pan_reset_button.set_control_element(buttons.get_button(index, 0))

        else:
            for strip in self._channel_strips:
                strip.pan_reset_button.set_control_element(None)

    def set_send_a_reset_buttons(self, buttons):
        if buttons is not None:
            for index, strip in enumerate(self._channel_strips):
                strip.send_a_reset_button.set_control_element(buttons.get_button(index, 0))

        else:
            for strip in self._channel_strips:
                strip.send_a_reset_button.set_control_element(None)

    def set_send_b_reset_buttons(self, buttons):
        if buttons is not None:
            for index, strip in enumerate(self._channel_strips):
                strip.send_b_reset_button.set_control_element(buttons.get_button(index, 0))

        else:
            for strip in self._channel_strips:
                strip.send_b_reset_button.set_control_element(None)

    @unmute_all_button.pressed
    def unmute_all_button(self, button):
        for track in tuple(self.song().tracks) + tuple(self.song().return_tracks):
            if track.mute:
                track.mute = False

    @unsolo_all_button.pressed
    def unsolo_all_button(self, button):
        for track in tuple(self.song().tracks) + tuple(self.song().return_tracks):
            if track.solo:
                track.solo = False

    @unarm_all_button.pressed
    def unarm_all_button(self, button):
        for track in self.song().tracks:
            if track.arm:
                track.arm = False