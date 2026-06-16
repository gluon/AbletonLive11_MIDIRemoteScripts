# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\timeline_navigation.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 52850 bytes
from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import filter, map, object, range
from past.utils import old_div
import logging, math
from collections import OrderedDict, namedtuple
from functools import partial
import Live
from ableton.v2.base import EventObject, clamp, const, depends, find_if, index_if, isclose, lazy_attribute, listenable_property, listens, listens_group, liveobj_valid, nop, old_hasattr, task
from ableton.v2.control_surface.control import EncoderControl
logger = logging.getLogger(__name__)
FocusMarker = namedtuple('FocusMarker', ['name', 'position'])

def ease_out(t, degree):
    return 1 - (1 - t) ** degree


def inverse_ease_out(t, degree):
    if t < 1.0:
        return 1.0 - (1.0 - t) ** (1.0 / degree)
    return 1.0


def interpolate(from_value, to_value, t, ease_out_degree):
    t = ease_out(t, ease_out_degree)
    return (1.0 - t) * from_value + t * to_value


def interpolate_inverse(from_value, to_value, current_value, ease_out_degree):
    t = 0.0 if from_value - to_value == 0 else -float(current_value - from_value) / float(from_value - to_value)
    return inverse_ease_out(t, ease_out_degree)


def calc_easing_degree_for_proportion(proportion):
    return -math.log10(proportion) + 1


def interpolate_region(from_region, to_region, t, ease_out_degree):
    return Region(interpolate(from_region.start, to_region.start, t, ease_out_degree), interpolate(from_region.end, to_region.end, t, ease_out_degree))


def inverse_interpolate_region(from_region, to_region, current_region, ease_out_degree, prefer_end):
    if prefer_end:
        index = 0 if from_region.end == to_region.end else 1
    else:
        index = 1 if from_region.start == to_region.start else 0
    return interpolate_inverse(from_region[index], to_region[index], current_region[index], ease_out_degree)


class Region(namedtuple('Region', ['start', 'end'])):

    def __eq__(self, region):
        return region is not None and isclose(region.start, self.start) and isclose(region.end, self.end)

    def __ne__(self, region):
        return not region == self

    def __hash__(self):
        return hash((self.start, self.end))

    @property
    def length(self):
        return self.end - self.start

    def inside(self, outer):
        if not (isclose(self.start, outer.start) or self.start > outer.start and isclose(self.end, outer.end)):
            return self.end < outer.end and outer != self

    def clamp_position(self, position):
        return clamp(position, self.start, self.end)

    def clamp_to_region(self, region):
        return Region(region.clamp_position(self.start), region.clamp_position(self.end))


class RegionOfInterest(object):

    def __init__(self, start_identifier=None, end_identifier=None, getter=None, add_margin=nop, *a, **k):
        (super(RegionOfInterest, self).__init__)(*a, **k)
        self.start_identifier = start_identifier
        self.end_identifier = end_identifier
        self.add_margin = add_margin
        self._getter = getter

    def bound_by(self, object_identifier):
        return object_identifier in (self.start_identifier, self.end_identifier)

    @property
    def region(self):
        return Region(*self._getter())

    @property
    def region_with_margin(self):
        return self.add_margin(Region(*self._getter()))


class ObjectDescription(object):

    def __init__(self, regions, focus_name_or_getter, *a, **k):
        (super(ObjectDescription, self).__init__)(*a, **k)
        self._regions = ('timeline', ) + regions + ('focused_object', )
        self._focus_name_or_getter = focus_name_or_getter

    @property
    def regions(self):
        return self._regions

    @property
    def focus_name(self):
        if callable(self._focus_name_or_getter):
            return self._focus_name_or_getter()
        return self._focus_name_or_getter


class MarginType(object):
    NONE, START, END = list(range(3))


class TimelineNavigation(EventObject):
    visible_region = listenable_property.managed(Region(0, 1))
    animate_visible_region = listenable_property.managed(False)
    focus_marker = listenable_property.managed(FocusMarker('', 0.0))
    show_focus = listenable_property.managed(False)
    ZOOM_SENSITIVITY = 1.5
    TIMELINE_WIDTH_IN_PX = 933
    MARGIN_IN_PX = 121
    RELATIVE_FOCUS_MARGIN = float(MARGIN_IN_PX) / TIMELINE_WIDTH_IN_PX
    UNSNAPPING_THRESHOLD = 0.6
    CHANGE_OBJECT_TIME = 0.1

    @depends(external_regions_of_interest_creator=(const(None)),
      external_focusable_object_descriptions=(const(None)))
    def __init__(self, external_regions_of_interest_creator=None, external_focusable_object_descriptions=None, *a, **k):
        (super(TimelineNavigation, self).__init__)(*a, **k)
        self._timeline_region = Region(0, 1)
        self.timeline_roi = self.make_region_of_interest(getter=(lambda: self._timeline_region
),
          with_margin=False)
        self.focused_object_roi = self.make_region_of_interest(getter=(self._make_region_for_focused_object),
          with_margin=False)
        self._external_regions_of_interest = external_regions_of_interest_creator(self.make_region_of_interest) if callable(external_regions_of_interest_creator) else {}
        self._external_focusable_object_descriptions = external_focusable_object_descriptions if external_focusable_object_descriptions else {}
        self._focused_identifier = None
        self._touched_identifiers = set()
        self._changed_identifiers = set()
        self._has_tasks = False
        self._target_roi = self.timeline_roi
        self._source_roi = self.timeline_roi
        self._request_select_region = False
        self._unsnapping_value = 0
        self._locked_roi = None
        self._last_action = None

    def disconnect(self):
        super(TimelineNavigation, self).disconnect()
        if self._has_tasks:
            self._tasks.kill()
            self._tasks.clear()

    def get_object_identifier(self, obj):
        raise NotImplementedError

    def get_zoom_object(self):
        raise NotImplementedError

    def get_min_visible_length(self):
        raise NotImplementedError

    @listenable_property
    def timeline_region(self):
        return self._timeline_region

    @timeline_region.setter
    def timeline_region(self, region):
        if region != self._timeline_region:
            self._timeline_region = region
            self._request_select_region = True
            self.set_visible_region(self._timeline_region)
            self.notify_timeline_region()

    def make_region_of_interest(self, start_identifier=None, end_identifier=None, getter=None, with_margin=True):
        return RegionOfInterest(start_identifier,
          end_identifier,
          getter,
          add_margin=(self._add_margin_to_region if with_margin else nop))

    @lazy_attribute
    def regions_of_interest(self):
        rois = {'timeline':self.timeline_roi, 
         'focused_object':self.focused_object_roi}
        rois.update(self._external_regions_of_interest)
        rois.update(self.additional_regions_of_interest)
        return rois

    @lazy_attribute
    def additional_regions_of_interest(self):
        return {}

    def get_name_for_roi(self, roi):
        item = find_if(lambda i: i[1] == roi
, iter(self.regions_of_interest.items()))
        if item is not None:
            return item[0]

    @lazy_attribute
    def focusable_object_descriptions(self):
        focusable_object_descriptions = {}
        focusable_object_descriptions.update(self._external_focusable_object_descriptions)
        focusable_object_descriptions.update(self.additional_focusable_object_descriptions)
        return focusable_object_descriptions

    @lazy_attribute
    def additional_focusable_object_descriptions(self):
        return {}

    def get_object_description(self, identifier):
        return self.focusable_object_descriptions.get(identifier, None)

    @property
    def visible_proportion(self):
        return self.visible_region.length / float(self._timeline_region.length)

    def set_visible_region(self, region, source_action=None, force_animate=False):
        self.animate_visible_region = force_animate or source_action != self._last_action
        self.visible_region = region.clamp_to_region(self._timeline_region)
        self._last_action = source_action

    def set_visible_length(self, length):
        start = self.visible_region.start
        end = min(start + length, self.timeline_region.end)
        start = end - length
        self.set_visible_region(Region(start, end))

    def zoom(self, value):
        animate = self._request_select_region
        if self._request_select_region or self._process_unsnapping(value):
            self._select_region(value > 0)
        source = self._source_roi.region_with_margin
        target = self._target_roi.region_with_margin
        easing_degree = calc_easing_degree_for_proportion(float(target.length) / float(source.length))
        focused_region, focus_marker, margin_type = self._get_zoom_info_for_focused_object()
        t = inverse_interpolate_region(source,
          target,
          (self.visible_region),
          easing_degree,
          prefer_end=(margin_type == MarginType.START))
        t = clamp(t + value * self.ZOOM_SENSITIVITY, 0.0, 1.0)
        region = interpolate_region(source, target, t, easing_degree)
        region = self._add_margin_to_zoomed_region(region, focused_region, margin_type)
        self.set_visible_region(region, force_animate=animate, source_action='zoom')
        self.focus_marker = focus_marker
        self.show_focus = True
        self.try_hide_focus_delayed()
        self._try_lock_region()

    def _get_zoom_info_for_focused_object(self):
        identifier = self._focused_identifier
        roi = self._get_roi_for_object_identifier(identifier)
        margin_type = MarginType.NONE
        region = None
        focus_marker = None
        if roi is not None:
            margin = self.timeline_region.length * self.RELATIVE_FOCUS_MARGIN
            region = roi.region
            is_start = roi.start_identifier == identifier
            if is_start and region.start < margin:
                margin_type = MarginType.START
            else:
                if not is_start:
                    if region.end > self.timeline_region.end - margin:
                        margin_type = MarginType.END
            obj_description = self.focusable_object_descriptions.get(identifier, None)
            if obj_description is not None:
                focus_marker = FocusMarker(obj_description.focus_name, region.end if roi.end_identifier == identifier else region.start)
        return (
         region, focus_marker, margin_type)

    def _add_margin_to_zoomed_region(self, zoom_region, focused_region, margin_type):
        if focused_region is not None:
            if margin_type != MarginType.NONE:
                position = focused_region.start if margin_type == MarginType.START else focused_region.end
                if zoom_region.start<= position <= zoom_region.end:
                    if margin_type == MarginType.START:
                        zoom_region = self._add_margin_to_zoomed_region_start(zoom_region, position)
                    else:
                        zoom_region = self._add_margin_to_zoomed_region_end(zoom_region, position)
                else:
                    logger.warning("Focused object not visible. Couldn't add margin to zoomed region. %d not in %r" % (
                     position, zoom_region))
        return zoom_region

    def _add_margin_to_zoomed_region_start(self, region, focused_position):
        p = focused_position - self.timeline_region.start
        samples_per_pixel = old_div(p, self.MARGIN_IN_PX)
        length = self.TIMELINE_WIDTH_IN_PX * samples_per_pixel
        if self.timeline_region.start + length < region.end:
            region = Region(self.timeline_region.start, region.end)
        else:
            p = region.end - focused_position
            samples_per_pixel = old_div(p, self.TIMELINE_WIDTH_IN_PX - self.MARGIN_IN_PX)
            length = self.TIMELINE_WIDTH_IN_PX * samples_per_pixel
            start = region.end - length
            if start < region.start:
                region = Region(start, region.end)
        return region

    def _add_margin_to_zoomed_region_end(self, region, focused_position):
        p = self.timeline_region.end - focused_position
        samples_per_pixel = old_div(p, self.MARGIN_IN_PX)
        length = self.TIMELINE_WIDTH_IN_PX * samples_per_pixel
        if self.timeline_region.end - length > region.start:
            region = Region(region.start, self.timeline_region.end)
        else:
            p = focused_position - region.start
            samples_per_pixel = old_div(p, self.TIMELINE_WIDTH_IN_PX - self.MARGIN_IN_PX)
            length = self.TIMELINE_WIDTH_IN_PX * samples_per_pixel
            end = region.start + length
            if end > region.end:
                region = Region(region.start, end)
        return region

    def _process_unsnapping(self, value):
        if self.is_snapped:
            self._unsnapping_value += value
            return abs(self._unsnapping_value) >= self.UNSNAPPING_THRESHOLD
        return False

    def _try_lock_region(self):
        if self.visible_region == self._timeline_region:
            self._locked_roi = None
        else:
            if self.visible_region == self._target_roi.region_with_margin:
                self._locked_roi = self._target_roi
            else:
                if self.visible_region == self._source_roi.region_with_margin:
                    self._locked_roi = self._source_roi
                else:
                    self._locked_roi = None

    @property
    def is_snapped(self):
        return self.visible_region == self._target_roi.region_with_margin or self.visible_region == self._source_roi.region_with_margin

    def focus_object(self, obj):
        if obj != self.get_zoom_object():
            identifier = self.get_object_identifier(obj)
            zoom_identifier = self.get_object_identifier(self.get_zoom_object())
            touched_identifiers = self._touched_identifiers - set([zoom_identifier])
            objects_to_show = self._changed_identifiers & touched_identifiers
            if identifier in self.focusable_object_descriptions:
                if len(objects_to_show) > 1:
                    logger.debug('Focus all objects %r' % objects_to_show)
                    self._focused_identifier = identifier
                    self._show_all_objects(objects_to_show)
                else:
                    logger.debug('Focus object %r' % identifier)
                    animate = len(touched_identifiers) <= 1 and self.object_changed(self._focused_identifier, identifier)
                    self._focused_identifier = identifier
                    self._focus_object_by_identifier(identifier, animate=animate)
                return True
        return False

    def object_changed(self, identifier1, identifier2):
        return identifier1 != identifier2

    def _get_roi_for_object_identifier(self, identifier):
        return find_if(lambda roi: roi.bound_by(identifier)
, list(self.regions_of_interest.values()))

    def _get_position_for_identifier(self, identifier):
        roi = self._get_roi_for_object_identifier(identifier)
        if roi is not None:
            if roi.start_identifier == identifier:
                return roi.region.start
            return roi.region.end

    def _zoom_out_or_move_region(self, source_region, target_region):
        new_region = None
        if source_region.inside(target_region):
            new_region = target_region
        else:
            if target_region.start < source_region.start:
                new_region = Region(target_region.start, max(target_region.start + source_region.length, target_region.end))
            else:
                if target_region.end > source_region.end:
                    new_region = Region(min(target_region.end - source_region.length, target_region.start), target_region.end)
        return new_region

    def _show_all_objects(self, identifiers):
        start = self.timeline_region.end
        end = self.timeline_region.start
        positions = list(map(self._get_position_for_identifier, identifiers))
        for position in filter(None, positions):
            start = min(start, position)
            end = max(end, position)

        margin = self.visible_region.length * self.RELATIVE_FOCUS_MARGIN
        visible_region_without_margin = Region(self.visible_region.start + margin, self.visible_region.end - margin)
        object_region = Region(start, end)
        new_region = self._zoom_out_or_move_region(visible_region_without_margin, object_region)
        if new_region is not None:
            self.set_visible_region((self._add_margin_to_region(new_region)),
              source_action=('show_objects %r' % identifiers))
            self._request_select_region = True
            self._locked_roi = None
        self.focus_marker = FocusMarker('', 0.0)

    def _focus_object_by_identifier(self, identifier, animate=False):
        roi = self._get_roi_for_object_identifier(identifier)
        region = roi.region
        if self._locked_roi is not None and self._locked_roi.bound_by(identifier):
            if region.start < self.timeline_region.start:
                start = self.timeline_region.start
                new_visible_region = Region(start, start + self.visible_region.length)
            else:
                if region.end > self.timeline_region.end:
                    end = self.timeline_region.end
                    new_visible_region = Region(end - self.visible_region.length, end)
                else:
                    new_visible_region = self._add_margin_to_region(region)
            self.set_visible_region(new_visible_region, force_animate=animate)
        else:
            visible_length = self.visible_region.length
            visible_margin = visible_length * self.RELATIVE_FOCUS_MARGIN
            timeline_start, timeline_end = self._timeline_region
            if roi.end_identifier == identifier:
                start = min(region.start - visible_margin, self.visible_region.start)
                right = max(region.end + visible_margin, start + visible_length)
                left = right - visible_length
            else:
                end = max(region.end + visible_margin, self.visible_region.end)
                left = min(region.start - visible_margin, end - visible_length)
                right = left + visible_length
            self.set_visible_region((Region(clamp(left, timeline_start, timeline_end - visible_length), clamp(right, timeline_start + visible_length, timeline_end))),
              force_animate=animate)
            self._request_select_region = True
        self.focus_marker = FocusMarker(self.focusable_object_descriptions[identifier].focus_name, region.end if roi.end_identifier == identifier else region.start)

    def touch_object(self, obj):
        is_zoom_object = obj == self.get_zoom_object()
        if is_zoom_object:
            if self.is_snapped:
                self._request_select_region = True
        self._touched_identifiers.add(self.get_object_identifier(obj))
        if self.focus_object(obj) or is_zoom_object:
            self.show_focus = True

    def release_object(self, obj):
        identifier = self.get_object_identifier(obj)
        self._remove_changed_object(identifier)
        if identifier in self._touched_identifiers:
            self._touched_identifiers.remove(identifier)
            self.try_hide_focus()

    def _remove_changed_object(self, identifier):
        if identifier in self._changed_identifiers:
            self._changed_identifiers.remove(identifier)

    def _remove_changed_object_delayed(self, identifier):
        tasks = self._tasks
        if tasks is not None:
            tasks.add(task.sequence(task.wait(self.CHANGE_OBJECT_TIME), task.run(partial(self._remove_changed_object, identifier))))

    def change_object(self, obj):
        identifier = self.get_object_identifier(obj)
        self._changed_identifiers.add(identifier)
        self._remove_changed_object_delayed(identifier)
        if self.focus_object(obj) or obj == self.get_zoom_object():
            self.show_focus = True
            self.try_hide_focus_delayed()

    def focus_region_of_interest(self, roi_identifier, focused_object):
        roi = self.regions_of_interest[roi_identifier]
        visible_region = roi.region_with_margin
        self.set_visible_region(visible_region)
        self.focus_object(focused_object)
        if visible_region != self._timeline_region:
            self._locked_roi = roi

    def try_hide_focus(self):
        if self._should_hide_focus():
            self.show_focus = False

    def try_hide_focus_delayed(self):
        if self._hide_focus_task:
            if self._should_hide_focus():
                self._hide_focus_task.restart()

    def _should_hide_focus(self):
        zoom_identifier = self.get_object_identifier(self.get_zoom_object())
        return zoom_identifier not in self._touched_identifiers and self._focused_identifier not in self._touched_identifiers

    def reset_focus_and_animation(self):
        self.show_focus = False
        self.animate_visible_region = False
        self._touched_identifiers = set()
        self._changed_identifiers = set()

    def copy_state(self, navigation):
        if self._timeline_region == navigation.timeline_region:
            self.set_visible_region(navigation.visible_region)
            self._focused_identifier = navigation._focused_identifier
            source_roi_name = navigation.get_name_for_roi(navigation._source_roi)
            target_roi_name = navigation.get_name_for_roi(navigation._target_roi)
            locked_roi_name = navigation.get_name_for_roi(navigation._locked_roi)
            self._source_roi = self.regions_of_interest.get(source_roi_name, None)
            self._target_roi = self.regions_of_interest.get(target_roi_name, None)
            self._locked_roi = self.regions_of_interest.get(locked_roi_name, None)

    @lazy_attribute
    @depends(parent_task_group=(const(None)))
    def _tasks(self, parent_task_group=None):
        if parent_task_group is not None:
            tasks = parent_task_group.add(task.TaskGroup())
            self._has_tasks = True
            return tasks

    @lazy_attribute
    def _hide_focus_task(self):
        tasks = self._tasks
        if tasks is not None:
            return tasks.add(task.sequence(task.wait(EncoderControl.TOUCH_TIME), task.run(self.try_hide_focus)))

    def _add_margin_to_region(self, region):
        start, end = region
        margin = self.RELATIVE_FOCUS_MARGIN
        start1 = old_div(margin * start + end * margin - start, 2 * margin - 1)
        start1 = self._timeline_region.clamp_position(start1)
        end1 = old_div(end - margin * start1, 1 - margin)
        end2 = old_div(margin * start + end * margin - end, 2 * margin - 1)
        end2 = self._timeline_region.clamp_position(end2)
        start2 = old_div(start - margin * end2, 1 - margin)
        return Region(max(start1, start2), min(end1, end2))

    def _make_region_from_position_identifier(self, identifier):
        roi = self._get_roi_for_object_identifier(identifier)
        align_right = roi.end_identifier == identifier
        region = roi.region
        position = region.end if align_right else region.start
        length = self.get_min_visible_length()
        margin = self.RELATIVE_FOCUS_MARGIN * length
        if align_right:
            right = self._timeline_region.clamp_position(position + margin)
            left = self._timeline_region.clamp_position(right - length)
        else:
            left = self._timeline_region.clamp_position(position - margin)
            right = self._timeline_region.clamp_position(left + length)
        return Region(left, right)

    def _make_region_for_focused_object(self):
        if self._focused_identifier is not None:
            return self._make_region_from_position_identifier(self._focused_identifier)
        return Region(0, 0)

    def _get_roi_for_focused_identifier(self):
        if self._focused_identifier is not None:
            return list(map(self.regions_of_interest.get, self.get_object_description(self._focused_identifier).regions))
        return []

    def _get_unique_regions_of_interest(self):
        rois = OrderedDict()
        for roi in self._get_roi_for_focused_identifier():
            rois[roi.region_with_margin] = roi

        items = sorted((list(rois.items())), key=(lambda r__: r__[0].length
), reverse=True)
        return [item[1] for item in items]

    def _select_region_around_visible_region(self):
        regions_of_interest = self._get_unique_regions_of_interest()
        source_roi = find_if(lambda roi: self.visible_region.inside(roi.region_with_margin)
, reversed(regions_of_interest[:-1]))
        if source_roi is not None:
            self._set_source_and_target_roi(source_roi, regions_of_interest[regions_of_interest.index(source_roi) + 1])

    def _select_reached_region(self, zoom_in):
        rois = self._get_unique_regions_of_interest()
        i = index_if(lambda roi: self.visible_region == roi.region_with_margin
, rois)
        if i != len(rois):
            if zoom_in:
                if i < len(rois) - 1:
                    self._set_source_and_target_roi(rois[i], rois[i + 1])
            else:
                if i > 0:
                    self._set_source_and_target_roi(rois[i - 1], rois[i])
            return True
        return False

    def _select_region(self, zoom_in):
        if not self._select_reached_region(zoom_in):
            self._select_region_around_visible_region()
        self._request_select_region = False
        self._unsnapping_value = 0

    def _set_source_and_target_roi(self, source_roi, target_roi):
        self._source_roi = source_roi
        self._target_roi = target_roi
        if logger.isEnabledFor(logging.DEBUG):
            self._report_current_source_and_target_roi()

    def _report_current_source_and_target_roi(self):
        source_roi_name = ''
        target_roi_name = ''
        for name, roi in self.regions_of_interest.items():
            if roi == self._source_roi:
                source_roi_name = name
            if roi == self._target_roi:
                target_roi_name = name

        logger.debug('Zooming between roi "%s" and "%s"' % (source_roi_name, target_roi_name))


class WaveformNavigation(EventObject):
    visible_region_in_samples = listenable_property.managed(Region(0, 1))
    MIN_VISIBLE_SAMPLES = 49

    def get_region_in_samples(self, region):
        return region


class SimplerWaveformNavigation(TimelineNavigation, WaveformNavigation):
    selected_slice_focus = 'selected_slice'

    def __init__(self, simpler=None, *a, **k):
        (super(SimplerWaveformNavigation, self).__init__)(*a, **k)
        self._simpler = simpler
        self._enable_focus_objects = True
        focusable_parameters = [self._simpler.get_parameter_by_name(n) for n in self.focusable_object_descriptions]
        self._SimplerWaveformNavigation__on_playback_mode_changed.subject = simpler
        self._SimplerWaveformNavigation__on_playing_position_enabled_changed.subject = simpler
        self._SimplerWaveformNavigation__on_selected_slice_changed.subject = simpler.positions
        self._SimplerWaveformNavigation__on_use_beat_time_changed.subject = simpler.positions
        self._SimplerWaveformNavigation__on_warp_markers_changed.subject = simpler.positions
        self._SimplerWaveformNavigation__on_before_update_all.subject = simpler.positions
        self._SimplerWaveformNavigation__on_after_update_all.subject = simpler.positions
        self._SimplerWaveformNavigation__on_parameter_value_changed.replace_subjects(focusable_parameters)
        self._update_waveform_region()

    def set_visible_region(self, region, source_action=None, force_animate=False):
        super(SimplerWaveformNavigation, self).set_visible_region(region, source_action, force_animate)
        self.visible_region_in_samples = self.get_region_in_samples(self.visible_region)

    def get_region_in_samples(self, region):
        sample = self._simpler.sample
        if liveobj_valid(sample):
            if sample.warping:
                return Region(sample.beat_to_sample_time(region.start), sample.beat_to_sample_time(region.end))
        return region

    def get_min_visible_length(self):
        sample = self._simpler.sample
        if sample.warping:
            return sample.sample_to_beat_time(self.MIN_VISIBLE_SAMPLES) - sample.sample_to_beat_time(0)
        return self.MIN_VISIBLE_SAMPLES

    @lazy_attribute
    def additional_regions_of_interest(self):
        return {'start_end_marker':self.make_region_of_interest(start_identifier='Start',
           end_identifier='End',
           getter=lambda: (
          self._simpler.positions.start_marker,
          self._simpler.positions.end_marker)
), 
         'active_sample':self.make_region_of_interest(start_identifier='S Start',
           end_identifier='S Length',
           getter=lambda: (
          self._simpler.positions.active_start,
          self._simpler.positions.active_end)
), 
         'loop':self.make_region_of_interest(start_identifier='S Loop Length',
           end_identifier='S Length',
           getter=lambda: (
          self._simpler.positions.loop_start,
          self._simpler.positions.loop_end)
), 
         'selected_slice':self.make_region_of_interest(start_identifier=self.selected_slice_focus,
           end_identifier=None,
           getter=lambda: (
          self._simpler.positions.selected_slice.time,
          self.get_next_slice_position())
)}

    @lazy_attribute
    def additional_focusable_object_descriptions(self):
        return {'Start': ObjectDescription(('start_end_marker', ), 'start_marker'), 
         'End': ObjectDescription(('start_end_marker', ), 'end_marker'), 
         'S Start': ObjectDescription(('start_end_marker', 'active_sample'), 'position'), 
         
         'S Length': ObjectDescription(('start_end_marker', 'active_sample'), 'position'), 
         
         'S Loop Length': ObjectDescription(('start_end_marker', 'active_sample', 'loop'), 'position'), 
         
         self.selected_slice_focus: ObjectDescription(('start_end_marker', 'selected_slice'), '')}

    def get_object_identifier(self, obj):
        if old_hasattr(obj, 'name'):
            return obj.name
        return obj

    def get_zoom_object(self):
        return self._simpler.zoom

    def get_next_slice_position(self):
        positions = self._simpler.positions
        slice_index = self._get_selected_slice_index()
        min_visible_length = self.get_min_visible_length()
        if slice_index == -1:
            next_pos = positions.selected_slice.time + min_visible_length
        else:
            if slice_index + 1 < len(positions.slices):
                next_pos = max(positions.slices[slice_index + 1].time, positions.selected_slice.time + min_visible_length)
            else:
                next_pos = max(positions.end_marker, positions.selected_slice.time + min_visible_length)
        return next_pos

    def object_changed(self, identifier1, identifier2):
        if self.selected_slice_focus in (identifier1, identifier2):
            if self._get_selected_slice_index() == 0:
                if 'Start' in (identifier1, identifier2):
                    return False
        return identifier1 != identifier2

    def focus_object(self, obj):
        if self._enable_focus_objects:
            return super(SimplerWaveformNavigation, self).focus_object(obj)
        return False

    @listens('playback_mode')
    def __on_playback_mode_changed(self):
        start_end_region = self.regions_of_interest['start_end_marker'].region
        if start_end_region.inside(self.visible_region):
            self.focus_object(self._simpler.get_parameter_by_name('Start'))
        else:
            self._focus_start_end_roi()

    @listens_group('value')
    def __on_parameter_value_changed(self, parameter):
        self._simpler.positions.update_all()
        self.change_object(parameter)

    @listens('selected_slice')
    def __on_selected_slice_changed(self, _):
        self._focus_selected_slice()

    @listens('playing_position_enabled')
    def __on_playing_position_enabled_changed(self):
        slicing = self._simpler.playback_mode == Live.SimplerDevice.PlaybackMode.slicing
        if slicing:
            if self._simpler.playing_position_enabled:
                self._focus_selected_slice()

    @listens('use_beat_time')
    def __on_use_beat_time_changed(self, use_beat_time):
        self._update_waveform_region_and_preserve_visible_region()

    @listens('warp_markers')
    def __on_warp_markers_changed(self):
        self._update_waveform_region_and_preserve_visible_region()

    @listens('before_update_all')
    def __on_before_update_all(self):
        self._enable_focus_objects = False

    @listens('after_update_all')
    def __on_after_update_all(self):
        self._enable_focus_objects = True

    def _update_waveform_region_and_preserve_visible_region(self):
        sample = self._simpler.sample
        region = self.visible_region_in_samples
        self._update_waveform_region()
        if sample.warping:
            region = Region(sample.sample_to_beat_time(region.start), sample.sample_to_beat_time(region.end))
        self.set_visible_region(region)

    def _update_waveform_region(self):
        self.timeline_region = Region(self._simpler.positions.start, self._simpler.positions.end)

    def _focus_selected_slice(self):
        slice_index = self._get_selected_slice_index()
        if slice_index != -1:
            self.focus_object(self.selected_slice_focus)

    def _focus_start_end_roi(self):
        self.focus_region_of_interest('start_end_marker', self._simpler.get_parameter_by_name('Start'))

    def _get_selected_slice_index(self):
        selected_slice_index = -1
        try:
            if liveobj_valid(self._simpler.sample):
                selected_slice_index = self._simpler.sample.slices.index(self._simpler.view.selected_slice)
        except ValueError:
            pass

        return selected_slice_index


class ClipTimelineNavigation(TimelineNavigation):
    MIN_VISIBLE_BEATS = 1
    zoom_focus = 'zoom'
    start_marker_focus = 'start_marker'
    loop_start_focus = 'loop_start'
    loop_end_focus = 'loop_end'

    def __init__(self, clip=None, *a, **k):
        (super(ClipTimelineNavigation, self).__init__)(*a, **k)
        self._clip = clip
        self._process_object_changes = True
        self._connect_positions_property('loop_start', self.loop_start_focus)
        self._connect_positions_property('loop_length', self.loop_end_focus)
        self._connect_positions_property('start_marker', self.start_marker_focus)
        self._ClipTimelineNavigation__on_is_recording_changed.subject = clip.positions
        self._ClipTimelineNavigation__on_before_update_all.subject = clip.positions
        self._ClipTimelineNavigation__on_after_update_all.subject = clip.positions
        self._update_timeline_region()

    def _connect_positions_property(self, property_name, focus_object):
        self.register_slot(self._clip.positions, lambda _: self.change_object(focus_object)
, property_name)

    @lazy_attribute
    def additional_regions_of_interest(self):
        return {'start_end_marker':self.make_region_of_interest(start_identifier=self.start_marker_focus,
           end_identifier=self.loop_end_focus,
           getter=lambda: (
          self._clip.positions.start_marker,
          self._clip.positions.loop_end)
), 
         'loop':self.make_region_of_interest(start_identifier=self.loop_start_focus,
           end_identifier=self.loop_end_focus,
           getter=lambda: (
          self._clip.positions.loop_start,
          self._clip.positions.loop_end)
), 
         'start_end':self.make_region_of_interest(getter=self._get_start_end_region)}

    @lazy_attribute
    def additional_focusable_object_descriptions(self):
        return {self.start_marker_focus: ObjectDescription(('start_end', 'start_end_marker'), 'start_marker'), 
         
         self.loop_start_focus: ObjectDescription(('start_end', 'loop'), lambda: 'position' if self._clip.looping else 'start_marker'
), 
         
         self.loop_end_focus: ObjectDescription(('start_end', ), 'end_marker')}

    def get_object_identifier(self, obj):
        return obj

    def get_zoom_object(self):
        return self.zoom_focus

    def object_changed(self, identfier1, identifier2):
        if self.start_marker_focus in (identfier1, identifier2):
            if self.loop_start_focus in (identfier1, identifier2):
                if self._clip.positions.start_marker == self._clip.positions.loop_start:
                    return False
        return identfier1 != identifier2

    def change_object(self, obj):
        if self._process_object_changes:
            self._clip.positions.update_all()
            visible_length = self.visible_region.length
            self._update_timeline_region()
            self.set_visible_length(visible_length)
            super(ClipTimelineNavigation, self).change_object(obj)

    def get_region_in_samples(self, region):
        if self._clip.warping:
            return Region(self._clip.beat_to_sample_time(region.start), self._clip.beat_to_sample_time(region.end))
        return region

    def get_min_visible_length(self):
        return self.MIN_VISIBLE_BEATS

    def set_focus_marker_without_updating_visible_region(self, identifier):
        self._focused_identifier = identifier
        self._request_select_region = True
        current_region = self.visible_region
        roi = self._get_roi_for_object_identifier(identifier)
        self.focus_marker = FocusMarker(self.focusable_object_descriptions[identifier].focus_name, current_region.end if roi.end_identifier == identifier else current_region.start)

    def _get_start_end_region(self):
        start_position = min(self._clip.positions.start_marker, self._clip.positions.loop_start)
        return (
         start_position, self._clip.positions.loop_end)

    @listens('is_recording')
    def __on_is_recording_changed(self):
        self._update_timeline_region()

    @listens('before_update_all')
    def __on_before_update_all(self):
        self._process_object_changes = False

    @listens('after_update_all')
    def __on_after_update_all(self):
        self._process_object_changes = True
        self._request_select_region = True

    def _update_timeline_region(self):
        self.timeline_region = Region(min(self._clip.positions.start, self._clip.positions.start_marker, self._clip.positions.loop_start), max(self._clip.positions.end, self._clip.positions.loop_end))


class MidiClipTimelineNavigation(ClipTimelineNavigation):

    def __init__(self, clip=None, *a, **k):
        (super(MidiClipTimelineNavigation, self).__init__)(a, clip=clip, **k)
        self._MidiClipTimelineNavigation__on_clip_end_changed.subject = self._clip.positions

    @listens('end')
    def __on_clip_end_changed(self, _):
        if self._process_object_changes:
            self._update_timeline_region()


class AudioClipTimelineNavigation(ClipTimelineNavigation, WaveformNavigation):

    def __init__(self, *a, **k):
        (super(AudioClipTimelineNavigation, self).__init__)(*a, **k)
        self._AudioClipTimelineNavigation__on_warp_markers_changed.subject = self._clip.positions
        self._AudioClipTimelineNavigation__on_use_beat_time_changed.subject = self._clip.positions
        self._update_timeline_region()

    def set_visible_region(self, region, source_action=None, force_animate=False):
        super(AudioClipTimelineNavigation, self).set_visible_region(region, source_action, force_animate)
        self.visible_region_in_samples = self.get_region_in_samples(self.visible_region)

    @listens('warp_markers')
    def __on_warp_markers_changed(self):
        self._update_waveform_region_and_preserve_visible_region()

    @listens('use_beat_time')
    def __on_use_beat_time_changed(self, use_beat_time):
        self._update_waveform_region_and_preserve_visible_region()

    def get_min_visible_length(self):
        if self._clip.warping:
            return self._clip.sample_to_beat_time(self.MIN_VISIBLE_SAMPLES) - self._clip.sample_to_beat_time(0)
        return self.MIN_VISIBLE_SAMPLES

    def _update_waveform_region_and_preserve_visible_region(self):
        region = self.visible_region_in_samples
        self._update_timeline_region()
        if self._clip.warping:
            region = Region(self._clip.sample_to_beat_time(region.start), self._clip.sample_to_beat_time(region.end))
        self.set_visible_region(region)