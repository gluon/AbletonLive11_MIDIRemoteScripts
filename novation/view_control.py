<<<<<<< HEAD
=======
# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/novation/view_control.py
# Compiled at: 2021-06-29 09:33:48
# Size of source mod 2**32: 3657 bytes
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import EventObject, ObservablePropertyAlias, clamp, index_if, listens
from ableton.v2.control_surface.components import BasicSceneScroller, BasicTrackScroller, ScrollComponent, ViewControlComponent, all_tracks
from .util import skin_scroll_buttons

class NotifyingTrackScroller(BasicTrackScroller, EventObject):
    __events__ = ('scrolled', )

    def _do_scroll(self, delta):
        super(NotifyingTrackScroller, self)._do_scroll(delta)
        self.notify_scrolled()


class NotifyingTrackPager(NotifyingTrackScroller):

    def __init__(self, track_provider=None, *a, **k):
        (super(NotifyingTrackPager, self).__init__)(*a, **k)
        self._track_provider = track_provider

    def _do_scroll(self, delta):
        selected_track = self._song.view.selected_track
        tracks = all_tracks(self._song)
        selected_track_index = index_if(lambda t: t == selected_track
, tracks)
        len_tracks = len(tracks)
        new_index = selected_track_index + delta * self._track_provider.num_tracks
        self._song.view.selected_track = tracks[clamp(new_index, 0, len_tracks - 1)]
        self.notify_scrolled()


class NotifyingViewControlComponent(ViewControlComponent):
    __events__ = ('selection_scrolled', 'selection_paged')

    def __init__(self, track_provider=None, enable_skinning=True, *a, **k):
        self._track_provider = track_provider
        (super(NotifyingViewControlComponent, self).__init__)(*a, **k)
        self._page_tracks = ScrollComponent((self._create_track_pager()), parent=self)
        self._NotifyingViewControlComponent__on_tracks_changed.subject = self._track_provider
        self._NotifyingViewControlComponent__on_selected_track_changed.subject = self.song.view
        if enable_skinning:
            skin_scroll_buttons(self._page_tracks, 'TrackNavigation.On', 'TrackNavigation.Pressed')
            skin_scroll_buttons(self._scroll_tracks, 'TrackNavigation.On', 'TrackNavigation.Pressed')
            skin_scroll_buttons(self._scroll_scenes, 'SceneNavigation.On', 'SceneNavigation.Pressed')

    def set_prev_track_page_button(self, button):
        self._page_tracks.set_scroll_up_button(button)

    def set_next_track_page_button(self, button):
        self._page_tracks.set_scroll_down_button(button)

    def _create_track_scroller(self):
        scroller = NotifyingTrackScroller()
        self.register_disconnectable(ObservablePropertyAlias(self,
          property_host=scroller,
          property_name='scrolled',
          alias_name='selection_scrolled'))
        return scroller

    def _create_scene_scroller(self):
        return BasicSceneScroller()

    def _create_track_pager(self):
        pager = NotifyingTrackPager(track_provider=(self._track_provider))
        self.register_disconnectable(ObservablePropertyAlias(self,
          property_host=pager,
          property_name='scrolled',
          alias_name='selection_paged'))
        return pager

    @listens('tracks')
    def __on_tracks_changed(self):
        self._update_track_scrollers()

    @listens('selected_track')
    def __on_selected_track_changed(self):
        self._update_track_scrollers()

    def _update_track_scrollers(self):
        self._scroll_tracks.update()
        self._page_tracks.update()