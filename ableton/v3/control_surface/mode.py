from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface import StackingResource
from ableton.v2.control_surface.mode import AddLayerMode, CompoundMode, EnablingMode, ImmediateBehaviour, LatchingBehaviour, LayerMode, LayerModeBase, Mode, ModeButtonBehaviour, ModeButtonControl, MomentaryBehaviour, _ModeEntry, make_mode_button_control, tomode
from ..base import listenable_property, mixin
from . import Component
from .controls import ButtonControl, SendValueInputControl
__all__ = ('AddLayerMode', 'CompoundMode', 'EnablingMode', 'ImmediateBehaviour', 'LatchingBehaviour',
           'LayerMode', 'LayerModeBase', 'Mode', 'ModeButtonControl', 'ModeButtonBehaviour',
           'ModesComponent', 'MomentaryBehaviour', 'ReenterBehaviourMixin', 'make_mode_button_control',
           'make_reenter_behaviour')

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


class ModesComponent(Component):
    mode_selection_control = SendValueInputControl()
    cycle_mode_button = ButtonControl()
    default_behaviour = LatchingBehaviour()

    def __init__(self, name=None, support_momentary_mode_cycling=True, is_private=False, *a, **k):
        (super().__init__)(a, name=name, is_private=is_private, **k)
        self._support_momentary_mode_cycling = support_momentary_mode_cycling
        self._last_toggle_value = 0
        self._mode_toggle = None
        self._mode_list = []
        self._mode_map = {}
        self._last_selected_mode = None
        self._mode_stack = StackingResource(self._do_enter_mode, self._do_leave_mode)

    def disconnect(self):
        self._mode_stack.release_all()
        super().disconnect()

    @property
    def modes(self):
        return self._mode_list

    @property
    def active_modes(self):
        return self._mode_stack.clients

    @listenable_property
    def selected_mode(self):
        return self._mode_stack.owner or self._last_selected_mode

    @selected_mode.setter
    def selected_mode(self, mode):
        if self.is_enabled():
            if self.selected_mode != mode:
                if mode is not None:
                    self.push_mode(mode)
                    self.pop_unselected_modes()
                else:
                    self._mode_stack.release_all()
        else:
            self._last_selected_mode = mode

    def get_mode(self, name):
        entry = self._mode_map.get(name, None)
        return entry and entry.mode

    def get_mode_button(self, name):
        return getattr(self, '%s_button' % name)

    def get_mode_groups(self, name):
        entry = self._mode_map.get(name, None)
        if entry:
            return entry.groups
        return set()

    def push_mode(self, mode):
        self._mode_stack.grab(mode)

    def pop_mode(self, mode):
        self._mode_stack.release(mode)

    def pop_unselected_modes(self):
        self._mode_stack.release_stacked()

    def pop_groups(self, groups):
        if not isinstance(groups, set):
            groups = set(groups)
        for client in self._mode_stack.clients:
            if self.get_mode_groups(client) & groups:
                self._mode_stack.release(client)

    def cycle_mode(self, delta=1):
        current_index = self._mode_list.index(self.selected_mode) if self.selected_mode else -delta
        current_index = (current_index + delta) % len(self._mode_list)
        self.selected_mode = self._mode_list[current_index]

    def add_mode(self, name, mode_or_component, groups=None, behaviour=None):
        if not isinstance(groups, set):
            groups = set(groups) if groups is not None else set()
        mode = tomode(mode_or_component)
        behaviour = behaviour or self.default_behaviour
        self._mode_list.append(name)
        self._mode_map[name] = _ModeEntry(mode=mode,
          cycle_mode_button_color=('{}.On'.format(self._get_mode_color_base_name(name))),
          behaviour=behaviour,
          groups=groups)
        self.add_mode_button_control(name, behaviour)

    def add_mode_button_control(self, mode_name, behaviour):
        mode_color_basename = self._get_mode_color_base_name(mode_name)
        colors = {'mode_selected_color':'{}.On'.format(mode_color_basename), 
         'mode_unselected_color':'{}.Off'.format(mode_color_basename), 
         'mode_group_active_color':'{}.On'.format(mode_color_basename)}
        button_control = make_mode_button_control(self, mode_name, behaviour, **colors)
        self.add_control('{}_button'.format(mode_name), button_control)
        self._update_mode_buttons(self.selected_mode)

    @mode_selection_control.value
    def mode_selection_control(self, value, _):
        modes = self.modes
        if value < len(modes):
            self.selected_mode = modes[value]

    @cycle_mode_button.pressed
    def cycle_mode_button(self, _):
        if self._mode_list:
            self.cycle_mode(1)

    @cycle_mode_button.released_delayed
    def cycle_mode_button(self, _):
        if self._mode_list:
            if self._support_momentary_mode_cycling:
                self.cycle_mode(-1)

    def _do_enter_mode(self, name):
        entry = self._mode_map[name]
        entry.mode.enter_mode()
        self._update_mode_buttons(name)
        self._update_cycle_mode_button(name)
        self.notify_selected_mode(name)

    def _do_leave_mode(self, name):
        self._mode_map[name].mode.leave_mode()
        if self._mode_stack.stack_size == 0:
            self._update_mode_buttons(None)
            self._update_cycle_mode_button(None)
            self.notify_selected_mode(None)

    def _get_mode_behaviour(self, name):
        entry = self._mode_map.get(name, None)
        if entry is not None:
            return entry.behaviour
        return self.default_behaviour

    def _get_mode_color_base_name(self, mode_name):
        return '{}.{}'.format(self.name.title().replace('_', ''), mode_name.title().replace('_', ''))

    def on_enabled_changed(self):
        super().on_enabled_changed()
        if not self.is_enabled():
            self._last_selected_mode = self.selected_mode
            self._mode_stack.release_all()
        else:
            if self._last_selected_mode:
                self.push_mode(self._last_selected_mode)

    def _update_mode_buttons(self, selected):
        if self.is_enabled():
            for name in self._mode_map:
                self._get_mode_behaviour(name).update_button(self, name, selected)

        if selected in self._mode_list:
            self.mode_selection_control.value = self._mode_list.index(selected)

    def _update_cycle_mode_button(self, selected):
        entry = self._mode_map.get(selected)
        color = entry.cycle_mode_button_color if entry else None
        if color is not None:
            self.cycle_mode_button.color = color