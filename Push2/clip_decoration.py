#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Push2/clip_decoration.py
from __future__ import absolute_import, print_function, unicode_literals
from builtins import zip
from builtins import object
from ableton.v2.base import liveobj_valid, listenable_property, listens, EventObject
from ableton.v2.control_surface import InternalParameter, DecoratorFactory, LiveObjectDecorator
from .decoration import find_decorated_object
from .timeline_navigation import AudioClipTimelineNavigation, MidiClipTimelineNavigation

class ClipPositions(EventObject):
    __events__ = (u'is_recording', u'warp_markers', u'before_update_all', u'after_update_all')
    MAX_TIME = 10000000
    MIN_TIME = -10000
    start = listenable_property.managed(0.0)
    end = listenable_property.managed(0.0)
    start_marker = listenable_property.managed(0.0)
    end_marker = listenable_property.managed(0.0)
    loop_start = listenable_property.managed(0.0)
    loop_end = listenable_property.managed(0.0)
    loop_length = listenable_property.managed(0.0)
    use_beat_time = listenable_property.managed(False)

    def __init__(self, clip = None, *a, **k):
        assert clip is not None
        super(ClipPositions, self).__init__(*a, **k)
        self._clip = clip
        self._looping = self._clip.looping
        self.__on_is_recording_changed.subject = clip
        self.__on_looping_changed.subject = clip
        self.__on_start_marker_changed.subject = clip
        self.__on_end_marker_changed.subject = clip
        self.__on_loop_start_changed.subject = clip
        self.__on_loop_end_changed.subject = clip
        self.__on_loop_start_changed()
        self.__on_loop_end_changed()
        if clip.is_audio_clip:
            self.__on_warping_changed.subject = clip
            self.__on_warp_markers_changed.subject = clip
        if clip.is_midi_clip:
            self.__on_notes_changed.subject = clip
            self._update_start_end_note_times()
        self.update_all()

    @property
    def is_warping(self):
        return self._clip.is_audio_clip and self._clip.warping

    def _convert_to_desired_unit(self, beat_time_or_seconds):
        u"""
        This converts the given beat time or seconds unit to the desired unit.
        - If the input unit is beat time, we are warped and don't need to do
          anything.
        - If the input time is seconds, we want to have sample time and need to
          convert.
        - If the clip is a midi clip, we don't need to do anything
        """
        if not self._clip.is_midi_clip and not self.is_warping:
            beat_time_or_seconds = self._clip.seconds_to_sample_time(beat_time_or_seconds)
        return beat_time_or_seconds

    @listens(u'start_marker')
    def __on_start_marker_changed(self):
        if not self._process_looping_update():
            self.start_marker = self._convert_to_desired_unit(self._clip.start_marker)

    @listens(u'end_marker')
    def __on_end_marker_changed(self):
        if not self._process_looping_update():
            self.end_marker = self._convert_to_desired_unit(self._clip.end_marker)

    @listens(u'loop_start')
    def __on_loop_start_changed(self):
        if not self._process_looping_update():
            self.loop_start = self._convert_to_desired_unit(self._clip.loop_start)
        self._update_loop_length()

    @listens(u'loop_end')
    def __on_loop_end_changed(self):
        if not self._process_looping_update():
            self.loop_end = self._convert_to_desired_unit(self._clip.loop_end)
        self._update_loop_length()

    @listens(u'is_recording')
    def __on_is_recording_changed(self):
        self._update_start_end()
        self.notify_is_recording()

    @listens(u'warp_markers')
    def __on_warp_markers_changed(self):
        self.update_all()
        self.notify_warp_markers()

    @listens(u'looping')
    def __on_looping_changed(self):
        self.update_all()

    @listens(u'warping')
    def __on_warping_changed(self):
        self.update_all()

    @listens(u'notes')
    def __on_notes_changed(self):
        self._update_start_end_note_times()
        self._update_start_end()

    def _update_start_end_note_times(self):
        all_notes = self._clip.get_notes_extended(from_time=self.MIN_TIME, from_pitch=0, time_span=self.MAX_TIME, pitch_span=128)
        start_times, end_times = list(zip(*[ (note.start_time, note.start_time + note.duration) for note in all_notes ])) if len(all_notes) > 0 else ([self.MAX_TIME], [self.MIN_TIME])
        self.start_of_first_note = min(start_times)
        self.end_of_last_note = max(end_times)

    def _process_looping_update(self):
        u"""
        Changing the looping setting is considered a transaction and will update
        all parameters.
        This method should be called, before updating any position parameter.
        Returns True, in case a looping change has been processed.
        """
        looping = self._clip.looping
        if looping != self._looping:
            self._looping = looping
            self.update_all()
            return True
        return False

    def _update_loop_length(self):
        self.loop_length = self._convert_to_desired_unit(self._clip.loop_end) - self._convert_to_desired_unit(self._clip.loop_start)

    def _update_start_end(self):
        start = None
        end = None
        if self.is_warping:
            start = self._clip.sample_to_beat_time(0)
            end = self._clip.sample_to_beat_time(self._clip.sample_length)
        elif self._clip.is_audio_clip:
            start = 0
            end = self._clip.sample_length
        else:
            start = self.start_of_first_note
            end = self.end_of_last_note
        self.start = min(start, self.loop_start if self._clip.looping else self.start_marker)
        self.end = max(end, self.loop_end)

    def update_all(self):
        self.notify_before_update_all()
        self.__on_start_marker_changed()
        self.__on_end_marker_changed()
        self.__on_loop_start_changed()
        self.__on_loop_end_changed()
        self._update_start_end()
        if self._clip.is_audio_clip:
            self.use_beat_time = self._clip.warping
        self.notify_after_update_all()


class MidiClipZoomParameter(MidiClipTimelineNavigation, InternalParameter):
    pass


class AudioClipZoomParameter(AudioClipTimelineNavigation, InternalParameter):
    pass


class ClipDecoration(EventObject, LiveObjectDecorator):
    __events__ = (u'zoom',)

    def __init__(self, *a, **k):
        super(ClipDecoration, self).__init__(*a, **k)
        self._positions = self.register_disconnectable(ClipPositions(self))
        parameter_type = AudioClipZoomParameter if self._live_object.is_audio_clip else MidiClipZoomParameter
        self._zoom_parameter = parameter_type(name=u'Zoom', parent=self._live_object, clip=self)
        self._zoom_parameter.focus_object(self._zoom_parameter.start_marker_focus)
        self.register_disconnectable(self._zoom_parameter)

    @property
    def positions(self):
        return self._positions

    @property
    def zoom(self):
        return self._zoom_parameter

    @property
    def timeline_navigation(self):
        return self._zoom_parameter


class ClipDecoratorFactory(DecoratorFactory):
    _decorator = ClipDecoration

    @classmethod
    def _should_be_decorated(cls, clip):
        return liveobj_valid(clip)


class ClipDecoratedPropertiesCopier(object):

    def __init__(self, source_clip = None, destination_clip = None, decorator_factory = None):
        self._source_clip = source_clip
        self._destination_clip = destination_clip
        self._decorator_factory = decorator_factory

    def post_duplication_action(self):
        decorated_clip = find_decorated_object(self._source_clip, self._decorator_factory)
        if decorated_clip:
            self._copy_zoom_parameter(decorated_clip)

    def _copy_zoom_parameter(self, copied_decorated_clip):
        if not self._destination_clip:
            return
        new_clip_decorated = self._decorator_factory.decorate(self._destination_clip)
        new_clip_decorated.zoom.copy_state(copied_decorated_clip.zoom)
