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