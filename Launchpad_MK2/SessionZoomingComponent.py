# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Launchpad_MK2/SessionZoomingComponent.py
# Compiled at: 2022-01-27 16:28:16
# Size of source mod 2**32: 1188 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import map
import _Framework.SessionComponent as SessionComponent
import _Framework.SessionZoomingComponent as SessionZoomingComponentBase
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