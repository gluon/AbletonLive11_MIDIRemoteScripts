# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Push2/device_decoration.py
# Compiled at: 2022-01-27 16:28:16
# Size of source mod 2**32: 17096 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import object, str
from ableton.v2.base import EventObject, const, inject, listenable_property, listens, liveobj_valid
from ableton.v2.control_surface import EnumWrappingParameter, InternalParameter, LiveObjectDecorator, NotifyingList, get_parameter_by_name
from .device_options import DeviceOnOffOption, DeviceSwitchOption
from .timeline_navigation import Region, SimplerWaveformNavigation

class IndexProvider(EventObject):
    __events__ = ('index', )

    def __init__(self, *a, **k):
        (super(IndexProvider, self).__init__)(*a, **k)
        self._index = 0

    def _get_index(self):
        return self._index

    def _set_index(self, value):
        self._index = value
        self.notify_index()

    index = property(_get_index, _set_index)


class WaveformNavigationParameter(InternalParameter):

    def __init__(self, simpler=None, *a, **k):
        (super(WaveformNavigationParameter, self).__init__)(*a, **k)
        self._simpler = simpler
        self._waveform_navigation = None
        self.post_sample_changed()

    @listenable_property
    def waveform_navigation(self):
        return self._waveform_navigation

    @property
    def visible_region(self):
        if self._waveform_navigation:
            return self._waveform_navigation.visible_region
        return Region(0, 1)

    @visible_region.setter
    def visible_region(self, region):
        if self._waveform_navigation:
            self._waveform_navigation.visible_region = region

    def set_visible_region(self, region):
        if self._waveform_navigation:
            self._waveform_navigation.set_visible_region(region)

    def zoom(self, value):
        if self._waveform_navigation:
            self._waveform_navigation.zoom(value)

    def touch_object(self, parameter):
        if self._waveform_navigation:
            self._waveform_navigation.touch_object(parameter)

    def release_object(self, parameter):
        if self._waveform_navigation:
            self._waveform_navigation.release_object(parameter)

    def change_object(self, parameter):
        if self._waveform_navigation:
            self._waveform_navigation.change_object(parameter)

    def focus_object(self, parameter):
        if self._waveform_navigation:
            self._waveform_navigation.focus_object(parameter)

    def focus_region_of_interest(self, roi_identifier, focused_object):
        if self._waveform_navigation:
            self._waveform_navigation.focus_region_of_interest(roi_identifier, focused_object)

    def reset_focus_and_animation(self):
        if self._waveform_navigation:
            self._waveform_navigation.reset_focus_and_animation()

    def post_sample_changed(self):
        sample = self._simpler.sample
        if self._waveform_navigation is not None:
            self.unregister_disconnectable(self._waveform_navigation)
            self._waveform_navigation.disconnect()
        if liveobj_valid(sample):
            self._waveform_navigation = self.register_disconnectable(SimplerWaveformNavigation(simpler=(self._simpler)))
        else:
            self._waveform_navigation = None
        self.notify_waveform_navigation()


class SlicePoint(object):

    def __init__(self, identifier, time):
        self.__id__ = identifier
        self.time = time

    def __eq__(self, other):
        if isinstance(other, SlicePoint):
            return self.__id__ == other.__id__ and self.time == other.time
        return False

    def __ne__(self, other):
        return not self == other

    __hash__ = None


class SimplerPositions(EventObject):
    __events__ = ('warp_markers', 'before_update_all', 'after_update_all')
    start = listenable_property.managed(0.0)
    end = listenable_property.managed(0.0)
    start_marker = listenable_property.managed(0.0)
    end_marker = listenable_property.managed(0.0)
    active_start = listenable_property.managed(0.0)
    active_end = listenable_property.managed(0.0)
    loop_start = listenable_property.managed(0.0)
    loop_end = listenable_property.managed(0.0)
    loop_fade_in_samples = listenable_property.managed(0.0)
    env_fade_in = listenable_property.managed(0.0)
    env_fade_out = listenable_property.managed(0.0)
    slices = listenable_property.managed([])
    selected_slice = listenable_property.managed(SlicePoint(0, 0.0))
    use_beat_time = listenable_property.managed(False)

    def __init__(self, simpler=None, *a, **k):
        (super(SimplerPositions, self).__init__)(*a, **k)
        self._simpler = simpler
        self._SimplerPositions__on_active_start_changed.subject = simpler.view
        self._SimplerPositions__on_active_end_changed.subject = simpler.view
        self._SimplerPositions__on_loop_start_changed.subject = simpler.view
        self._SimplerPositions__on_loop_end_changed.subject = simpler.view
        self._SimplerPositions__on_loop_fade_changed.subject = simpler.view
        self._SimplerPositions__on_env_fade_in_changed.subject = simpler.view
        self._SimplerPositions__on_env_fade_out_changed.subject = simpler.view
        self._SimplerPositions__on_selected_slice_changed.subject = simpler.view
        self.post_sample_changed()

    def post_sample_changed(self):
        self._SimplerPositions__on_start_marker_changed.subject = self._simpler.sample
        self._SimplerPositions__on_end_marker_changed.subject = self._simpler.sample
        self._SimplerPositions__on_slices_changed.subject = self._simpler.sample
        self._SimplerPositions__on_warping_changed.subject = self._simpler.sample
        self._SimplerPositions__on_warp_markers_changed.subject = self._simpler.sample
        self.update_all()

    def _convert_sample_time(self, sample_time):
        sample = self._simpler.sample
        if liveobj_valid(sample):
            if sample.warping:
                return sample.sample_to_beat_time(sample_time)
        return sample_time

    @listens('start_marker')
    def __on_start_marker_changed(self):
        if liveobj_valid(self._simpler.sample):
            self.start_marker = self._convert_sample_time(self._simpler.sample.start_marker)

    @listens('end_marker')
    def __on_end_marker_changed(self):
        if liveobj_valid(self._simpler.sample):
            self.end_marker = self._convert_sample_time(self._simpler.sample.end_marker)

    @listens('sample_start')
    def __on_active_start_changed(self):
        self.active_start = self._convert_sample_time(self._simpler.view.sample_start)

    @listens('sample_end')
    def __on_active_end_changed(self):
        self.active_end = self._convert_sample_time(self._simpler.view.sample_end)

    @listens('sample_loop_start')
    def __on_loop_start_changed(self):
        self.loop_start = self._convert_sample_time(self._simpler.view.sample_loop_start)

    @listens('sample_loop_end')
    def __on_loop_end_changed(self):
        self.loop_end = self._convert_sample_time(self._simpler.view.sample_loop_end)

    @listens('sample_loop_fade')
    def __on_loop_fade_changed(self):
        self.loop_fade_in_samples = self._simpler.view.sample_loop_fade

    @listens('sample_env_fade_in')
    def __on_env_fade_in_changed(self):
        if liveobj_valid(self._simpler.sample):
            start_marker = self._simpler.sample.start_marker
            fade_in_end = start_marker + self._simpler.view.sample_env_fade_in
            self.env_fade_in = self._convert_sample_time(fade_in_end) - self._convert_sample_time(start_marker)

    @listens('sample_env_fade_out')
    def __on_env_fade_out_changed(self):
        if liveobj_valid(self._simpler.sample):
            end_marker = self._simpler.sample.end_marker
            fade_out_start = end_marker - self._simpler.view.sample_env_fade_out
            self.env_fade_out = self._convert_sample_time(end_marker) - self._convert_sample_time(fade_out_start)

    @listens('slices')
    def __on_slices_changed(self):
        if liveobj_valid(self._simpler.sample):
            self.slices = [SlicePoint(s, self._convert_sample_time(s)) for s in self._simpler.sample.slices]

    @listens('selected_slice')
    def __on_selected_slice_changed(self):
        if liveobj_valid(self._simpler.sample):
            t = self._convert_sample_time(self._simpler.view.selected_slice)
            self.selected_slice = SlicePoint(t, t)

    @listens('warping')
    def __on_warping_changed(self):
        self.update_all()

    @listens('warp_markers')
    def __on_warp_markers_changed(self):
        self.update_all()
        self.notify_warp_markers()

    def update_all(self):
        if liveobj_valid(self._simpler.sample):
            self.notify_before_update_all()
            self.start = self._convert_sample_time(0)
            self.end = self._convert_sample_time(self._simpler.sample.length)
            self._SimplerPositions__on_start_marker_changed()
            self._SimplerPositions__on_end_marker_changed()
            self._SimplerPositions__on_active_start_changed()
            self._SimplerPositions__on_active_end_changed()
            self._SimplerPositions__on_loop_start_changed()
            self._SimplerPositions__on_loop_end_changed()
            self._SimplerPositions__on_loop_fade_changed()
            self._SimplerPositions__on_env_fade_in_changed()
            self._SimplerPositions__on_env_fade_out_changed()
            self._SimplerPositions__on_slices_changed()
            self._SimplerPositions__on_selected_slice_changed()
            self.use_beat_time = self._simpler.sample.warping
            self.notify_after_update_all()


class SamplerDeviceDecorator(EventObject, LiveObjectDecorator):

    def __init__(self, *a, **k):
        (super(SamplerDeviceDecorator, self).__init__)(*a, **k)
        self._SamplerDeviceDecorator__on_parameters_changed.subject = self._live_object
        self.filter_slope_option = DeviceSwitchOption(name='Filter Slope',
          parameter=(get_parameter_by_name(self, 'Filter Slope')))
        self.register_disconnectables(self.options)

    @property
    def options(self):
        return (
         self.filter_slope_option,)

    @listens('parameters')
    def __on_parameters_changed(self):
        self.filter_slope_option.set_parameter(get_parameter_by_name(self, 'Filter Slope'))


class PedalDeviceDecorator(LiveObjectDecorator):

    def __init__(self, *a, **k):
        (super(PedalDeviceDecorator, self).__init__)(*a, **k)
        self.mid_freq_option = DeviceSwitchOption(name='Mid Freq',
          parameter=(get_parameter_by_name(self, 'Mid Freq')))
        self.register_disconnectables(self.options)

    @property
    def options(self):
        return (
         self.mid_freq_option,)


class DrumBussDeviceDecorator(LiveObjectDecorator):

    def __init__(self, *a, **k):
        (super(DrumBussDeviceDecorator, self).__init__)(*a, **k)
        self.compressor_option = DeviceOnOffOption(name='Compressor',
          property_host=(get_parameter_by_name(self, 'Compressor On')))
        self.register_disconnectables(self.options)

    @property
    def options(self):
        return (
         self.compressor_option,)


class ModMatrixParameter(InternalParameter):

    def __init__(self, modulation_value_host=None, modulation_target_index_host=None, modulation_source=None, *a, **k):
        (super(ModMatrixParameter, self).__init__)(*a, **k)
        self._modulation_value_host = modulation_value_host
        self._target_index_host = modulation_target_index_host
        self._source = modulation_source
        self._on_target_index_changed.subject = modulation_target_index_host
        self._on_modulation_matrix_changed.subject = modulation_value_host
        self._modulation_value = 0.0
        self._update_value()

    def _target_index(self):
        return self._target_index_host.index

    def _update_value(self, force_update=False):
        old_value = self._modulation_value
        self._modulation_value = self._modulation_value_host.get_modulation_value(self._target_index(), self._source)
        if old_value != self._modulation_value or (force_update):
            self.notify_value()

    @listens('index')
    def _on_target_index_changed(self):
        self._update_value(force_update=True)

    @listens('modulation_matrix_changed')
    def _on_modulation_matrix_changed(self):
        self._update_value()

    def _get_linear_value(self):
        return self._modulation_value

    def _set_linear_value(self, new_value):
        if new_value != self._modulation_value:
            self._modulation_value_host.set_modulation_value(self._target_index(), self._source, new_value)

    linear_value = property(_get_linear_value, _set_linear_value)

    @property
    def min(self):
        return -1.0

    @property
    def max(self):
        return 1.0

    @property
    def display_value(self):
        percentage = 100.0 * self._modulation_value
        precision = 1 if abs(percentage) < 10.0 else 0
        format_str = '%.' + str(precision) + 'f'
        return str(format_str % percentage)

    @property
    def default_value(self):
        return 0


class UtilityDeviceDecorator(LiveObjectDecorator, EventObject):

    def __init__(self, *a, **k):
        (super(UtilityDeviceDecorator, self).__init__)(*a, **k)
        self._UtilityDeviceDecorator__on_parameters_changed.subject = self._live_object
        self.mono_option = DeviceOnOffOption(name='Mono',
          property_host=(get_parameter_by_name(self, 'Mono')))
        self.bass_mono_option = DeviceOnOffOption(name='Bass Mono',
          property_host=(get_parameter_by_name(self, 'Bass Mono')))
        self.dc_filter_option = DeviceOnOffOption(name='DC Filter',
          property_host=(get_parameter_by_name(self, 'DC Filter')))
        self.register_disconnectables(self.options)

    @property
    def options(self):
        return (
         self.mono_option, self.bass_mono_option, self.dc_filter_option)

    @listens('parameters')
    def __on_parameters_changed(self):
        self.mono_option.set_property_host(get_parameter_by_name(self, 'Mono'))
        self.bass_mono_option.set_property_host(get_parameter_by_name(self, 'Bass Mono'))


class SimplerDecoratedPropertiesCopier(object):
    ADDITIONAL_PROPERTIES = [
     'playhead_real_time_channel_id',
     'waveform_real_time_channel_id']

    def __init__(self, decorated_object=None, factory=None, *a, **k):
        (super(SimplerDecoratedPropertiesCopier, self).__init__)(*a, **k)
        self._decorated_object = decorated_object
        self._factory = factory
        self._copied_additional_properties = {}
        self._nested_properties = {}
        self.copy_properties({self.ADDITIONAL_PROPERTIES[0]: None, self.ADDITIONAL_PROPERTIES[1]: None})

    def copy_properties(self, properties):
        for prop, getter in properties.items():
            if getter:
                self._nested_properties[prop] = getter(self._decorated_object)
            else:
                self._copied_additional_properties[prop] = getattr(self._decorated_object, prop)

    def apply_properties(self, new_object, song):
        decorated = None
        with inject(song=(const(song))).everywhere():
            decorated = self._factory.decorate(new_object,
              additional_properties=(self._copied_additional_properties),
              song=song)
        self._apply_nested_properties(decorated)
        return decorated

    def _apply_nested_properties(self, decorated_object):
        if decorated_object.zoom.waveform_navigation is not None:
            if self._decorated_object.zoom.waveform_navigation is not None:
                decorated_object.zoom.waveform_navigation.copy_state(self._decorated_object.zoom.waveform_navigation)