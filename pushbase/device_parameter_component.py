# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\pushbase\device_parameter_component.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 3425 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import map, str
from future.moves.itertools import zip_longest
from past.utils import old_div
import Live
from ableton.v2.base import is_parameter_bipolar, listens_group
from ableton.v2.control_surface.components import DisplayingDeviceParameterComponent as DeviceParameterComponentBase
from ableton.v2.control_surface.elements import DisplayDataSource
from . import consts
AutomationState = Live.DeviceParameter.AutomationState

def graphic_bar_for_parameter(parameter):
    if is_parameter_bipolar(parameter):
        return consts.GRAPH_PAN
    if parameter.is_quantized:
        return consts.GRAPH_SIN
    return consts.GRAPH_VOL


def convert_parameter_value_to_graphic(param, param_to_value=lambda p: p.value
):
    if param != None:
        param_range = param.max - param.min
        param_bar = graphic_bar_for_parameter(param)
        graph_range = len(param_bar) - 1
        value = int(old_div(float(param_to_value(param) - param.min), param_range) * graph_range)
        graphic_display_string = param_bar[value]
    else:
        graphic_display_string = ' '
    return graphic_display_string


class DeviceParameterComponent(DeviceParameterComponentBase):

    def __init__(self, *a, **k):
        self._parameter_graphic_data_sources = list(map(DisplayDataSource, ('', '',
                                                                            '', '',
                                                                            '', '',
                                                                            '', '')))
        (super(DeviceParameterComponent, self).__init__)(*a, **k)

    def set_graphic_display_line(self, line):
        self._set_display_line(line, self._parameter_graphic_data_sources)

    def clear_display(self):
        super(DeviceParameterComponent, self).clear_display()
        for source in self._parameter_graphic_data_sources:
            source.set_display_string('')

    def _update_parameters(self):
        super(DeviceParameterComponent, self)._update_parameters()
        if self.is_enabled():
            self._on_parameter_automation_state_changed.replace_subjects(self.parameters)

    @listens_group('automation_state')
    def _on_parameter_automation_state_changed(self, parameter):
        self._update_parameter_names()
        self._update_parameter_values()

    def _update_parameter_values(self):
        super(DeviceParameterComponent, self)._update_parameter_values()
        if self.is_enabled():
            for param, data_source in zip_longest(self.parameters, self._parameter_graphic_data_sources):
                graph = convert_parameter_value_to_graphic(param, self.parameter_to_value)
                if data_source:
                    data_source.set_display_string(graph)

    def info_to_name(self, info):
        parameter = info and info.parameter
        name = info and (info.name) or ''
        if parameter:
            if parameter.automation_state != AutomationState.none:
                name = consts.CHAR_FULL_BLOCK + name
        return name

    def parameter_to_string(self, parameter):
        s = '' if parameter == None else str(parameter)
        if parameter:
            if parameter.automation_state == AutomationState.overridden:
                s = '[%s]' % s
        return s