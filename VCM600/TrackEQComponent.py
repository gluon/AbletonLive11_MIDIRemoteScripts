# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\VCM600\TrackEQComponent.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 7932 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
import Live
from _Generic.Devices import get_parameter_by_name
import _Framework.ControlSurfaceComponent as ControlSurfaceComponent
import _Framework.EncoderElement as EncoderElement
EQ_DEVICES = {'Eq8':{'Gains': ['%i Gain A' % (index + 1) for index in range(8)]}, 
 'FilterEQ3':{'Gains':[
   'GainLo', 'GainMid', 'GainHi'], 
  'Cuts':[
   'LowOn', 'MidOn', 'HighOn']}}

class TrackEQComponent(ControlSurfaceComponent):

    def __init__(self):
        ControlSurfaceComponent.__init__(self)
        self._track = None
        self._device = None
        self._gain_controls = None
        self._cut_buttons = None

    def disconnect(self):
        if self._gain_controls != None:
            for control in self._gain_controls:
                control.release_parameter()

            self._gain_controls = None
        if self._cut_buttons != None:
            for button in self._cut_buttons:
                button.remove_value_listener(self._cut_value)

        self._cut_buttons = None
        if self._track != None:
            self._track.remove_devices_listener(self._on_devices_changed)
            self._track = None
        self._device = None
        if self._device != None:
            device_dict = EQ_DEVICES[self._device.class_name]
            if 'Cuts' in list(device_dict.keys()):
                cut_names = device_dict['Cuts']
                for cut_name in cut_names:
                    parameter = get_parameter_by_name(self._device, cut_name)
                    if parameter != None:
                        if parameter.value_has_listener(self._on_cut_changed):
                            parameter.remove_value_listener(self._on_cut_changed)

    def on_enabled_changed(self):
        self.update()

    def set_track(self, track):
        if self._track != None:
            self._track.remove_devices_listener(self._on_devices_changed)
            if self._gain_controls != None:
                if self._device != None:
                    for control in self._gain_controls:
                        control.release_parameter()

        self._track = track
        if self._track != None:
            self._track.add_devices_listener(self._on_devices_changed)
        self._on_devices_changed()

    def set_cut_buttons(self, buttons):
        if buttons != self._cut_buttons:
            if self._cut_buttons != None:
                for button in self._cut_buttons:
                    button.remove_value_listener(self._cut_value)

            self._cut_buttons = buttons
            if self._cut_buttons != None:
                for button in self._cut_buttons:
                    button.add_value_listener((self._cut_value), identify_sender=True)

            self.update()

    def set_gain_controls(self, controls):
        if self._device != None:
            if self._gain_controls != None:
                for control in self._gain_controls:
                    control.release_parameter()

        for control in controls:
            pass

        self._gain_controls = controls
        self.update()

    def update(self):
        super(TrackEQComponent, self).update()
        if self.is_enabled() and self._device != None:
            device_dict = EQ_DEVICES[self._device.class_name]
            if self._gain_controls != None:
                gain_names = device_dict['Gains']
                for index in range(len(self._gain_controls)):
                    self._gain_controls[index].release_parameter()
                    if len(gain_names) > index:
                        parameter = get_parameter_by_name(self._device, gain_names[index])
                        if parameter != None:
                            self._gain_controls[index].connect_to(parameter)

            if not self._cut_buttons != None or 'Cuts' in list(device_dict.keys()):
                cut_names = device_dict['Cuts']
                for index in range(len(self._cut_buttons)):
                    self._cut_buttons[index].turn_off()
                    if len(cut_names) > index:
                        parameter = get_parameter_by_name(self._device, cut_names[index])
                        if parameter != None:
                            if parameter.value == 0.0:
                                self._cut_buttons[index].turn_on()
                            if not parameter.value_has_listener(self._on_cut_changed):
                                parameter.add_value_listener(self._on_cut_changed)

        else:
            if self._cut_buttons != None:
                for button in self._cut_buttons:
                    if button != None:
                        button.turn_off()

            if self._gain_controls != None:
                for control in self._gain_controls:
                    control.release_parameter()

    def _cut_value(self, value, sender):
        if self.is_enabled():
            if self._device != None:
                if not sender.is_momentary() or value is not 0:
                    device_dict = EQ_DEVICES[self._device.class_name]
                    if 'Cuts' in list(device_dict.keys()):
                        cut_names = device_dict['Cuts']
                        index = list(self._cut_buttons).index(sender)
                        if index in range(len(cut_names)):
                            parameter = get_parameter_by_name(self._device, cut_names[index])
                            if parameter != None:
                                if parameter.is_enabled:
                                    parameter.value = float(int(parameter.value + 1) % 2)

    def _on_devices_changed(self):
        if self._device != None:
            device_dict = EQ_DEVICES[self._device.class_name]
            if 'Cuts' in list(device_dict.keys()):
                cut_names = device_dict['Cuts']
                for cut_name in cut_names:
                    parameter = get_parameter_by_name(self._device, cut_name)
                    if parameter != None:
                        if parameter.value_has_listener(self._on_cut_changed):
                            parameter.remove_value_listener(self._on_cut_changed)

        self._device = None
        if self._track != None:
            for index in range(len(self._track.devices)):
                device = self._track.devices[-1 * (index + 1)]
                if device.class_name in list(EQ_DEVICES.keys()):
                    self._device = device
                    break

        self.update()

    def _on_cut_changed(self):
        if self.is_enabled():
            if self._cut_buttons != None:
                cut_names = EQ_DEVICES[self._device.class_name]['Cuts']
                for index in range(len(self._cut_buttons)):
                    self._cut_buttons[index].turn_off()
                    if len(cut_names) > index:
                        parameter = get_parameter_by_name(self._device, cut_names[index])
                        if parameter != None:
                            if parameter.value == 0.0:
                                self._cut_buttons[index].turn_on()