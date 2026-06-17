# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\display\display_specification.py
# Compiled at: 2023-10-06 16:19:02
# Size of source mod 2**32: 8342 bytes
from __future__ import absolute_import, print_function, unicode_literals
import sys
from contextlib import contextmanager
from io import StringIO
from typing import Callable, Optional, Type
from ...base import Disconnectable, const, inject
from .notifications import DefaultNotifications, Notifications
from .renderable import Renderable
from .state import State
from .type_decl import DISCONNECT_EVENT, INIT_EVENT
from .util import updating_display
from .view import View

class DisplaySpecification:

    def __init__(self, create_root_view: Optional[Callable[([], View)]]=None, protocol=None, notifications: Optional[Type[Notifications]]=None):
        self.create_root_view = create_root_view
        self.protocol = protocol
        self.notifications = notifications or DefaultNotifications


class Display(Disconnectable):

    def __init__(self, specification: DisplaySpecification, renderable_components, elements):
        self._react_fns = []
        with inject(register_react_fn=(const(self._react_fns.append))).everywhere():
            self._root_view = specification.create_root_view()
        self._display_protocol = specification.protocol
        self._display_fn = None
        self._initialized = False
        self._last_displayed_content = None
        self._is_deferring_render_and_update = False
        self._was_updated_in_deferred_context = False
        self._exception_raised = False
        self._suppress_stdout_from_render = True
        self._state = State()
        for component in renderable_components:
            if component.include_in_top_level_state:
                setattr(self._state, component.name.lower(), component.renderable_state)

        self._state.elements = State()
        for name, element in vars(elements).items():
            if isinstance(element, Renderable):
                setattr(self._state.elements, name, element.renderable_state)

        self._display_fn = self._display_protocol(elements)
        self._initialized = True
        self.react(INIT_EVENT)

    @property
    def state(self):
        return self._state

    def react(self, event):
        if self._initialized:
            for fn in self._react_fns:
                fn(self._state, event)

            self._suppress_stdout_from_render = False
            self.render_and_update_display()

    def render(self):
        return self._root_view(self._state)

    def display(self, content):
        with updating_display():
            self._display_fn(content)

    def render_and_update_display(self):
        try:
            if self._is_deferring_render_and_update:
                self._was_updated_in_deferred_context = True
            else:
                if self._display_fn:
                    captured_stdout = StringIO()
                    with capturing_stdout(captured_stdout):
                        content = self.render()
                    if content != self._last_displayed_content:
                        self.display(content)
                        self._last_displayed_content = content
                        self._suppress_stdout_from_render = False
                    if not self._suppress_stdout_from_render:
                        last_output = captured_stdout.getvalue()
                        if last_output:
                            print(last_output)
                        self._suppress_stdout_from_render = True
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

    @property
    def rendered_content(self):
        return self._last_displayed_content

    def disconnect(self):
        self.react(DISCONNECT_EVENT)

    def clear_content_cache(self):
        self._last_displayed_content = None


@contextmanager
def capturing_stdout(temp_output_stream):
    original_stdout = sys.stdout
    sys.stdout = temp_output_stream
    try:
        yield
    finally:
        sys.stdout = original_stdout