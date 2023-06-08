from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import range
from past.utils import old_div
import _Framework.ButtonElement as ButtonElement
from _Framework.SessionZoomingComponent import DeprecatedSessionZoomingComponent

class ShiftableZoomingComponent(DeprecatedSessionZoomingComponent):

    def __init__(self, session, stop_buttons, *a, **k):
        (super(ShiftableZoomingComponent, self).__init__)(session, *a, **k)
        self._stop_buttons = stop_buttons
        self._ignore_buttons = False
        for button in self._stop_buttons:
            button.add_value_listener((self._stop_value), identify_sender=True)

    def disconnect(self):
        super(ShiftableZoomingComponent, self).disconnect()
        for button in self._stop_buttons:
            button.remove_value_listener(self._stop_value)

    def set_ignore_buttons(self, ignore):
        if self._ignore_buttons != ignore:
            self._ignore_buttons = ignore
            if not self._is_zoomed_out:
                self._session.set_enabled(not ignore)
            self.update()

    def update(self):
        if not self._ignore_buttons:
            super(ShiftableZoomingComponent, self).update()
        else:
            if self.is_enabled():
                if self._scene_bank_buttons != None:
                    for button in self._scene_bank_buttons:
                        button.turn_off()

    def _stop_value(self, value, sender):
        if self.is_enabled():
            if self._ignore_buttons or self._is_zoomed_out and not value != 0 or sender.is_momentary():
                self.song().stop_all_clips()

    def _zoom_value(self, value):
        if self.is_enabled():
            if self._zoom_button.is_momentary():
                self._is_zoomed_out = value > 0
            else:
                self._is_zoomed_out = not self._is_zoomed_out
            if not self._ignore_buttons:
                if self._is_zoomed_out:
                    self._scene_bank_index = int(old_div(old_div(self._session.scene_offset(), self._session.height()), self._buttons.height()))
                else:
                    self._scene_bank_index = 0
                self._session.set_enabled(not self._is_zoomed_out)
                if self._is_zoomed_out:
                    self.update()

    def _matrix_value(self, value, x, y, is_momentary):
        if not self._ignore_buttons:
            super(ShiftableZoomingComponent, self)._matrix_value(value, x, y, is_momentary)

    def _nav_up_value(self, value):
        if not self._ignore_buttons:
            super(ShiftableZoomingComponent, self)._nav_up_value(value)

    def _nav_down_value(self, value):
        if not self._ignore_buttons:
            super(ShiftableZoomingComponent, self)._nav_down_value(value)

    def _nav_left_value(self, value):
        if not self._ignore_buttons:
            super(ShiftableZoomingComponent, self)._nav_left_value(value)

    def _nav_right_value(self, value):
        if not self._ignore_buttons:
            super(ShiftableZoomingComponent, self)._nav_right_value(value)

    def _scene_bank_value(self, value, sender):
        if not self._ignore_buttons:
            super(ShiftableZoomingComponent, self)._scene_bank_value(value, sender)