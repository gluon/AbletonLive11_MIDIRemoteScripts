#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v2/control_surface/simpler_decoration.py
from __future__ import absolute_import, print_function, unicode_literals
from builtins import round
from past.utils import old_div
from functools import partial
from math import ceil, floor
import Live
from ..base import clamp, liveobj_valid, listenable_property, listens, sign, EventObject
from ..base.collection import IndexedDict
from .decoration import LiveObjectDecorator
from .internal_parameter import EnumWrappingParameter, RelativeInternalParameter, to_percentage_display, WrappingParameter
BoolWrappingParameter = partial(WrappingParameter, to_property_value=lambda integer, _simpler: bool(integer), from_property_value=lambda boolean, _simpler: int(boolean), value_items=[u'Off', u'On'], display_value_conversion=lambda val: (u'On' if val else u'Off'))

def from_user_range(minv, maxv):
    return lambda v, s: old_div(v - minv, float(maxv - minv))


def to_user_range(minv, maxv):
    return lambda v, s: clamp(v * (maxv - minv) + minv, minv, maxv)


def to_user_range_quantized(minv, maxv):
    user_range_transform = to_user_range(minv, maxv)
    return lambda v, s: int(round(user_range_transform(v, s)))


def from_sample_count(value, sample):
    return old_div(float(value), sample.length)


def to_sample_count(prev_value_getter, value, sample):
    truncation_func = ceil if sign(value - prev_value_getter()) > 0 else floor
    return clamp(int(truncation_func(value * sample.length)), 0, sample.length - 1)


SimplerWarpModes = IndexedDict(((Live.Clip.WarpMode.beats, u'Beats'),
 (Live.Clip.WarpMode.tones, u'Tones'),
 (Live.Clip.WarpMode.texture, u'Texture'),
 (Live.Clip.WarpMode.repitch, u'Re-Pitch'),
 (Live.Clip.WarpMode.complex, u'Complex'),
 (Live.Clip.WarpMode.complex_pro, u'Pro')))

class SimplerDeviceDecorator(EventObject, LiveObjectDecorator):

    def __init__(self, *a, **k):
        super(SimplerDeviceDecorator, self).__init__(*a, **k)
        self._sample_based_parameters = []
        self._additional_parameters = []
        self.setup_parameters()
        self.register_disconnectables(self._decorated_parameters())
        self.__on_playback_mode_changed.subject = self._live_object
        self.__on_sample_changed.subject = self._live_object
        self.__on_slices_changed.subject = self._live_object.sample

    def setup_parameters(self):
        self.start = WrappingParameter(name=u'Start', parent=self, property_host=self._live_object.sample, source_property=u'start_marker', from_property_value=from_sample_count, to_property_value=partial(to_sample_count, lambda : self.start.linear_value))
        self.end = WrappingParameter(name=u'End', parent=self, property_host=self._live_object.sample, source_property=u'end_marker', from_property_value=from_sample_count, to_property_value=partial(to_sample_count, lambda : self.end.linear_value))
        self.sensitivity = WrappingParameter(name=u'Sensitivity', parent=self, property_host=self._live_object.sample, source_property=u'slicing_sensitivity', display_value_conversion=to_percentage_display)
        self.mode = EnumWrappingParameter(name=u'Mode', parent=self, values_host=self, index_property_host=self, values_property=u'available_playback_modes', index_property=u'playback_mode')
        self.slicing_playback_mode_param = EnumWrappingParameter(name=u'Playback', parent=self, values_host=self, index_property_host=self, values_property=u'available_slicing_playback_modes', index_property=u'slicing_playback_mode')
        self.pad_slicing_param = BoolWrappingParameter(name=u'Pad Slicing', parent=self, property_host=self._live_object, source_property=u'pad_slicing')
        self.nudge = RelativeInternalParameter(name=u'Nudge', parent=self)
        self.multi_sample_mode_param = BoolWrappingParameter(name=u'Multi Sample', parent=self, property_host=self._live_object, source_property=u'multi_sample_mode')
        self.warp = BoolWrappingParameter(name=u'Warp', parent=self, property_host=self._live_object.sample, source_property=u'warping')
        self.warp_mode_param = EnumWrappingParameter(name=u'Warp Mode', parent=self, values_host=self, index_property_host=self._live_object.sample, values_property=u'available_warp_modes', index_property=u'warp_mode', to_index_conversion=lambda i: Live.Clip.WarpMode(SimplerWarpModes.key_by_index(i)), from_index_conversion=lambda i: SimplerWarpModes.index_by_key(i))
        self.voices_param = EnumWrappingParameter(name=u'Voices', parent=self, values_host=self, index_property_host=self, values_property=u'available_voice_numbers', index_property=u'voices', to_index_conversion=lambda i: self.available_voice_numbers[i], from_index_conversion=lambda i: self.available_voice_numbers.index(i))
        self.granulation_resolution = EnumWrappingParameter(name=u'Preserve', parent=self, values_host=self, index_property_host=self._live_object.sample, values_property=u'available_resolutions', index_property=u'beats_granulation_resolution')
        self.transient_loop_mode = EnumWrappingParameter(name=u'Loop Mode', parent=self, values_host=self, index_property_host=self._live_object.sample, values_property=u'available_transient_loop_modes', index_property=u'beats_transient_loop_mode')
        self.transient_envelope = WrappingParameter(name=u'Envelope', parent=self, property_host=self._live_object.sample, source_property=u'beats_transient_envelope', from_property_value=from_user_range(0.0, 100.0), to_property_value=to_user_range(0.0, 100.0))
        self.tones_grain_size_param = WrappingParameter(name=u'Grain Size Tones', parent=self, property_host=self._live_object.sample, source_property=u'tones_grain_size', from_property_value=from_user_range(12.0, 100.0), to_property_value=to_user_range(12.0, 100.0))
        self.texture_grain_size_param = WrappingParameter(name=u'Grain Size Texture', parent=self, property_host=self._live_object.sample, source_property=u'texture_grain_size', from_property_value=from_user_range(2.0, 263.0), to_property_value=to_user_range(2.0, 263.0))
        self.flux = WrappingParameter(name=u'Flux', parent=self, property_host=self._live_object.sample, source_property=u'texture_flux', from_property_value=from_user_range(0.0, 100.0), to_property_value=to_user_range(0.0, 100.0))
        self.formants = WrappingParameter(name=u'Formants', parent=self, property_host=self._live_object.sample, source_property=u'complex_pro_formants', from_property_value=from_user_range(0.0, 100.0), to_property_value=to_user_range(0.0, 100.0))
        self.complex_pro_envelope_param = WrappingParameter(name=u'Envelope Complex Pro', parent=self, property_host=self._live_object.sample, source_property=u'complex_pro_envelope', from_property_value=from_user_range(8.0, 256.0), to_property_value=to_user_range(8.0, 256.0))
        self.gain_param = WrappingParameter(name=u'Gain', parent=self, property_host=self._live_object.sample, source_property=u'gain', display_value_conversion=lambda _: (self._live_object.sample.gain_display_string() if liveobj_valid(self._live_object) and liveobj_valid(self._live_object.sample) else u''))
        self.slicing_style_param = EnumWrappingParameter(name=u'Slice by', parent=self, values_host=self, index_property_host=self._live_object.sample, values_property=u'available_slice_styles', index_property=u'slicing_style')
        self.slicing_beat_division_param = EnumWrappingParameter(name=u'Division', parent=self, values_host=self, index_property_host=self._live_object.sample, values_property=u'available_slicing_beat_divisions', index_property=u'slicing_beat_division')
        self.slicing_region_count_param = WrappingParameter(name=u'Regions', parent=self, property_host=self._live_object.sample, source_property=u'slicing_region_count', from_property_value=from_user_range(2, 64), to_property_value=to_user_range_quantized(2, 64))
        self._sample_based_parameters.extend([self.start,
         self.end,
         self.sensitivity,
         self.warp,
         self.transient_envelope,
         self.tones_grain_size_param,
         self.texture_grain_size_param,
         self.flux,
         self.formants,
         self.complex_pro_envelope_param,
         self.gain_param,
         self.slicing_region_count_param,
         self.warp_mode_param,
         self.granulation_resolution,
         self.transient_loop_mode,
         self.slicing_style_param,
         self.slicing_beat_division_param])
        self._additional_parameters.extend([self.mode,
         self.slicing_playback_mode_param,
         self.pad_slicing_param,
         self.nudge,
         self.multi_sample_mode_param,
         self.voices_param])

    def _decorated_parameters(self):
        return tuple(self._sample_based_parameters) + tuple(self._additional_parameters)

    @property
    def parameters(self):
        return tuple(self._live_object.parameters) + self._decorated_parameters()

    @property
    def available_playback_modes(self):
        return [u'Classic', u'One-Shot', u'Slicing']

    @property
    def available_slicing_playback_modes(self):
        return [u'Mono', u'Poly', u'Thru']

    @property
    def available_voice_numbers(self):
        return list(Live.SimplerDevice.get_available_voice_numbers())

    @property
    def available_warp_modes(self):
        return list(SimplerWarpModes.values())

    @property
    def available_resolutions(self):
        return (u'1 Bar', u'1/2', u'1/4', u'1/8', u'1/16', u'1/32', u'Transients')

    @property
    def available_slice_styles(self):
        return (u'Transient', u'Beat', u'Region', u'Manual')

    @property
    def available_slicing_beat_divisions(self):
        return (u'1/16', u'1/16T', u'1/8', u'1/8T', u'1/4', u'1/4T', u'1/2', u'1/2T', u'1 Bar', u'2 Bars', u'4 Bars')

    @property
    def available_transient_loop_modes(self):
        return (u'Off', u'Forward', u'Alternate')

    @listenable_property
    def current_playback_mode(self):
        return self._live_object.playback_mode

    @listenable_property
    def slices(self):
        if liveobj_valid(self._live_object) and liveobj_valid(self._live_object.sample):
            return self._live_object.sample.slices
        return []

    @listens(u'sample')
    def __on_sample_changed(self):
        self._on_sample_changed()

    def _on_sample_changed(self):
        self._reconnect_sample_listeners()

    def _reconnect_sample_listeners(self):
        for param in self._sample_based_parameters:
            param.set_property_host(self._live_object.sample)

        self._reconnect_to_slices()

    def _reconnect_to_slices(self):
        self.__on_slices_changed.subject = self._live_object.sample
        self.notify_slices()

    @listens(u'slices')
    def __on_slices_changed(self):
        self._on_slices_changed()

    def _on_slices_changed(self):
        self.notify_slices()

    @listens(u'playback_mode')
    def __on_playback_mode_changed(self):
        self.notify_current_playback_mode()
