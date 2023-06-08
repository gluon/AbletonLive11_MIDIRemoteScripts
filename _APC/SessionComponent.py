from __future__ import absolute_import, print_function, unicode_literals
from _Framework.SessionComponent import SessionComponent as SessionComponentBase

class SessionComponent(SessionComponentBase):

    def link_with_track_offset(self, track_offset):
        if self._is_linked():
            self._unlink()
        self.set_offsets(track_offset, self.scene_offset())
        self._link()

    def unlink(self):
        if self._is_linked():
            self._unlink()