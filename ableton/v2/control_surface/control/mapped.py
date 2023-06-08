from __future__ import absolute_import, print_function, unicode_literals
from ...base import clamp, listens, liveobj_valid, old_hasattr
from control_surface.internal_parameter import InternalParameterBase
from .control import InputControl
from .encoder import ValueStepper

class MappedControl(InputControl):

    class State(InputControl.State):

        def __init__(self, control=None, manager=None, *a, **k):
            (super(MappedControl.State, self).__init__)(a, control=control, manager=manager, **k)
            self._direct_mapping = None

        def set_control_element(self, control_element):
            if self._control_element:
                self._control_element.release_parameter()
            super(MappedControl.State, self).set_control_element(control_element)
            self._update_direct_connection()
            self._update_value_slot()

        @property
        def mapped_parameter(self):
            return self._direct_mapping

        @mapped_parameter.setter
        def mapped_parameter(self, direct_mapping):
            self._direct_mapping = direct_mapping
            self._update_direct_connection()
            self._update_value_slot()

        def _event_listener_required(self):
            return True

        def _update_direct_connection(self):
            if self._control_element:
                self._control_element.connect_to(self._direct_mapping)

        def _update_value_slot(self):
            self._value_slot.subject = None if liveobj_valid(self._direct_mapping) else self._control_element

        def _notifications_enabled(self):
            return super(MappedControl.State, self)._notifications_enabled() and self._direct_mapping is None

    def __init__(self, *a, **k):
        super(MappedControl, self).__init__(extra_args=a, extra_kws=k)


def is_internal_parameter(parameter):
    return isinstance(parameter, InternalParameterBase)


def is_zoom_parameter(parameter):
    return old_hasattr(parameter, 'zoom')


class MappedSensitivitySettingControl(MappedControl):
    DEFAULT_SENSITIVITY = 1.0
    FINE_SENSITIVITY = 0.1

    class State(MappedControl.State):

        def __init__(self, *a, **k):
            (super(MappedSensitivitySettingControl.State, self).__init__)(*a, **k)
            self.default_sensitivity = MappedSensitivitySettingControl.DEFAULT_SENSITIVITY
            self.fine_sensitivity = MappedSensitivitySettingControl.FINE_SENSITIVITY
            self._quantized_stepper = ValueStepper()

        def update_sensitivities(self, default, fine):
            self.default_sensitivity = default
            self.fine_sensitivity = fine
            if self._control_element:
                self._update_control_sensitivity()

        def _update_direct_connection(self):
            if self._control_element is None or is_internal_parameter(self.mapped_parameter):
                if self._control_element:
                    self._control_element.release_parameter()
                self._control_value.subject = self._control_element
            else:
                self._control_value.subject = None
                self._update_control_element()
            self._quantized_stepper.reset()

        def _update_control_element(self):
            if liveobj_valid(self.mapped_parameter):
                self._control_element.connect_to(self.mapped_parameter)
            else:
                self._control_element.release_parameter()
            self._update_control_sensitivity()
            self._quantized_stepper.reset()

        def _update_control_sensitivity(self):
            if old_hasattr(self._control_element, 'set_sensitivities'):
                self._control_element.set_sensitivities(self.default_sensitivity, self.fine_sensitivity)
            else:
                self._control_element.mapping_sensitivity = self.default_sensitivity

        @listens('normalized_value')
        def _control_value(self, value):
            if is_zoom_parameter(self.mapped_parameter):
                self.mapped_parameter.zoom(value * self._control_element.mapping_sensitivity)
            if self.mapped_parameter.is_quantized:
                steps = self._quantized_stepper.advance(value)
                if steps != 0:
                    self.mapped_parameter.value = self._clamp_value_to_parameter_range(self.mapped_parameter.value + steps)
            else:
                value_offset = value * self._control_element.mapping_sensitivity
                self.mapped_parameter.linear_value = self._clamp_value_to_parameter_range(self.mapped_parameter.linear_value + value_offset)

        def _clamp_value_to_parameter_range(self, value):
            return clamp(value, self.mapped_parameter.min, self.mapped_parameter.max)