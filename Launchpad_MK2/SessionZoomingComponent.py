# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchpad_MK2\SessionZoomingComponent.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 1226 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import map
import _Framework.SessionComponent as SessionComponent
from _Framework.SessionZoomingComponent import SessionZoomingComponent as SessionZoomingComponentBase
from .ComponentUtils import skin_scroll_component

class SessionZoomingComponent(SessionZoomingComponentBase):

    def _enable_skinning(self):
        super(SessionZoomingComponent, self)._enable_skinning()
        list(map(skin_scroll_component, (self._horizontal_scroll, self._vertical_scroll)))

    def register_component(self, component):
        self._sub_components.append(component)
        return component

    def on_enabled_changed(self):
        self.update()

    def set_enabled(self, enable):
        self._explicit_is_enabled = bool(enable)
        self._update_is_enabled()
        for component in self._sub_components:
            if not isinstance(component, SessionComponent):
                component._set_enabled_recursive(self.is_enabled())