from __future__ import absolute_import, print_function, unicode_literals
from ...base import CompoundDisconnectable, EventObject, EventObjectMeta, const, depends, lazy_attribute, nop
from .renderable_state import RenderableState

def collect_properties(cls):
    return (name for name, _ in EventObjectMeta.collect_listenable_properties(cls.__dict__))


class Renderable(CompoundDisconnectable):

    @depends(render_and_update_display=(const(None)))
    def __init__(self, render_and_update_display=None, *a, **k):
        (super().__init__)(*a, **k)
        self._render_and_update_display = render_and_update_display or nop

    @lazy_attribute
    def renderable_state(self):
        renderable_state = RenderableState()
        if isinstance(self, EventObject):
            for property_name in collect_properties(self.__class__):
                setattr(renderable_state, property_name, getattr(self, property_name))
                self.register_slot(self, self._create_event_handler(property_name), property_name)

        if hasattr(self, 'name'):
            renderable_state.name = self.name.lower()
        return renderable_state

    def _create_event_handler(self, property_name):

        def on_event(*_):
            setattr(self.renderable_state, property_name, getattr(self, property_name))
            self._render_and_update_display()

        return on_event