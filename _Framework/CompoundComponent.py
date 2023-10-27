# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_Framework\CompoundComponent.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 2059 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import map
from .ControlSurfaceComponent import ControlSurfaceComponent

class CompoundComponent(ControlSurfaceComponent):

    def __init__(self, *a, **k):
        (super(CompoundComponent, self).__init__)(*a, **k)
        self._sub_components = []

    def update_all(self):
        self.update()
        for component in self._sub_components:
            component.update_all()

    def register_component(self, component):
        component._set_enabled_recursive(self.is_enabled())
        self._sub_components.append(component)
        return component

    def register_components(self, *a):
        return list(map(self.register_component, a))

    def has_component(self, component):
        return component in self._sub_components

    def set_enabled(self, enable):
        super(CompoundComponent, self).set_enabled(enable)
        for component in self._sub_components:
            component._set_enabled_recursive(self.is_enabled())

    def _set_enabled_recursive(self, enable):
        super(CompoundComponent, self)._set_enabled_recursive(enable)
        for component in self._sub_components:
            component._set_enabled_recursive(self.is_enabled())

    def set_allow_update(self, allow_updates):
        allow = bool(allow_updates)
        if self._allow_updates != allow:
            for component in self._sub_components:
                component.set_allow_update(allow)

            super(CompoundComponent, self).set_allow_update(allow)