<<<<<<< HEAD
from __future__ import absolute_import, print_function, unicode_literals
from functools import partial
from .. import Component
from ..controls import ButtonControl, InputControl, RadioButtonGroup

class NopControl(InputControl):

    class State(InputControl.State):

        def _event_listener_required(self):
            return True


class BackgroundComponent(Component):

    def __init__(self, name='Background', control_type=None, *a, **k):
        (super().__init__)(a, name=name, **k)
        self._control_type = control_type or NopControl

    def _setup_control_state(self, name, control_state):
        pass

    def __getattr__(self, name):
        if name.startswith('set_'):
            return partial(self._set_element_for_control, name[4:])
        raise AttributeError(name)

    def _set_element_for_control(self, name, element):
        if element:
            element.reset()
        if name in self.__dict__:
            self.__dict__[name].set_control_element(element)
        else:
            control = self._control_type()
            control_state = control._get_state(self)
            setattr(self, name, control_state)
            self._setup_control_state(name, control_state)
            control_state.set_control_element(element)


class TranslatingBackgroundComponent(BackgroundComponent):
    channel_selection_buttons = RadioButtonGroup(unchecked_color='Translation.Channel.NotSelected',
      checked_color='Translation.Channel.Selected')

    def __init__(self, name='Translating_Background', translation_channel=0, *a, **k):
        (super().__init__)(a, name=name, **k)
        self._base_translation_channel = translation_channel

    def set_channel_selection_buttons(self, buttons):
        self.channel_selection_buttons.set_control_element(buttons)
        if buttons:
            if self.channel_selection_buttons.checked_index < 0:
                self.channel_selection_buttons.checked_index = 0

    @channel_selection_buttons.checked
    def channel_selection_buttons(self, button):
        for control_state in self._control_states.values():
            control_state.channel = self._base_translation_channel + button.index

    def _setup_control_state(self, _, control_state):
        control_state.channel = self._base_translation_channel


class ModifierBackgroundComponent(BackgroundComponent):

    def __init__(self, name='Modifier_Background', *a, **k):
        (super().__init__)(a, name=name, control_type=ButtonControl, **k)

    def _setup_control_state(self, name, control_state):
        base_name = self.name.title().replace('_', '')
        control_name = name.title().replace('_', '')
        control_state.color = '{}.{}'.format(base_name, control_name)
        control_state.pressed_color = '{}.{}Pressed'.format(base_name, control_name)
=======
# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v3/control_surface/components/background.py
# Compiled at: 2022-01-28 05:06:24
# Size of source mod 2**32: 1598 bytes
from __future__ import absolute_import, print_function, unicode_literals
from future.utils import itervalues
from functools import partial
from ...base import nop
from .. import Component

class BackgroundComponent(Component):

    def __init__(self, name='Background', *a, **k):
        (super().__init__)(a, name=name, **k)
        self._control_slots = {}
        self._control_map = {}

    def __getattr__(self, name):
        if len(name) > 4:
            if name[:4] == 'set_':
                return partial(self._clear_control, name[4:])
        raise AttributeError(name)

    def _clear_control(self, name, control):
        slot = self._control_slots.get(name, None)
        if slot:
            del self._control_slots[name]
            self.disconnect_disconnectable(slot)
        if control:
            control.reset()
            self._control_map[name] = control
            self._control_slots[name] = self.register_slot(control, nop, 'value')
        elif name in self._control_map:
            del self._control_map[name]

    def update(self):
        super().update()
        if self.is_enabled():
            for control in itervalues(self._control_map):
                control.reset()
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
