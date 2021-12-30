#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v2/control_surface/components/session_overview.py
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
from past.utils import old_div
from ...base import in_range, listens, liveobj_valid
from ..component import Component

class SessionOverviewComponent(Component):
    u"""
    Class using a matrix of buttons to choose blocks of clips in the
    session, as if you had zoomed out from session.
    """

    def __init__(self, session_ring = None, enable_skinning = False, *a, **k):
        super(SessionOverviewComponent, self).__init__(*a, **k)
        assert session_ring is not None
        self._buttons = None
        self._scene_bank_index = 0
        self._track_bank_index = 0
        self._empty_value = 0
        self._stopped_value = 100
        self._playing_value = 127
        self._selected_value = 64
        self._session_ring = session_ring
        self.__on_session_offset_changes.subject = self._session_ring
        self.__on_scene_list_changed.subject = self.song
        if enable_skinning:
            self._enable_skinning()

    def _enable_skinning(self):
        self.set_stopped_value(u'Zooming.Stopped')
        self.set_selected_value(u'Zooming.Selected')
        self.set_playing_value(u'Zooming.Playing')
        self.set_empty_value(u'Zooming.Empty')

    @listens(u'scenes')
    def __on_scene_list_changed(self):
        self.update()

    def set_button_matrix(self, buttons):
        if buttons:
            buttons.reset()
        self._buttons = buttons
        self.__on_matrix_value.subject = self._buttons
        self.update()
        self._update_bank_index(self._session_ring.track_offset, self._session_ring.scene_offset)

    def set_empty_value(self, value):
        self._empty_value = value

    def set_playing_value(self, value):
        self._playing_value = value

    def set_stopped_value(self, value):
        self._stopped_value = value

    def set_selected_value(self, value):
        self._selected_value = value

    def update(self):
        super(SessionOverviewComponent, self).update()
        if self.is_enabled():
            self._update_matrix_buttons()

    def _update_matrix_buttons(self):
        if self._buttons != None:
            tracks = self._session_ring.tracks_to_use()
            scenes = self.song.scenes
            slots_registry = [ None for index in range(len(scenes)) ]
            width = self._session_ring.num_tracks
            height = self._session_ring.num_scenes
            for x in range(self._buttons.width()):
                for y in range(self._buttons.height()):
                    value_to_send = self._empty_value
                    track_bank_offset = self._track_bank_index * self._buttons.width() * width
                    scene_bank_offset = self._scene_bank_index * self._buttons.height() * height
                    track_offset = x * width + track_bank_offset
                    scene_offset = y * height + scene_bank_offset
                    if track_offset in range(len(tracks)) and scene_offset in range(len(scenes)):
                        value_to_send = self._stopped_value
                        if self._session_ring.track_offset - track_bank_offset in range(width * (x - 1) + 1, width * (x + 1)) and self._session_ring.scene_offset - scene_bank_offset in range(height * (y - 1) + 1, height * (y + 1)):
                            value_to_send = self._selected_value
                        else:
                            playing = False
                            for track in range(track_offset, track_offset + width):
                                for scene in range(scene_offset, scene_offset + height):
                                    if track in range(len(tracks)) and scene in range(len(scenes)):
                                        if not liveobj_valid(slots_registry[scene]):
                                            slots_registry[scene] = scenes[scene].clip_slots
                                        slot = slots_registry[scene][track] if len(slots_registry[scene]) > track else None
                                        if liveobj_valid(slot) and slot.has_clip and slot.clip.is_playing:
                                            value_to_send = self._playing_value
                                            playing = True
                                            break

                                if playing:
                                    break

                    if in_range(value_to_send, 0, 128):
                        self._buttons.send_value(x, y, value_to_send)
                    else:
                        self._buttons.set_light(x, y, value_to_send)

    @listens(u'offset')
    def __on_session_offset_changes(self, track_offset, scene_offset):
        self._update_bank_index(track_offset, scene_offset)

    def _update_bank_index(self, track_offset, scene_offset):
        if self._buttons and self.is_enabled():
            self._track_bank_index = int(old_div(old_div(track_offset, self._session_ring.num_tracks), self._buttons.width()))
            self._scene_bank_index = int(old_div(old_div(scene_offset, self._session_ring.num_scenes), self._buttons.height()))
        self.update()

    @listens(u'value')
    def __on_matrix_value(self, value, x, y, is_momentary):
        if self.is_enabled():
            if value != 0 or not is_momentary:
                track_offset = (x + self._track_bank_index * self._buttons.width()) * self._session_ring.num_tracks
                scene_offset = (y + self._scene_bank_index * self._buttons.height()) * self._session_ring.num_scenes
                if track_offset in range(len(self._session_ring.tracks_to_use())) and scene_offset in range(len(self.song.scenes)):
                    self._session_ring.set_offsets(track_offset, scene_offset)
