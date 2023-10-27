# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchkey_MK2\ModeUtils.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 3044 bytes
from __future__ import absolute_import, print_function, unicode_literals
from _Framework.Dependency import depends
from _Framework.ModesComponent import ModeButtonBehaviour, ModesComponent
from . import consts

def to_class_name(mode_name):
    return ''.join([s.capitalize() for s in mode_name.replace('_', ' ').split()])


class MomentaryBehaviour(ModeButtonBehaviour):

    @depends(send_midi=None)
    def __init__(self, send_midi=None, *a, **k):
        (super(MomentaryBehaviour, self).__init__)(*a, **k)
        self._send_midi = send_midi

    def press_immediate(self, component, mode):
        self._send_midi(consts.IN_CONTROL_QUERY)

    def release_immediate(self, component, mode):
        pass

    def press_delayed(self, component, mode):
        component.push_mode(mode)

    def release_delayed(self, component, mode):
        component.pop_mode(mode)


class SkinableBehaviourMixin(ModeButtonBehaviour):

    def update_button(self, component, mode, selected_mode):
        button = component.get_mode_button(mode)
        groups = component.get_mode_groups(mode)
        selected_groups = component.get_mode_groups(selected_mode)
        mode_color = to_class_name(mode)
        is_selected = mode == selected_mode or bool(groups & selected_groups)
        button.set_light('Mode.%s%s' % (mode_color, 'On' if is_selected else ''))


class DisablingModesComponent(ModesComponent):

    def __init__(self, *a, **k):
        (super(DisablingModesComponent, self).__init__)(*a, **k)
        self._enabled_modes = {}

    def add_mode(self, name, mode_or_component, is_enabled=True, **k):
        (super(DisablingModesComponent, self).add_mode)(name, mode_or_component, **k)
        self._enabled_modes[name] = is_enabled

    def set_mode_enabled(self, mode, enable):
        self._enabled_modes[mode] = enable
        self.update()

    def _update_buttons(self, selected):
        if self.is_enabled():
            for name, entry in self._mode_map.items():
                if entry.subject_slot.subject != None:
                    if self._enabled_modes[name]:
                        self._get_mode_behaviour(name).update_button(self, name, selected)
                    else:
                        button = self.get_mode_button(name)
                        button.set_light('Mode.Disabled')

            if self._mode_toggle:
                entry = self._mode_map.get(selected)
                value = entry and entry.toggle_value
                self._mode_toggle.set_light(value)

    def _on_mode_button_value(self, name, value, sender):
        if self._enabled_modes[name]:
            super(DisablingModesComponent, self)._on_mode_button_value(name, value, sender)