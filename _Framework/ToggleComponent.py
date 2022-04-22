# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/_Framework/ToggleComponent.py
# Compiled at: 2021-06-29 09:33:48
# Size of source mod 2**32: 2887 bytes
from __future__ import absolute_import, print_function, unicode_literals
from .ControlSurfaceComponent import ControlSurfaceComponent
from .SubjectSlot import subject_slot

class ToggleComponent(ControlSurfaceComponent):
    is_private = True
    is_momentary = False
    read_only = False

    def __init__(self, property_name=None, subject=None, is_momentary=False, model_transform=None, view_transform=None, read_only=False, *a, **k):
        (super(ToggleComponent, self).__init__)(*a, **k)
        self._property_name = property_name
        self._property_slot = self.register_slot(subject, self._on_property_changed_in_model, property_name)
        self._property_button = None
        if is_momentary:
            self.is_momentary = is_momentary
        if model_transform:
            self.model_transform = model_transform
        if view_transform:
            self.view_transform = view_transform
        if read_only:
            self.read_only = read_only

    def model_transform(self, value):
        return value

    def view_transform(self, value):
        return value

    def _get_subject(self):
        return self._property_slot.subject

    def _set_subject(self, model):
        self._property_slot.subject = model
        self.update()

    subject = property(_get_subject, _set_subject)

    def _get_value(self):
        if self.subject:
            return getattr(self.subject, self._property_name)

    def _set_value(self, value):
        setattr(self.subject, self._property_name, value)

    value = property(_get_value, _set_value)

    def set_toggle_button(self, button):
        self._on_button_value.subject = button
        self._update_button()

    def on_enabled_changed(self):
        self.update()

    def update(self):
        super(ToggleComponent, self).update()
        self._update_button()

    def _update_button(self):
        if self.is_enabled():
            button = self._on_button_value.subject
            if button:
                button.set_light(self.view_transform(self.value))

    def _on_property_changed_in_model(self):
        self._update_button()

    @subject_slot('value')
    def _on_button_value(self, value):
        if self.is_enabled() and not self.read_only:
            if self.is_momentary:
                if value:
                    self.value = self.model_transform(True)
                else:
                    self.value = self.model_transform(False)
        elif value:
            self.value = self.model_transform(not self.value)