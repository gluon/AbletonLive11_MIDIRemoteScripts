# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchpad_MK2\ModeUtils.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 3511 bytes
from __future__ import absolute_import, print_function, unicode_literals
from _Framework.Dependency import depends
from _Framework.ModesComponent import ImmediateBehaviour, ModeButtonBehaviour, ModesComponent

def to_class_name(mode_name):
    return ''.join([s.capitalize() for s in mode_name.split('_')])


class SkinableBehaviourMixin(ModeButtonBehaviour):

    def update_button(self, component, mode, selected_mode):
        button = component.get_mode_button(mode)
        groups = component.get_mode_groups(mode)
        selected_groups = component.get_mode_groups(selected_mode)
        is_selected = mode == selected_mode
        is_in_group = bool(groups & selected_groups)
        mode_color = to_class_name(mode)
        value_status = 'Off'
        if is_selected:
            value_status = 'On'
        else:
            if is_in_group:
                value_status = 'GroupOn'
        button.set_light('Mode.%s.%s' % (mode_color, value_status))


class EnablingReenterBehaviour(SkinableBehaviourMixin, ImmediateBehaviour):

    def __init__(self, component=None, *a, **k):
        (super(EnablingReenterBehaviour, self).__init__)(*a, **k)
        self._component = component

    def press_immediate(self, component, mode):
        was_active = component.selected_mode == mode
        super(EnablingReenterBehaviour, self).press_immediate(component, mode)
        if was_active:
            self.component_set_enabled(True)

    def release_immediate(self, component, mode):
        super(EnablingReenterBehaviour, self).release_immediate(component, mode)
        self.component_set_enabled(False)

    def release_delayed(self, component, mode):
        super(EnablingReenterBehaviour, self).release_delayed(component, mode)
        self.component_set_enabled(False)

    def component_set_enabled(self, enable):
        if self._component is not None:
            self._component.set_enabled(enable)


class NotifyingModesComponent(ModesComponent):

    @depends(switch_layout=None)
    def __init__(self, switch_layout=None, *a, **k):
        (super(NotifyingModesComponent, self).__init__)(*a, **k)
        self._modes_to_layout_bytes = {}
        self._switch_layout = switch_layout

    def add_mode(self, name, mode_or_component, layout_byte=None, toggle_value=False, groups=set(), behaviour=None):
        super(NotifyingModesComponent, self).add_mode(name, mode_or_component, toggle_value, groups, behaviour)
        if layout_byte is not None:
            self._modes_to_layout_bytes[name] = layout_byte

    def push_mode(self, mode):
        self.send_switch_layout_message(mode)
        super(NotifyingModesComponent, self).push_mode(mode)

    def send_switch_layout_message(self, mode=None):
        mode = mode or self.selected_mode
        try:
            layout_byte = self._modes_to_layout_bytes[mode]
            self._switch_layout(layout_byte)
        except KeyError:
            print("Couldn't switch layout on hardware")