# emacs-mode: -*- python-*-
# -*- coding: utf-8 -*-

import Live
from _Framework.SessionZoomingComponent import SessionZoomingComponent
from _Framework.ButtonElement import ButtonElement
class SpecialZoomingComponent(SessionZoomingComponent):
    ' Special ZoomingComponent that uses clip stop buttons for stop all when zoomed '
    __module__ = __name__

    def __init__(self, session):
        SessionZoomingComponent.__init__(self, session)


    def _scroll_up(self):
        #if self._is_zoomed_out:
        height       = self._session.height()
        track_offset = self._session.track_offset()
        scene_offset = self._session.scene_offset()

        if scene_offset > 0:
            new_scene_offset = scene_offset
            if scene_offset % height > 0:
                new_scene_offset -= (scene_offset % height)
            else:
                new_scene_offset = max(0, scene_offset - height)
            self._session.set_offsets(track_offset, new_scene_offset)

    def _scroll_down(self):
        #if self._is_zoomed_out:
            height       = self._session.height()
            track_offset = self._session.track_offset()
            scene_offset = self._session.scene_offset()
            new_scene_offset = scene_offset + height - (scene_offset % height)
            self._session.set_offsets(track_offset, new_scene_offset)

    def _scroll_left(self):
        #if self._is_zoomed_out:
        width        = self._session.width()
        track_offset = self._session.track_offset()
        scene_offset = self._session.scene_offset()
        if track_offset > 0:
            new_track_offset = track_offset
            if track_offset % width > 0:
                new_track_offset -= (track_offset % width)
            else:
                new_track_offset = max(0, track_offset - width)
            self._session.set_offsets(new_track_offset, scene_offset)

    def _scroll_right(self):
        #if self._is_zoomed_out:
        width        = self._session.width()
        track_offset = self._session.track_offset()
        scene_offset = self._session.scene_offset()
        new_track_offset = track_offset + width - (track_offset % width)
        self._session.set_offsets(new_track_offset, scene_offset)
