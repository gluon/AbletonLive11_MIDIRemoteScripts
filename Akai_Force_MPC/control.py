#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Akai_Force_MPC/control.py
from __future__ import absolute_import, print_function, unicode_literals
from past.utils import old_div
from ableton.v2.base import clamp, listens, liveobj_valid
from ableton.v2.control_surface.control import InputControl, MappedControl, MappedSensitivitySettingControl, SendValueMixin, is_internal_parameter

class SendReceiveValueControl(InputControl):

    class State(SendValueMixin, InputControl.State):
        pass


class MappedAbsoluteControl(MappedControl):
    u"""
    Control that maps ControlElements with an absolute map mode to
    Live parameters. Supports internal parameters.
    """

    class State(MappedControl.State):

        def _update_direct_connection(self):
            if self._control_element is None:
                self._control_value.subject = None
            if is_internal_parameter(self.mapped_parameter):
                self._connect_to_internal_parameter()
            else:
                self._connect_to_parameter()

        def _connect_to_internal_parameter(self):
            if self._control_element:
                self._control_element.release_parameter()
                self._control_value.subject = self._control_element

        def _connect_to_parameter(self):
            self._control_value.subject = None
            if self._control_element is not None:
                parameter = self.mapped_parameter
                if liveobj_valid(parameter):
                    self._control_element.connect_to(parameter)
                else:
                    self._control_element.release_parameter()

        @listens(u'value')
        def _control_value(self, value):
            mapped_parameter = self.mapped_parameter
            if mapped_parameter.is_quantized:
                num_items = len(mapped_parameter.value_items)
                if num_items > 0:
                    mapped_parameter.value = value * num_items // 128
            else:
                mapped_parameter.linear_value = self._midi_value_to_parameter_value(value)

        def _midi_value_to_parameter_value(self, value):
            parameter = self.mapped_parameter
            parameter_min = parameter.min
            parameter_max = parameter.max
            normalized_value = clamp(old_div(value, 127.0), 0.0, 1.0)
            return clamp((parameter_min + parameter_max) * normalized_value, parameter_min, parameter_max)


class SendingMappedAbsoluteControl(MappedAbsoluteControl):

    class State(SendValueMixin, MappedAbsoluteControl.State):
        pass


class SendingMappedSensitivitySettingControl(MappedSensitivitySettingControl):

    class State(SendValueMixin, MappedSensitivitySettingControl.State):
        pass
