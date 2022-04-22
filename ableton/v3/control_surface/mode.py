# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v3/control_surface/mode.py
# Compiled at: 2022-01-27 16:28:17
# Size of source mod 2**32: 3830 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.mode import AddLayerMode, CompoundMode, EnablingMode, ImmediateBehaviour, LatchingBehaviour, LayerModeBase, Mode, ModeButtonControl
import ableton.v2.control_surface.mode as ModesComponentBase
from ableton.v2.control_surface.mode import MomentaryBehaviour, make_mode_button_control
from ..base import mixin
from .controls import SendValueInputControl
__all__ = ('AddLayerMode', 'CompoundMode', 'EnablingMode', 'ImmediateBehaviour', 'LatchingBehaviour',
           'LayerModeBase', 'Mode', 'ModeButtonControl', 'ModesComponent', 'MomentaryBehaviour',
           'ReenterBehaviourMixin', 'make_mode_button_control', 'make_reenter_behaviour')

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


class ModesComponent(ModesComponentBase):
    mode_selection_control = SendValueInputControl()

    def __init__(self, name=None, enable_skinning=False, *a, **k):
        (super().__init__)(a, name=name, enable_skinning=enable_skinning, **k)

    @mode_selection_control.value
    def mode_selection_control(self, value, _):
        modes = self.modes
        if value < len(modes):
            self.selected_mode = modes[value]

    def add_mode(self, name, mode_or_component, cycle_mode_button_color=None, groups=None, behaviour=None):
        if self._enable_skinning:
            if cycle_mode_button_color is None:
                cycle_mode_button_color = '{}.On'.format(self._get_mode_color_base_name(name))
        super().add_mode(name,
          mode_or_component,
          cycle_mode_button_color=cycle_mode_button_color,
          groups=(groups or set()),
          behaviour=behaviour)

    def add_mode_button_control(self, mode_name, behaviour):
        colors = {}
        if self._enable_skinning:
            mode_color_basename = self._get_mode_color_base_name(mode_name)
            colors = {'mode_selected_color':'{}.On'.format(mode_color_basename), 
             'mode_unselected_color':'{}.Off'.format(mode_color_basename), 
             'mode_group_active_color':'{}.On'.format(mode_color_basename)}
        button_control = make_mode_button_control(self, mode_name, behaviour, **colors)
        self.add_control('{}_button'.format(mode_name), button_control)
        self._update_mode_buttons(self.selected_mode)

    def _get_mode_color_base_name(self, mode_name):
        return '{}.{}'.format(self.name, mode_name)

    def _update_mode_buttons(self, selected):
        super()._update_mode_buttons(selected)
        self.mode_selection_control.value = self._mode_list.index(selected) if selected in self._mode_list else 0