# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\selected_track_parameter_provider.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 949 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface import ParameterInfo
from pushbase.selected_track_parameter_provider import SelectedTrackParameterProvider as SelectedTrackParameterProviderBase
from .parameter_mapping_sensitivities import fine_grain_parameter_mapping_sensitivity, parameter_mapping_sensitivity

class SelectedTrackParameterProvider(SelectedTrackParameterProviderBase):

    def _create_parameter_info(self, parameter, name):
        return ParameterInfo(name=name,
          parameter=parameter,
          default_encoder_sensitivity=(parameter_mapping_sensitivity(parameter)),
          fine_grain_encoder_sensitivity=(fine_grain_parameter_mapping_sensitivity(parameter)))