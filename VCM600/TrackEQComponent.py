#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/VCM600/TrackEQComponent.py
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
import Live
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.EncoderElement import EncoderElement
from _Generic.Devices import get_parameter_by_name
EQ_DEVICES = {u'Eq8': {u'Gains': [ u'%i Gain A' % (index + 1) for index in range(8) ]},
 u'FilterEQ3': {u'Gains': [u'GainLo', u'GainMid', u'GainHi'],
                u'Cuts': [u'LowOn', u'MidOn', u'HighOn']}}

class TrackEQComponent(ControlSurfaceComponent):
    u""" Class representing a track's EQ, it attaches to the last EQ device in the track """

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
            if u'Cuts' in list(device_dict.keys()):
                cut_names = device_dict[u'Cuts']
                for cut_name in cut_names:
                    parameter = get_parameter_by_name(self._device, cut_name)
                    if parameter != None and parameter.value_has_listener(self._on_cut_changed):
                        parameter.remove_value_listener(self._on_cut_changed)

    def on_enabled_changed(self):
        self.update()

    def set_track(self, track):
        assert track == None or isinstance(track, Live.Track.Track)
        if self._track != None:
            self._track.remove_devices_listener(self._on_devices_changed)
            if self._gain_controls != None and self._device != None:
                for control in self._gain_controls:
                    control.release_parameter()

        self._track = track
        if self._track != None:
            self._track.add_devices_listener(self._on_devices_changed)
        self._on_devices_changed()

    def set_cut_buttons(self, buttons):
        assert buttons == None or isinstance(buttons, tuple)
        if buttons != self._cut_buttons:
            if self._cut_buttons != None:
                for button in self._cut_buttons:
                    button.remove_value_listener(self._cut_value)

            self._cut_buttons = buttons
            if self._cut_buttons != None:
                for button in self._cut_buttons:
                    button.add_value_listener(self._cut_value, identify_sender=True)

            self.update()

    def set_gain_controls(self, controls):
        assert controls != None
        assert isinstance(controls, tuple)
        if self._device != None and self._gain_controls != None:
            for control in self._gain_controls:
                control.release_parameter()

        for control in controls:
            assert control != None
            assert isinstance(control, EncoderElement)

        self._gain_controls = controls
        self.update()

    def update(self):
        super(TrackEQComponent, self).update()
        if self.is_enabled() and self._device != None:
            device_dict = EQ_DEVICES[self._device.class_name]
            if self._gain_controls != None:
                gain_names = device_dict[u'Gains']
                for index in range(len(self._gain_controls)):
                    self._gain_controls[index].release_parameter()
                    if len(gain_names) > index:
                        parameter = get_parameter_by_name(self._device, gain_names[index])
                        if parameter != None:
                            self._gain_controls[index].connect_to(parameter)

            if self._cut_buttons != None and u'Cuts' in list(device_dict.keys()):
                cut_names = device_dict[u'Cuts']
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
        assert sender in self._cut_buttons
        assert value in range(128)
        if self.is_enabled() and self._device != None:
            if not sender.is_momentary() or value is not 0:
                device_dict = EQ_DEVICES[self._device.class_name]
                if u'Cuts' in list(device_dict.keys()):
                    cut_names = device_dict[u'Cuts']
                    index = list(self._cut_buttons).index(sender)
                    if index in range(len(cut_names)):
                        parameter = get_parameter_by_name(self._device, cut_names[index])
                        if parameter != None and parameter.is_enabled:
                            parameter.value = float(int(parameter.value + 1) % 2)

    def _on_devices_changed(self):
        if self._device != None:
            device_dict = EQ_DEVICES[self._device.class_name]
            if u'Cuts' in list(device_dict.keys()):
                cut_names = device_dict[u'Cuts']
                for cut_name in cut_names:
                    parameter = get_parameter_by_name(self._device, cut_name)
                    if parameter != None and parameter.value_has_listener(self._on_cut_changed):
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
        assert self._device != None
        assert u'Cuts' in list(EQ_DEVICES[self._device.class_name].keys())
        if self.is_enabled() and self._cut_buttons != None:
            cut_names = EQ_DEVICES[self._device.class_name][u'Cuts']
            for index in range(len(self._cut_buttons)):
                self._cut_buttons[index].turn_off()
                if len(cut_names) > index:
                    parameter = get_parameter_by_name(self._device, cut_names[index])
                    if parameter != None and parameter.value == 0.0:
                        self._cut_buttons[index].turn_on()
