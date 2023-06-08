from __future__ import absolute_import, print_function, unicode_literals
from typing import Any, NamedTuple, Optional
import Live
from ableton.v3.base import depends, task
from ableton.v3.control_surface.mode import ImmediateBehaviour, LayerModeBase
from ableton.v3.control_surface.mode import ModesComponent as ModesComponentBase

def select_mode_for_main_view(main_view_name, can_select_now=True):
    return select_mode_on_event_change(EventDescription(subject=(Live.Application.get_application().view),
      event_name='focused_document_view',
      event_state=main_view_name),
      can_select_now=can_select_now)


def select_mode_on_event_change(event_description, can_select_now=False):
    subject = event_description.subject
    if callable(subject):
        subject = subject()

    def inner(modes_component, mode_name):

        def on_event_changed(*_):
            if event_description.event_state is None or getattr(subject, event_description.event_name) == event_description.event_state:
                modes_component.selected_mode = mode_name

        modes_component.register_slot(subject, on_event_changed, event_description.event_name)
        if can_select_now:
            if event_description.event_state is not None:
                on_event_changed()

    return inner


class EventDescription(NamedTuple):
    subject: Any
    event_name: str
    event_state = None
    event_state: Optional[Any]


class EnablingAddLayerMode(LayerModeBase):

    @depends(parent_task_group=None)
    def __init__(self, parent_task_group=None, *a, **k):
        (super().__init__)(*a, **k)
        self._should_track_layers = not isinstance(self._component, ModesComponent) and not hasattr(self._component, 'disable_layer_tracking') and hasattr(self._component, 'num_layers')
        if self._should_track_layers:
            self._possibly_disable_component_task = parent_task_group.add(task.run(self._possibly_disable_component))
            self._possibly_disable_component_task.kill()

    def enter_mode(self):
        component = self._get_component()
        self._layer.grab(component)
        if self._should_track_layers:
            component.num_layers += 1
        if not component.is_enabled():
            component.set_enabled(True)

    def leave_mode(self):
        component = self._get_component()
        self._layer.release(component)
        if self._should_track_layers:
            component.num_layers -= 1
            self._possibly_disable_component_task.restart()

    def _possibly_disable_component(self):
        component = self._get_component()
        if not component.num_layers:
            component.set_enabled(False)


class ModesComponent(ModesComponentBase):
    default_behaviour = ImmediateBehaviour()

    def __init__(self, default_behaviour=None, *a, **k):
        (super().__init__)(*a, **k)
        if default_behaviour is not None:
            self.default_behaviour = default_behaviour

    def add_mode(self, name, mode_or_component, selector=None, *a, **k):
        (super().add_mode)(name, mode_or_component, *a, **k)
        if callable(selector):
            selector(self, name)