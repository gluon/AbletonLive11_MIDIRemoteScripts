# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\mode\behaviour.py
# Compiled at: 2023-09-13 04:24:51
# Size of source mod 2**32: 3845 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ...base import mixin
from . import ModeButtonBehaviour, pop_last_mode

def make_reenter_behaviour(base_behaviour, on_reenter=None, *a, **k):
    return (mixin(ReenterBehaviourMixin, base_behaviour))(a, on_reenter=on_reenter, **k)


class ReenterBehaviourMixin:

    def __init__(self, on_reenter=None, *a, **k):
        (super().__init__)(*a, **k)
        self._on_reenter = on_reenter

    def press_immediate(self, component, mode):
        was_active = component.selected_mode == mode
        super().press_immediate(component, mode)
        if was_active:
            self._on_reenter()


class ToggleBehaviour(ModeButtonBehaviour):

    def __init__(self, return_to_default=False, *a, **k):
        (super().__init__)(*a, **k)
        self._return_to_default = return_to_default

    def press_immediate(self, component, mode):
        if component.selected_mode == mode:
            if self._return_to_default:
                component.push_mode(component.modes[0])
                component.pop_unselected_modes()
            else:
                pop_last_mode(component, mode)
        else:
            component.push_mode(mode)


class MomentaryBehaviour(ModeButtonBehaviour):

    def __init__(self, entry_delay=None, exit_delay=None, immediate_exit_delay=None):
        self._entry_delay = entry_delay
        self._exit_delay = exit_delay
        self._immediate_exit_delay = self._exit_delay if immediate_exit_delay is None else immediate_exit_delay

    def press_immediate(self, component, mode):
        component.push_mode(mode, delay=(self._entry_delay))

    def release_immediate(self, component, mode):
        component.pop_mode(mode, delay=(self._immediate_exit_delay))

    def release_delayed(self, component, mode):
        component.pop_mode(mode, delay=(self._exit_delay))