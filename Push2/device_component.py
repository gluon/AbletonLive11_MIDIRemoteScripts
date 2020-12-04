#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Push2/device_component.py
from __future__ import absolute_import, print_function, unicode_literals
from collections import namedtuple
from functools import partial
import re
from MidiRemoteScript import MutableVector
from ableton.v2.base import EventError, const, listenable_property, listens, liveobj_valid
from ableton.v2.control_surface import DeviceProvider as DeviceProviderBase, ParameterInfo
from ableton.v2.control_surface.components import DeviceComponent as DeviceComponentBase
from ableton.v2.control_surface.control import control_list, ButtonControl
from pushbase.song_utils import find_parent_track
from .colors import COLOR_INDEX_TO_SCREEN_COLOR
from .device_parameter_bank_with_options import create_device_bank_with_options, OPTIONS_PER_BANK
from .parameter_mapping_sensitivities import PARAMETER_SENSITIVITIES, DEFAULT_SENSITIVITY_KEY, FINE_GRAINED_SENSITIVITY_KEY, parameter_mapping_sensitivity, fine_grain_parameter_mapping_sensitivity

def make_vector(items):
    vector = MutableVector()
    for item in items:
        vector.append(item)

    return vector


def parameter_sensitivities(device_class, parameter):
    sensitivities = {}
    try:
        param_name = parameter.name if liveobj_valid(parameter) else u''
        sensitivities = PARAMETER_SENSITIVITIES[device_class][param_name]
    except KeyError:
        pass

    for key, getter in ((DEFAULT_SENSITIVITY_KEY, parameter_mapping_sensitivity), (FINE_GRAINED_SENSITIVITY_KEY, fine_grain_parameter_mapping_sensitivity)):
        if key not in sensitivities:
            sensitivities[key] = getter(parameter)

    return sensitivities


ButtonRange = namedtuple(u'ButtonRange', [u'left_index', u'right_index'])

class Push2DeviceProvider(DeviceProviderBase):
    allow_update_callback = const(True)

    def update_device_selection(self):
        if self.allow_update_callback():
            super(Push2DeviceProvider, self).update_device_selection()


class GenericDeviceComponent(DeviceComponentBase):
    parameter_touch_buttons = control_list(ButtonControl, control_count=8)
    shift_button = ButtonControl()

    def __init__(self, visualisation_real_time_data = None, delete_button = None, *a, **k):
        super(GenericDeviceComponent, self).__init__(*a, **k)
        self._visualisation_real_time_data = visualisation_real_time_data
        self._delete_button = delete_button
        self.default_sensitivity = partial(self._sensitivity, DEFAULT_SENSITIVITY_KEY)
        self.fine_sensitivity = partial(self._sensitivity, FINE_GRAINED_SENSITIVITY_KEY)

    def set_device(self, device):
        self._set_device(device)

    def _set_device(self, device):
        super(GenericDeviceComponent, self)._set_device(device)
        self.notify_options()

    def _on_device_changed(self, device):
        u"""
        Override the base class behaviour, which calls _set_device when a device in
        the device provider changes. It's already donne by the DeviceComponentProvider.
        """
        pass

    @parameter_touch_buttons.pressed
    def parameter_touch_buttons(self, button):
        if button.index < len(self._provided_parameters):
            parameter = self._provided_parameters[button.index].parameter
            self._parameter_touched(parameter)

    @parameter_touch_buttons.released
    def parameter_touch_buttons(self, button):
        if button.index < len(self._provided_parameters):
            parameter = self._provided_parameters[button.index].parameter
            self._parameter_released(parameter)

    def parameters_changed(self):
        pass

    def _parameter_touched(self, parameter):
        pass

    def _parameter_released(self, parameter):
        pass

    @shift_button.pressed
    def shift_button(self, button):
        self._shift_button_pressed(button)

    @shift_button.released
    def shift_button(self, button):
        self._shift_button_released(button)

    def _shift_button_pressed(self, button):
        pass

    def _shift_button_released(self, button):
        pass

    def initialize_visualisation_view_data(self):
        view_data = self._initial_visualisation_view_data()
        if view_data:
            self._update_visualisation_view_data(view_data)

    def _update_visualisation_view_data(self, view_data):
        visualisation = self._visualisation_real_time_data.device_visualisation()
        if liveobj_valid(visualisation):
            visualisation_view_data = visualisation.get_view_data()
            for key, value in view_data.items():
                visualisation_view_data[key] = value

            visualisation.set_view_data(visualisation_view_data)

    def _initial_visualisation_view_data(self):
        return {}

    def _is_parameter_available(self, parameter):
        return True

    def _create_parameter_info(self, parameter, name):
        return ParameterInfo(parameter=parameter if self._is_parameter_available(parameter) else None, name=name, default_encoder_sensitivity=self.default_sensitivity(parameter), fine_grain_encoder_sensitivity=self.fine_sensitivity(parameter))

    def _sensitivity(self, sensitivity_key, parameter):
        device = self.device()
        sensitivity = parameter_sensitivities(device.class_name, parameter)[sensitivity_key]
        if liveobj_valid(parameter):
            sensitivity = self._adjust_parameter_sensitivity(parameter, sensitivity)
        return sensitivity

    def _adjust_parameter_sensitivity(self, parameter, sensitivity):
        return sensitivity

    @listenable_property
    def options(self):
        return getattr(self._bank, u'options', [None] * OPTIONS_PER_BANK)

    @property
    def bank_view_description(self):
        return getattr(self._bank, u'bank_view_description', u'')

    @listenable_property
    def visualisation_visible(self):
        return self._visualisation_visible

    @property
    def _visualisation_visible(self):
        return False

    @listenable_property
    def shrink_parameters(self):
        return self._shrink_parameters

    @property
    def _shrink_parameters(self):
        return [False] * 8

    @listens(u'options')
    def __on_options_changed(self):
        self.notify_options()

    def _setup_bank(self, device):
        super(GenericDeviceComponent, self)._setup_bank(device, bank_factory=create_device_bank_with_options)
        try:
            self.__on_options_changed.subject = self._bank
        except EventError:
            pass


class DeviceComponentWithTrackColorViewData(GenericDeviceComponent):

    def _set_device(self, device):
        super(DeviceComponentWithTrackColorViewData, self)._set_device(device)
        self.__on_device_active_changed.subject = device if liveobj_valid(device) else None
        parent_track = find_parent_track(self._decorated_device)
        self.__on_track_mute_changed.subject = parent_track
        self.__on_track_muted_via_solo_changed.subject = parent_track
        self.__on_track_or_chain_color_changed.subject = device.canonical_parent if liveobj_valid(device) else None

    def _initial_visualisation_view_data(self):
        view_data = {u'IsActive': self._is_active_for_visualisation()}
        track_color = self._track_color_for_visualisation()
        if track_color is not None:
            view_data[u'TrackColor'] = track_color
        return view_data

    def _is_active_for_visualisation(self):
        device = self._decorated_device
        parent_track = find_parent_track(self._decorated_device)
        if liveobj_valid(device) and liveobj_valid(parent_track):
            if parent_track == self.song.master_track:
                return device.is_active
            return device.is_active and not parent_track.mute and not parent_track.muted_via_solo
        return False

    def _track_color_for_visualisation(self):
        device = self._decorated_device
        canonical_parent = device.canonical_parent if liveobj_valid(device) else None
        if liveobj_valid(canonical_parent) and canonical_parent.color_index is not None:
            color = COLOR_INDEX_TO_SCREEN_COLOR[canonical_parent.color_index]
            return color.as_remote_script_color()

    @listens(u'is_active')
    def __on_device_active_changed(self):
        self._update_is_active()

    @listens(u'mute')
    def __on_track_mute_changed(self):
        self._update_is_active()

    @listens(u'muted_via_solo')
    def __on_track_muted_via_solo_changed(self):
        self._update_is_active()

    def _update_is_active(self):
        if self.is_enabled():
            self._update_visualisation_view_data({u'IsActive': self._is_active_for_visualisation()})

    @listens(u'color_index')
    def __on_track_or_chain_color_changed(self):
        if self.is_enabled():
            track_color = self._track_color_for_visualisation()
            if track_color is not None:
                self._update_visualisation_view_data({u'TrackColor': track_color})


ENVELOPE_FEATURES_FOR_PARAMETER = {u'Attack': set([u'AttackLine', u'AttackNode', u'DecayLine']),
 u'Decay': set([u'DecayLine', u'DecayNode', u'SustainLine']),
 u'Sustain': set([u'DecayLine',
              u'DecayNode',
              u'SustainLine',
              u'SustainNode',
              u'ReleaseLine']),
 u'Release': set([u'ReleaseLine', u'ReleaseNode']),
 u'Init': set([u'InitNode', u'AttackLine']),
 u'Initial': set([u'InitNode', u'AttackLine']),
 u'Peak': set([u'AttackLine', u'AttackNode', u'DecayLine']),
 u'End': set([u'ReleaseLine', u'ReleaseNode']),
 u'Final': set([u'ReleaseLine', u'ReleaseNode']),
 u'A Slope': set([u'AttackLine']),
 u'D Slope': set([u'DecayLine']),
 u'R Slope': set([u'ReleaseLine']),
 u'Fade In': set([u'FadeInLine', u'FadeInNode', u'SustainLine']),
 u'Fade Out': set([u'FadeOutLine', u'FadeOutNode'])}

def normalize_envelope_parameter_name(parameter_name, envelope_prefixes):
    find_envelope_prefix = re.compile(u'^({}) '.format(u'|'.join(envelope_prefixes)))
    return re.sub(find_envelope_prefix, u'', parameter_name)


def extend_with_envelope_features_for_parameter(features, parameter, envelope_prefixes):
    if liveobj_valid(parameter):
        normalized_name = normalize_envelope_parameter_name(parameter.name, envelope_prefixes)
        try:
            features |= ENVELOPE_FEATURES_FOR_PARAMETER[normalized_name]
        except KeyError:
            pass
