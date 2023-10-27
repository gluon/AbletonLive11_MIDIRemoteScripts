# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\display\view\notification.py
# Compiled at: 2023-08-04 12:30:20
# Size of source mod 2**32: 4792 bytes
from __future__ import absolute_import, print_function, unicode_literals
from math import inf
from typing import Any, Callable, Generic, Optional, Tuple
from uuid import uuid1
from ..event_signal import EventSignalFn, on_notification
from ..state import State
from ..type_decl import INIT_EVENT, ContentType, Event
from .type_decl import NotificationDataType, RenderNotification
from .util import suppress_notifications
from .view import View
DEFAULT_NOTIFICATION_DURATION: float = 2.0

class NotificationView(View[ContentType], Generic[(ContentType, NotificationDataType)]):

    def __init__(self, render_fn: RenderNotification[(Any, ContentType)], render_condition: Callable[([State], bool)]=lambda *_: True
, notification_signal: EventSignalFn[NotificationDataType]=on_notification(), name: str='notification', duration: Optional[float]=None, exclusive: bool=True, suppressing_signals: Tuple[(EventSignalFn[NotificationDataType], ...)]=tuple(), supports_new_line: bool=False):
        self._render = render_fn
        self._render_condition = render_condition
        self._notification_signal = notification_signal
        self._name = name
        self._duration = duration
        self._exclusive = exclusive
        self._suppressing_signals = suppressing_signals
        self._supports_new_line = supports_new_line

    def init(self, state: State):
        if not hasattr(state, '_notifications'):
            setattr(state, '_notifications', set())
        if self._name in getattr(state, '_notifications'):
            self._name += str(uuid1())
        getattr(state, '_notifications').add(self._name)
        self.reset_state(state)

    def reset_state(self, state: State, delay: Optional[float]=None):
        state.set_delayed(self._name, None, delay)

    def react(self, state: State, event: Event):
        if event is INIT_EVENT:
            self.init(state)
        notification_data = self._notification_signal(state, event)
        if notification_data:
            setattr(state, self._name, notification_data)
            if self._exclusive:
                suppress_notifications(state, exclude=[self._name])
            if self._duration != inf:
                self.reset_state(state,
                  delay=(self._duration if self._duration else DEFAULT_NOTIFICATION_DURATION))
        else:
            if any((suppressing_signal(state, event) for suppressing_signal in self._suppressing_signals)):
                self.reset_state(state)
        return state

    def render(self, state: State):
        notification_data = getattr(state, self._name)
        if not (self._supports_new_line or isinstance(notification_data, str)):
            return self._render(state, notification_data)
        return self._render(state, notification_data.replace('\n', ' '))

    def render_condition(self, state: State) -> bool:
        notification_data = getattr(state, self._name)
        return notification_data is not None and self._render_condition(state, notification_data)

    def content_condition(self, content) -> bool:
        return True