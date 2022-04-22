# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/_Framework/ModesComponent.py
# Compiled at: 2022-01-27 16:28:16
# Size of source mod 2**32: 28051 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import map, object
from functools import partial
from ableton.v2.base import old_hasattr
from . import Defaults, Task
from .CompoundComponent import CompoundComponent
from .ControlSurfaceComponent import ControlSurfaceComponent
from .Dependency import depends
from .Layer import LayerBase
from .Resource import StackingResource
from .SubjectSlot import subject_slot
from .Util import NamedTuple, infinite_context_manager, is_contextmanager, is_iterable, lazy_attribute

def tomode(thing):
    if thing == None:
        return Mode()
    if isinstance(thing, Mode):
        return thing
    if isinstance(thing, ControlSurfaceComponent):
        return ComponentMode(thing)
    if isinstance(thing, tuple):
        if len(thing) == 2:
            if isinstance(thing[0], ControlSurfaceComponent):
                if isinstance(thing[1], LayerBase):
                    return LayerMode(*thing)
            if callable(thing[0]):
                if callable(thing[1]):
                    mode = Mode()
                    mode.enter_mode, mode.leave_mode = thing
                    return mode
    if is_iterable(thing):
        return CompoundMode(*thing)
    if is_contextmanager(thing):
        return ContextManagerMode(thing)
    if callable(thing):
        mode = Mode()
        mode.enter_mode = thing
        return mode
    return thing


class Mode(object):

    def enter_mode(self):
        pass

    def leave_mode(self):
        pass

    def __enter__(self):
        self.enter_mode()

    def __exit__(self, *a):
        return self.leave_mode()


class ContextManagerMode(Mode):

    def __init__(self, context_manager=None, *a, **k):
        (super(ContextManagerMode, self).__init__)(*a, **k)
        self._context_manager = context_manager

    def enter_mode(self):
        self._context_manager.__enter__()

    def leave_mode(self):
        self._context_manager.__exit__(None, None, None)

    def __exit__(self, exc_type, exc_value, traceback):
        return self._context_manager.__exit__(exc_type, exc_value, traceback)


def generator_mode(function):
    makecontext = infinite_context_manager(function)
    return lambda *a, **k: ContextManagerMode(makecontext(*a, **k))


class ComponentMode(Mode):

    def __init__(self, component=None, *a, **k):
        (super(ComponentMode, self).__init__)(*a, **k)
        self._component = component

    def enter_mode(self):
        self._component.set_enabled(True)

    def leave_mode(self):
        self._component.set_enabled(False)


class LazyComponentMode(Mode):

    def __init__(self, component_creator=None, *a, **k):
        (super(LazyComponentMode, self).__init__)(*a, **k)
        self._component_creator = component_creator

    @lazy_attribute
    def component(self):
        return self._component_creator()

    def enter_mode(self):
        self.component.set_enabled(True)

    def leave_mode(self):
        self.component.set_enabled(False)


class DisableMode(Mode):

    def __init__(self, component=None, *a, **k):
        (super(DisableMode, self).__init__)(*a, **k)
        self._component = component

    def enter_mode(self):
        self._component.set_enabled(False)

    def leave_mode(self):
        self._component.set_enabled(True)


class LayerModeBase(Mode):

    def __init__(self, component=None, layer=None, *a, **k):
        (super(LayerModeBase, self).__init__)(*a, **k)
        self._component = component
        self._layer = layer

    def _get_component(self):
        if callable(self._component):
            return self._component()
        return self._component


class LayerMode(LayerModeBase):

    def enter_mode(self):
        self._get_component().layer = self._layer

    def leave_mode(self):
        self._get_component().layer = None


class AddLayerMode(LayerModeBase):

    def enter_mode(self):
        self._layer.grab(self._get_component())

    def leave_mode(self):
        self._layer.release(self._get_component())


class CompoundMode(Mode):

    def __init__(self, *modes, **k):
        (super(CompoundMode, self).__init__)(**k)
        self._modes = list(map(tomode, modes))

    def enter_mode(self):
        for mode in self._modes:
            mode.enter_mode()

    def leave_mode(self):
        for mode in reversed(self._modes):
            mode.leave_mode()


class MultiEntryMode(Mode):

    def __init__(self, mode=None, *a, **k):
        (super(MultiEntryMode, self).__init__)(*a, **k)
        self._mode = tomode(mode)
        self._entry_count = 0

    def enter_mode(self):
        if self._entry_count == 0:
            self._mode.enter_mode()
        self._entry_count += 1

    def leave_mode(self):
        if self._entry_count == 1:
            self._mode.leave_mode()
        self._entry_count -= 1

    @property
    def is_entered(self):
        return self._entry_count > 0


class SetAttributeMode(Mode):

    def __init__(self, obj=None, attribute=None, value=None, *a, **k):
        (super(SetAttributeMode, self).__init__)(*a, **k)
        self._obj = obj
        self._attribute = attribute
        self._old_value = None
        self._value = value

    def _get_object(self):
        if callable(self._obj):
            return self._obj()
        return self._obj

    def enter_mode(self):
        self._old_value = getattr(self._get_object(), self._attribute, None)
        setattr(self._get_object(), self._attribute, self._value)

    def leave_mode(self):
        if getattr(self._get_object(), self._attribute) == self._value:
            setattr(self._get_object(), self._attribute, self._old_value)


class DelayMode(Mode):

    @depends(parent_task_group=None)
    def __init__(self, mode=None, delay=None, parent_task_group=None, *a, **k):
        (super(DelayMode, self).__init__)(*a, **k)
        delay = delay if delay is not None else Defaults.MOMENTARY_DELAY
        self._mode = tomode(mode)
        self._mode_entered = False
        self._delay_task = parent_task_group.add(Task.sequence(Task.wait(delay), Task.run(self._enter_mode_delayed)))
        self._delay_task.kill()

    def _enter_mode_delayed(self):
        self._mode_entered = True
        self._mode.enter_mode()

    def enter_mode(self):
        self._delay_task.restart()

    def leave_mode(self):
        if self._mode_entered:
            self._mode.leave_mode()
            self._mode_entered = False
        self._delay_task.kill()


class ModeButtonBehaviour(object):

    def press_immediate(self, component, mode):
        pass

    def release_immediate(self, component, mode):
        pass

    def press_delayed(self, component, mode):
        pass

    def release_delayed(self, component, mode):
        pass

    def update_button(self, component, mode, selected_mode):
        button = component.get_mode_button(mode)
        groups = component.get_mode_groups(mode)
        selected_groups = component.get_mode_groups(selected_mode)
        button.set_light(mode == selected_mode or bool(groups & selected_groups))


class LatchingBehaviour(ModeButtonBehaviour):

    def press_immediate(self, component, mode):
        component.push_mode(mode)

    def release_immediate(self, component, mode):
        component.pop_unselected_modes()

    def release_delayed(self, component, mode):
        if len(component.active_modes) > 1:
            component.pop_mode(mode)


class ReenterBehaviour(LatchingBehaviour):

    def __init__(self, on_reenter=None, *a, **k):
        (super(ReenterBehaviour, self).__init__)(*a, **k)
        if on_reenter is not None:
            self.on_reenter = on_reenter

    def press_immediate(self, component, mode):
        was_active = component.selected_mode == mode
        super(ReenterBehaviour, self).press_immediate(component, mode)
        if was_active:
            self.on_reenter()

    def on_reenter(self):
        pass


class CancellableBehaviour(ModeButtonBehaviour):
    _previous_mode = None

    def press_immediate(self, component, mode):
        active_modes = component.active_modes
        groups = component.get_mode_groups(mode)
        can_cancel_mode = mode in active_modes or any(map(lambda other: groups & component.get_mode_groups(other), active_modes))
        if can_cancel_mode:
            if groups:
                component.pop_groups(groups)
            else:
                component.pop_mode(mode)
            self.restore_previous_mode(component)
        else:
            self.remember_previous_mode(component)
            component.push_mode(mode)

    def remember_previous_mode(self, component):
        self._previous_mode = component.active_modes[0] if component.active_modes else None

    def restore_previous_mode(self, component):
        if len(component.active_modes) == 0:
            if self._previous_mode != None:
                component.push_mode(self._previous_mode)


class ImmediateBehaviour(ModeButtonBehaviour):

    def press_immediate(self, component, mode):
        component.selected_mode = mode


class AlternativeBehaviour(CancellableBehaviour):

    def __init__(self, alternative_mode=None, *a, **k):
        (super(AlternativeBehaviour, self).__init__)(*a, **k)
        self._alternative_mode = alternative_mode

    def _check_mode_groups(self, component, mode):
        mode_groups = component.get_mode_groups(mode)
        alt_group = component.get_mode_groups(self._alternative_mode)
        return mode_groups and mode_groups & alt_group

    def release_delayed(self, component, mode):
        component.pop_groups(component.get_mode_groups(mode))
        self.restore_previous_mode(component)

    def press_delayed(self, component, mode):
        self.remember_previous_mode(component)
        component.push_mode(self._alternative_mode)

    def release_immediate(self, component, mode):
        super(AlternativeBehaviour, self).press_immediate(component, mode)

    def press_immediate(self, component, mode):
        pass


class DynamicBehaviourMixin(ModeButtonBehaviour):

    def __init__(self, mode_chooser=None, *a, **k):
        (super(DynamicBehaviourMixin, self).__init__)(*a, **k)
        self._mode_chooser = mode_chooser
        self._chosen_mode = None

    def press_immediate(self, component, mode):
        self._chosen_mode = self._mode_chooser() or mode
        super(DynamicBehaviourMixin, self).press_immediate(component, self._chosen_mode)

    def release_delayed(self, component, mode):
        super(DynamicBehaviourMixin, self).release_delayed(component, self._chosen_mode)

    def press_delayed(self, component, mode):
        super(DynamicBehaviourMixin, self).press_delayed(component, self._chosen_mode)

    def release_immediate(self, component, mode):
        super(DynamicBehaviourMixin, self).release_immediate(component, self._chosen_mode)


class ExcludingBehaviourMixin(ModeButtonBehaviour):

    def __init__(self, excluded_groups=set(), *a, **k):
        (super(ExcludingBehaviourMixin, self).__init__)(*a, **k)
        self._excluded_groups = set(excluded_groups)

    def is_excluded(self, component, selected):
        return bool(component.get_mode_groups(selected) & self._excluded_groups)

    def press_immediate(self, component, mode):
        if not self.is_excluded(component, component.selected_mode):
            super(ExcludingBehaviourMixin, self).press_immediate(component, mode)

    def release_delayed(self, component, mode):
        if not self.is_excluded(component, component.selected_mode):
            super(ExcludingBehaviourMixin, self).release_delayed(component, mode)

    def press_delayed(self, component, mode):
        if not self.is_excluded(component, component.selected_mode):
            super(ExcludingBehaviourMixin, self).press_delayed(component, mode)

    def release_immediate(self, component, mode):
        if not self.is_excluded(component, component.selected_mode):
            super(ExcludingBehaviourMixin, self).release_immediate(component, mode)

    def update_button(self, component, mode, selected_mode):
        if not self.is_excluded(component, selected_mode):
            super(ExcludingBehaviourMixin, self).update_button(component, mode, selected_mode)
        else:
            component.get_mode_button(mode).set_light('DefaultButton.Disabled')


class _ModeEntry(NamedTuple):
    mode = None
    groups = set()
    toggle_value = False
    subject_slot = None
    momentary_task = None


class ModesComponent(CompoundComponent):
    __subject_events__ = ('selected_mode', )
    momentary_toggle = False
    default_behaviour = LatchingBehaviour()

    def __init__(self, *a, **k):
        (super(ModesComponent, self).__init__)(*a, **k)
        self._last_toggle_value = 0
        self._mode_toggle = None
        self._mode_toggle_task = self._tasks.add(Task.wait(Defaults.MOMENTARY_DELAY))
        self._mode_toggle_task.kill()
        self._mode_list = []
        self._mode_map = {}
        self._last_selected_mode = None
        self._mode_stack = StackingResource(self._do_enter_mode, self._do_leave_mode)
        self._shift_button = None

    def disconnect(self):
        self._mode_stack.release_all()
        super(ModesComponent, self).disconnect()

    def set_shift_button(self, button):
        self._shift_button = button

    def _do_enter_mode(self, name):
        entry = self._mode_map[name]
        entry.mode.enter_mode()
        self._update_buttons(name)
        self.notify_selected_mode(name)

    def _do_leave_mode(self, name):
        self._mode_map[name].mode.leave_mode()
        if self._mode_stack.stack_size == 0:
            self._update_buttons(None)
            self.notify_selected_mode(None)

    def _get_selected_mode(self):
        return self._mode_stack.owner or self._last_selected_mode

    def _set_selected_mode(self, mode):
        if self.is_enabled():
            if mode != None:
                self.push_mode(mode)
                self.pop_unselected_modes()
            else:
                self._mode_stack.release_all()
        else:
            self._last_selected_mode = mode

    selected_mode = property(_get_selected_mode, _set_selected_mode)

    @property
    def selected_groups(self):
        entry = self._mode_map.get(self.selected_mode, None)
        if entry:
            return entry.groups
        return set()

    @property
    def active_modes(self):
        return self._mode_stack.clients

    def push_mode(self, mode):
        self._mode_stack.grab(mode)

    def pop_mode(self, mode):
        self._mode_stack.release(mode)

    def pop_groups(self, groups):
        if not isinstance(groups, set):
            groups = set(groups)
        for client in self._mode_stack.clients:
            if self.get_mode_groups(client) & groups:
                self._mode_stack.release(client)

    def pop_unselected_modes(self):
        self._mode_stack.release_stacked()

    def on_enabled_changed(self):
        super(ModesComponent, self).on_enabled_changed()
        if not self.is_enabled():
            self._last_selected_mode = self.selected_mode
            self._mode_stack.release_all()
        elif self._last_selected_mode:
            self.push_mode(self._last_selected_mode)

    def update(self):
        super(ModesComponent, self).update()
        self._update_buttons(self.selected_mode)

    def add_mode(self, name, mode_or_component, toggle_value=False, groups=set(), behaviour=None):
        if not isinstance(groups, set):
            groups = set(groups)
        mode = tomode(mode_or_component)
        task = self._tasks.add(Task.sequence(Task.wait(Defaults.MOMENTARY_DELAY), Task.run(lambda: self._get_mode_behaviour(name).press_delayed(self, name))))
        task.kill()
        slot = self.register_slot(listener=(partial(self._on_mode_button_value, name)),
          event='value',
          extra_kws=dict(identify_sender=True))
        self._mode_list.append(name)
        self._mode_map[name] = _ModeEntry(mode=mode,
          toggle_value=toggle_value,
          behaviour=behaviour,
          subject_slot=slot,
          momentary_task=task,
          groups=groups)
        button_setter = 'set_' + name + '_button'
        if not old_hasattr(self, button_setter):
            setattr(self, button_setter, partial(self.set_mode_button, name))

    def _get_mode_behaviour(self, name):
        entry = self._mode_map.get(name, None)
        return entry and (entry.behaviour) or (self.default_behaviour)

    def get_mode(self, name):
        entry = self._mode_map.get(name, None)
        return entry and entry.mode

    def get_mode_groups(self, name):
        entry = self._mode_map.get(name, None)
        if entry:
            return entry.groups
        return set()

    def set_toggle_button(self, button):
        if button:
            if self.is_enabled():
                button.reset()
        self._mode_toggle = button
        self._on_toggle_value.subject = button
        self._update_buttons(self.selected_mode)

    def set_mode_button(self, name, button):
        if button:
            if self.is_enabled():
                button.reset()
        self._mode_map[name].subject_slot.subject = button
        self._update_buttons(self.selected_mode)

    def get_mode_button(self, name):
        return self._mode_map[name].subject_slot.subject

    def _update_buttons(self, selected):
        if self.is_enabled():
            for name, entry in self._mode_map.items():
                if entry.subject_slot.subject != None:
                    self._get_mode_behaviour(name).update_button(self, name, selected)

            if self._mode_toggle:
                entry = self._mode_map.get(selected)
                value = entry and entry.toggle_value
                self._mode_toggle.set_light(value)

    def _on_mode_button_value(self, name, value, sender):
        shift = self._shift_button and self._shift_button.is_pressed()
        if not shift:
            if self.is_enabled():
                behaviour = self._get_mode_behaviour(name)
                if sender.is_momentary():
                    entry = self._mode_map[name]
                    task = entry.momentary_task
                    if value:
                        behaviour.press_immediate(self, name)
                        task.restart()
                    elif task.is_killed:
                        behaviour.release_delayed(self, name)
                    else:
                        behaviour.release_immediate(self, name)
                        task.kill()
                else:
                    behaviour.press_immediate(self, name)
                    behaviour.release_immediate(self, name)

    @subject_slot('value')
    def _on_toggle_value(self, value):
        shift = self._shift_button and self._shift_button.is_pressed()
        if not shift:
            if self.is_enabled():
                if len(self._mode_list):
                    is_press = value and not self._last_toggle_value
                    is_release = not value and self._last_toggle_value
                    can_latch = self._mode_toggle_task.is_killed and self.selected_mode != self._mode_list[0]
                    if not self._mode_toggle.is_momentary() or is_press:
                        self.cycle_mode(1)
                        self._mode_toggle_task.restart()
                    elif is_release:
                        if self.momentary_toggle or (can_latch):
                            self.cycle_mode(-1)
                    self._last_toggle_value = value

    def cycle_mode(self, delta=1):
        current_index = self._mode_list.index(self.selected_mode) if self.selected_mode else -delta
        current_index = (current_index + delta) % len(self._mode_list)
        self.selected_mode = self._mode_list[current_index]


class DisplayingModesComponent(ModesComponent):

    def __init__(self, *a, **k):
        (super(DisplayingModesComponent, self).__init__)(*a, **k)
        self._mode_data_sources = {}

    def add_mode(self, name, mode_or_component, data_source):
        super(DisplayingModesComponent, self).add_mode(name, mode_or_component)
        self._mode_data_sources[name] = (data_source, data_source.display_string())

    def update(self):
        super(DisplayingModesComponent, self).update()
        self._update_data_sources(self.selected_mode)

    def _do_enter_mode(self, name):
        super(DisplayingModesComponent, self)._do_enter_mode(name)
        self._update_data_sources(name)

    def _update_data_sources(self, selected):
        if self.is_enabled():
            for name, (source, string) in self._mode_data_sources.items():
                source.set_display_string('*' + string if name == selected else string)


class EnablingModesComponent(ModesComponent):

    def __init__(self, component=None, toggle_value=False, disabled_value=False, *a, **k):
        (super(EnablingModesComponent, self).__init__)(*a, **k)
        component.set_enabled(False)
        self.add_mode('disabled', None, disabled_value)
        self.add_mode('enabled', component, toggle_value)
        self.selected_mode = 'disabled'