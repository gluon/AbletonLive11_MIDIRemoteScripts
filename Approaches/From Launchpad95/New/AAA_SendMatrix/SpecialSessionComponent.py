from _Framework.SessionComponent import SessionComponent
from _Framework.SceneComponent import SceneComponent
import Live


class SpecialSessionComponent(SessionComponent):

    """Special session subclass that handles ConfigurableButtons"""

    def __init__(
        self, num_tracks, num_scenes, stop_clip_buttons, control_surface, main_selector
    ):
        self._stop_clip_buttons = stop_clip_buttons
        self._control_surface = control_surface
        self._main_selector = main_selector
        SessionComponent.__init__(
            self,
            num_tracks=num_tracks,
            num_scenes=num_scenes,
            enable_skinning=True,
            name="Session",
            is_root=True,
        )
        from .ColorsMK3 import CLIP_COLOR_TABLE, RGB_COLOR_TABLE

        self.set_rgb_mode(CLIP_COLOR_TABLE, RGB_COLOR_TABLE)

    def link_with_track_offset(self, track_offset):
        assert track_offset >= 0
        if self._is_linked():
            self._unlink()
        self.set_offsets(track_offset, 0)
        self._link()

    def _update_stop_clips_led(self, index):
        if (
            (self.is_enabled())
            and (self._stop_track_clip_buttons != None)
            and (index < len(self._stop_track_clip_buttons))
        ):
            button = self._stop_track_clip_buttons[index]
            tracks_to_use = self.tracks_to_use()
            track_index = index + self.track_offset()
            if 0 <= track_index < len(tracks_to_use):
                track = tracks_to_use[track_index]
                if track.fired_slot_index == -2:
                    button.send_value(self._stop_clip_triggered_value)
                elif track.playing_slot_index >= 0:
                    button.send_value(self._stop_clip_value)
                else:
                    button.turn_off()
            else:
                button.send_value(4)

    def unlink(self):
        if self._is_linked():
            self._unlink()

    def update(self):
        SessionComponent.update(self)

    def set_enabled(self, enabled):
        SessionComponent.set_enabled(self, enabled)

    def _reassign_tracks(self):
        SessionComponent._reassign_tracks(self)
