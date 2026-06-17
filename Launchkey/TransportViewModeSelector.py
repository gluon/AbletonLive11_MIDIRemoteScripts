# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchkey\TransportViewModeSelector.py
# Compiled at: 2022-11-28 08:01:31
# Size of source mod 2**32: 1769 bytes
from __future__ import absolute_import, print_function, unicode_literals
import _Framework.ModeSelectorComponent as ModeSelectorComponent

class TransportViewModeSelector(ModeSelectorComponent):

    def __init__(self, transport, session, ffwd_button, rwd_button):
        ModeSelectorComponent.__init__(self)
        self._transport = transport
        self._session = session
        self._ffwd_button = ffwd_button
        self._rwd_button = rwd_button
        self._app_view().add_is_view_visible_listener('Session', self._on_view_changed)
        self.update()

    def disconnect(self):
        ModeSelectorComponent.disconnect(self)
        self._transport = None
        self._session = None
        self._ffwd_button = None
        self._rwd_button = None
        self._app_view().remove_is_view_visible_listener('Session', self._on_view_changed)

    def update(self):
        super(TransportViewModeSelector, self).update()
        if self.is_enabled():
            if self._mode_index == 0:
                self._transport.set_seek_buttons(self._ffwd_button, self._rwd_button)
                self._session.set_select_buttons(None, None)
            else:
                self._transport.set_seek_buttons(None, None)
                self._session.set_select_buttons(self._ffwd_button, self._rwd_button)

    def _app_view(self):
        return self.application().view

    def _on_view_changed(self):
        if self._app_view().is_view_visible('Session'):
            self._mode_index = 1
        else:
            self._mode_index = 0
        self.update()