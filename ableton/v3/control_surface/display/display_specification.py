from __future__ import absolute_import, print_function, unicode_literals
from contextlib import contextmanager
from ...base import Disconnectable
from .renderable_state import RenderableState
from .util import Content, updating_display

class DisplaySpecification(Disconnectable):

    def __init__(self, render, protocol=None):
        self._render = render
        self._display_protocol = protocol
        self._display_fn = None
        self._last_displayed_content = None
        self._is_deferring_render_and_update = False
        self._was_updated_in_deferred_context = False
        self._exception_raised = False

    def initialize(self, renderable_components, elements):
        self._state = RenderableState()
        for component_state in (c.renderable_state for c in renderable_components):
            setattr(self._state, component_state.name, component_state)

        self._state.connected = True
        self._display_fn = self._display_protocol(elements)

    def render(self, state=None, from_test=False):
        return self._render(state or self._state)

    def display(self, content):
        with updating_display():
            self._display_fn(content.value if isinstance(content, Content) else content)

    def render_and_update_display(self):
        try:
            if self._is_deferring_render_and_update:
                self._was_updated_in_deferred_context = True
            else:
                if self._display_fn:
                    content = self.render()
                    if content != self._last_displayed_content:
                        self.display(content)
                        self._last_displayed_content = content
        except Exception as e:
            try:
                exception_already_raised = self._exception_raised
                self._exception_raised = True
                if not exception_already_raised:
                    raise e
            finally:
                e = None
                del e

    @contextmanager
    def deferring_render_and_update_display(self):
        self._is_deferring_render_and_update = True
        self._was_updated_in_deferred_context = False
        try:
            yield
        finally:
            self._is_deferring_render_and_update = False
            if self._was_updated_in_deferred_context:
                self.render_and_update_display()

    def disconnect(self):
        self._state.connected = False
        self.render_and_update_display()