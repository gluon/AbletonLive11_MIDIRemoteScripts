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