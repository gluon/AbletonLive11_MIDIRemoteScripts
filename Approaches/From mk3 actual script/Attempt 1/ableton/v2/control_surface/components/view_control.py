#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v2/control_surface/components/view_control.py
from __future__ import absolute_import, print_function, unicode_literals
import Live
from ...base import depends, in_range, liveobj_valid
from ..component import Component
from .scroll import ScrollComponent, Scrollable
NavDirection = Live.Application.Application.View.NavDirection
VIEWS = (u'Browser', u'Arranger', u'Session', u'Detail', u'Detail/Clip', u'Detail/DeviceChain')

class _DeltaSongScroller(Scrollable):

    @depends(song=None)
    def __init__(self, song = None, *a, **k):
        super(_DeltaSongScroller, self).__init__(*a, **k)
        self._song = song

    _do_scroll = NotImplemented
    _can_scroll = NotImplemented

    def scroll_up(self):
        if self.can_scroll_up():
            self._do_scroll(-1)

    def scroll_down(self):
        if self.can_scroll_down():
            self._do_scroll(1)

    def can_scroll_up(self):
        return self._can_scroll(-1)

    def can_scroll_down(self):
        return self._can_scroll(1)


def all_tracks(song):
    return list(tuple(song.visible_tracks) + tuple(song.return_tracks) + (song.master_track,))


def next_item(seq, item, delta):
    return seq[list(seq).index(item) + delta]


def has_next_item(seq, item, delta):
    try:
        return in_range(list(seq).index(item) + delta, 0, len(seq))
    except ValueError:
        return False


class BasicTrackScroller(_DeltaSongScroller):

    def _do_scroll(self, delta):
        song = self._song
        tracks = all_tracks(song)
        song.view.selected_track = next_item(tracks, song.view.selected_track, delta)

    def _can_scroll(self, delta):
        tracks = all_tracks(self._song)
        try:
            return has_next_item(tracks, self._song.view.selected_track, delta)
        except ValueError:
            return False


class TrackScroller(BasicTrackScroller):

    def _do_scroll(self, delta):
        super(TrackScroller, self)._do_scroll(delta)
        self._select_scene_of_playing_clip(self._song.view.selected_track)

    def _select_scene_of_playing_clip(self, track):
        if track.can_be_armed:
            playing_slot_index = track.playing_slot_index
            if playing_slot_index >= 0 and track.clip_slots[playing_slot_index].clip:
                self._song.view.highlighted_clip_slot = track.clip_slots[playing_slot_index]


class BasicSceneScroller(_DeltaSongScroller):

    def _do_scroll(self, delta):
        song = self._song
        view = song.view
        view.selected_scene = next_item(song.scenes, view.selected_scene, delta)

    def _can_scroll(self, delta):
        song = self._song
        view = song.view
        return has_next_item(song.scenes, view.selected_scene, delta)


class SceneScroller(BasicSceneScroller):

    def _do_scroll(self, delta):
        super(SceneScroller, self)._do_scroll(delta)
        if liveobj_valid(self._song.view.highlighted_clip_slot):
            if self._song.view.highlighted_clip_slot.has_clip:
                self._song.view.highlighted_clip_slot.fire(force_legato=True, launch_quantization=Live.Song.Quantization.q_no_q)
            else:
                self._song.view.selected_track.stop_all_clips(False)


class SceneListScroller(BasicSceneScroller):

    def _do_scroll(self, delta):
        super(SceneListScroller, self)._do_scroll(delta)
        self._song.view.selected_scene.fire(force_legato=True, can_select_scene_on_launch=False)


class ViewControlComponent(Component):
    u"""
    Component that can toggle the device chain- and clip view of the
    selected track
    """

    def __init__(self, *a, **k):
        super(ViewControlComponent, self).__init__(*a, **k)
        self._scroll_tracks = ScrollComponent(self._create_track_scroller(), parent=self)
        self._scroll_scene_list = ScrollComponent(SceneListScroller(), parent=self)
        self._scroll_scenes = ScrollComponent(self._create_scene_scroller(), parent=self)
        song = self.song
        view = song.view
        self.register_slot(song, self._scroll_tracks.update, u'visible_tracks')
        self.register_slot(song, self._scroll_tracks.update, u'return_tracks')
        self.register_slot(song, self._scroll_scenes.update, u'scenes')
        self.register_slot(song, self._scroll_scene_list.update, u'scenes')
        self.register_slot(view, self._scroll_tracks.update, u'selected_track')
        self.register_slot(view, self._scroll_scenes.update, u'selected_scene')
        self.register_slot(view, self._scroll_scene_list.update, u'selected_scene')

    def _create_track_scroller(self):
        return TrackScroller()

    def _create_scene_scroller(self):
        return SceneScroller()

    def set_next_track_button(self, button):
        self._scroll_tracks.set_scroll_down_button(button)

    def set_prev_track_button(self, button):
        self._scroll_tracks.set_scroll_up_button(button)

    def set_next_scene_button(self, button):
        self._scroll_scenes.set_scroll_down_button(button)

    def set_prev_scene_button(self, button):
        self._scroll_scenes.set_scroll_up_button(button)

    def set_next_scene_list_button(self, button):
        self._scroll_scene_list.set_scroll_down_button(button)

    def set_prev_scene_list_button(self, button):
        self._scroll_scene_list.set_scroll_up_button(button)

    def show_view(self, view):
        assert view in VIEWS
        app_view = self.application.view
        try:
            if view == u'Detail/DeviceChain' or u'Detail/Clip':
                if not app_view.is_view_visible(u'Detail'):
                    app_view.show_view(u'Detail')
            if not app_view.is_view_visible(view):
                app_view.show_view(view)
        except RuntimeError:
            pass

    def focus_view(self, view):
        assert view in VIEWS
        app_view = self.application.view
        if view == u'Detail/DeviceChain' or u'Detail/Clip':
            if not app_view.is_view_visible(u'Detail'):
                app_view.show_view(u'Detail')
        if not app_view.is_view_visible(view):
            app_view.focus_view(view)
