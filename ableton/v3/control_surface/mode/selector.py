# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\mode\selector.py
# Compiled at: 2023-09-22 14:37:57
# Size of source mod 2**32: 3641 bytes
from __future__ import absolute_import, print_function, unicode_literals
from typing import Any, NamedTuple, Optional
import Live
from . import pop_last_mode

def select_mode_for_main_view(main_view_name, can_select_now=True):
    return select_mode_on_event_change(EventDescription(subject=(Live.Application.get_application().view),
      event_name='focused_document_view',
      event_state=main_view_name),
      can_select_now=can_select_now)


def select_mode_on_event_change(event_description, can_select_now=False):
    subject = _get_subject(event_description.subject)
    event_name = event_description.event_name
    event_state = event_description.event_state

    def inner(modes_component, mode_name):

        def on_event_changed(*_):
            if event_state is None or getattr(subject, event_name) == event_state:
                modes_component.selected_mode = mode_name

        modes_component.register_slot(subject, on_event_changed, event_name)
        if can_select_now:
            if event_state is not None:
                on_event_changed()

    return inner


def toggle_mode_on_property_change(event_description, return_to_default=False, can_select_now=False):
    subject = _get_subject(event_description.subject)
    event_name = event_description.event_name

    def inner(modes_component, mode_name):

        def on_property_changed(state=None):
            if bool(state or getattr(subject, event_name)):
                modes_component.push_mode(mode_name)
            else:
                if return_to_default and modes_component.selected_mode == mode_name:
                    modes_component.push_mode(modes_component.modes[0])
                    modes_component.pop_unselected_modes()
                else:
                    pop_last_mode(modes_component, mode_name)

        modes_component.register_slot(subject, on_property_changed, event_name)
        if can_select_now:
            on_property_changed(getattr(subject, event_name))

    return inner


def _get_subject(subject):
    if callable(subject):
        return subject()
    return subject


class EventDescription(NamedTuple):
    subject: Any
    event_name: str
    event_state = None
    event_state: Optional[Any]