# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v2\control_surface\control\control_list.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 12229 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
from future.moves.itertools import zip_longest
from past.utils import old_div
from functools import partial
from ...base import clamp, find_if, first, flatten, is_matrix, mixin, old_hasattr, product, second
from .control import Connectable, Control
from .radio_button import RadioButtonControl
_DYNAMIC_CONTROL_COUNT = None

class ControlList(Control):
    DYNAMIC_CONTROL_COUNT = _DYNAMIC_CONTROL_COUNT

    class State(Control.State):

        def __init__(self, control=None, manager=None, unavailable_color=None, extra_args=None, extra_kws=None, *a, **k):
            super(ControlList.State, self).__init__(manager=manager, control=control)
            self._control_elements = None
            self._control_type = control.control_type
            self._controls = []
            self._dynamic_create = False
            self._unavailable_color = unavailable_color if unavailable_color is not None else 'DefaultButton.Disabled'
            self._extra_args = a
            self._extra_kws = k
            self.control_count = control.control_count

        @property
        def control_elements(self):
            return self._control_elements

        @property
        def control_count(self):
            return len(self._controls)

        @control_count.setter
        def control_count--- This code section failed: ---

 L.  79         0  LOAD_FAST                'count'
                2  LOAD_GLOBAL              ControlList
                4  LOAD_ATTR                DYNAMIC_CONTROL_COUNT
                6  COMPARE_OP               ==
                8  STORE_FAST               'dynamic_create'

 L.  81        10  LOAD_GLOBAL              len
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                _controls
               16  CALL_FUNCTION_1       1  '1 positional argument'
               18  LOAD_FAST                'count'
               20  COMPARE_OP               !=
               22  POP_JUMP_IF_FALSE    28  'to 28'
               24  LOAD_FAST                'dynamic_create'
               26  POP_JUMP_IF_FALSE    38  'to 38'
             28_0  COME_FROM            22  '22'

 L.  82        28  LOAD_FAST                'self'
               30  LOAD_ATTR                _dynamic_create
               32  LOAD_FAST                'dynamic_create'
               34  COMPARE_OP               !=
               36  POP_JUMP_IF_FALSE    94  'to 94'
             38_0  COME_FROM            26  '26'

 L.  83        38  LOAD_FAST                'count'
               40  LOAD_GLOBAL              ControlList
               42  LOAD_ATTR                DYNAMIC_CONTROL_COUNT
               44  COMPARE_OP               ==
               46  LOAD_FAST                'self'
               48  STORE_ATTR               _dynamic_create

 L.  84        50  LOAD_FAST                'self'
               52  LOAD_ATTR                _dynamic_create
               54  POP_JUMP_IF_FALSE    76  'to 76'

 L.  85        56  LOAD_FAST                'self'
               58  LOAD_ATTR                _control_elements
               60  POP_JUMP_IF_FALSE    72  'to 72'
               62  LOAD_GLOBAL              len
               64  LOAD_FAST                'self'
               66  LOAD_ATTR                _control_elements
               68  CALL_FUNCTION_1       1  '1 positional argument'
               70  JUMP_FORWARD         74  'to 74'
             72_0  COME_FROM            60  '60'
               72  LOAD_CONST               0
             74_0  COME_FROM            70  '70'
               74  STORE_FAST               'count'
             76_0  COME_FROM            54  '54'

 L.  86        76  LOAD_FAST                'self'
               78  LOAD_METHOD              _create_controls
               80  LOAD_FAST                'count'
               82  CALL_METHOD_1         1  '1 positional argument'
               84  POP_TOP          

 L.  87        86  LOAD_FAST                'self'
               88  LOAD_METHOD              _update_controls
               90  CALL_METHOD_0         0  '0 positional arguments'
               92  POP_TOP          
             94_0  COME_FROM            36  '36'

Parse error at or near `POP_TOP' instruction at offset 92

        @property
        def unavailable_color(self):
            return self._unavailable_color

        @unavailable_color.setter
        def unavailable_color(self, value):
            self._unavailable_color = value
            control_elements = self._control_elements or []
            for control, element in zip_longest(self._controls, control_elements):
                if not control:
                    if element:
                        self._send_unavailable_color(element)

        def _create_controls(self, count):
            if count > len(self._controls):
                self._controls.extend([self._make_control(i) for i in range(len(self._controls), count)])
            else:
                if count < len(self._controls):
                    self._disconnect_controls(self._controls[count:])
                    self._controls = self._controls[:count]

        def _disconnect_controls(self, controls):
            for control in controls:
                control._get_state(self._manager).disconnect()
                control._clear_state(self._manager)

        def _make_control(self, index):
            control = (self._control_type)(*self._extra_args, **self._extra_kws)
            control._event_listeners = self._event_listeners
            control_state = control._get_state(self._manager)
            if not old_hasattr(control_state, 'index'):
                control_state.index = index
            else:
                raise RuntimeError("Cannot set 'index' attribute. Attribute already set.")
            return control

        def set_control_element(self, control_elements):
            self._control_elements = control_elements
            if self._dynamic_create:
                if len(control_elements or []) != len(self._control_element or []):
                    self._create_controls(len(control_elements or []))
            self._update_controls()

        def _update_controls(self):
            control_elements = self._control_elements or []
            for control, element in zip_longest(self._controls, control_elements):
                if control:
                    control._get_state(self._manager).set_control_element(element)
                if element:
                    element.reset_state()
                    self._send_unavailable_color(element)

        def _send_unavailable_color(self, element):
            if old_hasattr(element, 'set_light'):
                element.set_light(self._unavailable_color)

        def __getitem__(self, index):
            return self._controls[index]._get_state(self._manager)

        def _on_value(self, value, *a, **k):
            pass

        def _register_value_slot(self, manager, control):
            pass

    def __init__(self, control_type=None, control_count=_DYNAMIC_CONTROL_COUNT, *a, **k):
        (super(ControlList, self).__init__)(a, extra_args=a, extra_kws=k, **k)
        self.control_type = control_type
        self.control_count = control_count


class RadioButtonGroup(ControlList, RadioButtonControl):

    class State(ControlList.State, Connectable):
        requires_listenable_connected_property = True

        def __init__(self, *a, **k):
            self._checked_index = -1
            (super(RadioButtonGroup.State, self).__init__)(*a, **k)

        @property
        def checked_index(self):
            return self._checked_index

        @checked_index.setter
        def checked_index(self, index):
            if index != -1:
                self[index].is_checked = True
            else:
                checked_control = find_if(lambda c: c.is_checked
, self)
                if checked_control is not None:
                    checked_control.is_checked = False

        def connect_property(self, *a):
            (super(RadioButtonGroup.State, self).connect_property)(*a)
            self.checked_index = self.connected_property_value

        def on_connected_property_changed(self, value):
            self.checked_index = value

        def _create_controls(self, count):
            super(RadioButtonGroup.State, self)._create_controls(count)
            self.checked_index = clamp(self._checked_index, -1, count - 1)

        def _make_control(self, index):
            control = super(RadioButtonGroup.State, self)._make_control(index)
            control_state = control._get_state(self._manager)
            control_state._on_checked = partial(self._on_checked, control_state)
            control_state.is_checked = index == self._checked_index
            return control

        def _on_checked(self, checked_control):
            for control in self._controls:
                control = control._get_state(self._manager)
                control.is_checked = control == checked_control

            self._checked_index = checked_control.index
            self.connected_property_value = self._checked_index

    def __init__(self, *a, **k):
        (super(RadioButtonGroup, self).__init__)(RadioButtonControl, *a, **k)


_DYNAMIC_MATRIX_DIMENSIONS = (None, None)

class MatrixControl(ControlList):
    DYNAMIC_DIMENSIONS = _DYNAMIC_MATRIX_DIMENSIONS

    class State(ControlList.State):

        def __init__(self, control=None, manager=None, dimensions=None, *a, **k):
            (super(MatrixControl.State, self).__init__)(control, manager, *a, **k)
            self._dimensions = (None, None)
            if dimensions is not None:
                self.dimensions = dimensions

        @property
        def dimensions(self):
            return self._dimensions

        @dimensions.setter
        def dimensions(self, dimensions):
            self._dynamic_create = dimensions == MatrixControl.DYNAMIC_DIMENSIONS
            if self._dynamic_create:
                count = len(self._control_elements) if self._control_elements else 0
            self._dimensions = dimensions
            count = first(dimensions) * second(dimensions)
            self._create_controls(count)
            self._update_controls()

        def _create_controls(self, count):
            super(MatrixControl.State, self)._create_controls(count)
            self._update_coordinates()

        def _make_control(self, index):
            control = super(MatrixControl.State, self)._make_control(index)
            if old_hasattr(control._get_state(self._manager), 'coordinate'):
                raise RuntimeError("Cannot set 'coordinate' attribute. Attribute already set.")
            return control

        def _update_coordinates(self):
            for index, control in enumerate(self._controls):
                control_state = control._get_state(self._manager)
                control_state.coordinate = (
                 int(old_div(index, self.width)),
                 index % self.width)

        def set_control_element(self, control_elements):
            dimensions = (None, None)
            if old_hasattr(control_elements, 'width') and old_hasattr(control_elements, 'height'):
                dimensions = (control_elements.height(), control_elements.width())
                if not self._dynamic_create:
                    control_elements = [control_elements.get_button(row, col) for row, col in product(range(self.height), range(self.width))]
            else:
                if is_matrix(control_elements):
                    dimensions = (
                     len(control_elements), len(first(control_elements)))
                    if not self._dynamic_create:
                        control_elements = [row[0:self.width] for row in control_elements]
                    control_elements = list(flatten(control_elements))
                else:
                    if control_elements is not None:
                        raise RuntimeError('Control Elements must be a matrix')
            if self._dynamic_create:
                if None not in dimensions:
                    self._dimensions = dimensions
                    self._create_controls(first(dimensions) * second(dimensions))
                    self._update_controls()
            super(MatrixControl.State, self).set_control_element(control_elements)

        def get_control(self, row, column):
            index = row * self.width + column
            return self._controls[index]._get_state(self._manager)

        @property
        def width(self):
            return second(self._dimensions)

        @property
        def height(self):
            return first(self._dimensions)

    def __init__(self, *a, **k):
        (super(MatrixControl, self).__init__)(*a, **k)


_control_list_classes = dict()
_control_matrix_classes = dict()

def control_list(control_type, *a, **k):
    if control_type == RadioButtonControl:
        return RadioButtonGroup(*a, **k)
    c = _control_list_classes.get(control_type, None)
    if not c:
        c = mixin(ControlList, control_type)
        _control_list_classes[control_type] = c
    return c(control_type, *a, **k)


def control_matrix(control_type, *a, **k):
    m = _control_matrix_classes.get(control_type, None)
    if not m:
        m = mixin(MatrixControl, control_type)
        _control_matrix_classes[control_type] = m
    return m(control_type, *a, **k)