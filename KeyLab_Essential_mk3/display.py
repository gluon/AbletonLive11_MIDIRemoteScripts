# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\KeyLab_Essential_mk3\display.py
# Compiled at: 2023-10-06 16:19:02
# Size of source mod 2**32: 6404 bytes
from __future__ import absolute_import, print_function, unicode_literals
from dataclasses import dataclass
from enum import Enum
from functools import partial
from typing import Optional, Tuple, Union
from ableton.v3.control_surface.display import DefaultNotifications, DisplaySpecification, Text, view
from ableton.v3.live import display_name, is_arrangement_view_active, is_track_armed, liveobj_name, song
Line1Text = partial(Text, max_width=11, justification=(Text.Justification.NONE))
Line2Text = partial(Text, max_width=20, justification=(Text.Justification.NONE))

class IconType(Enum):
    NONE = 0
    LIVE = 71
    MIXER = 63
    ARM = 66
    DOWN_ARROW = 57
    UP_ARROW = 58
    LEFT_ARROW = 59
    RIGHT_ARROW = 60


class IconState(Enum):
    UNFRAMED = 0
    CLOSED = 1
    OPENED = 2
    FRAMED = 3


@dataclass
class Icon:
    type = IconType.NONE
    type: IconType
    state = IconState.UNFRAMED
    state: IconState


Lines = Tuple[(str, str)]
Header = str
Footer = Tuple[(Icon, Icon, Icon, Icon)]
Popup = Union[(str, Lines)]

@dataclass
class Frame:
    header: Header
    footer: Footer


@dataclass
class Content:
    primary = None
    primary: Optional[Lines]
    primary_icon = IconType.NONE
    primary_icon: Optional[IconType]
    frame = None
    frame: Optional[Frame]
    popup = None
    popup: Optional[Popup]
    parameters = (None, None, None, None, None, None, None, None, None, None, None,
                  None, None, None, None, None, None, None)
    parameters: Tuple[(Optional[Lines], ...)]


class Notifications(DefaultNotifications):
    identify = lambda: Content(primary=('Connected', ''), primary_icon=(IconType.LIVE))

    class Transport(DefaultNotifications.Transport):
        tap_tempo = lambda tempo: Content(popup=('Tap Tempo', str(int(tempo))))


def create_root_view() -> view.View[Optional[Content]]:

    @view.View
    def main_view(state) -> Optional[Content]:
        return Content(primary=(
         liveobj_name(state.target_track.target_track),
         display_name(song().view.selected_scene)),
          parameters=(tuple(((element.parameter_name, element.parameter_value) if element.parameter_name else None for element in state.elements.continuous_controls + [
         state.elements.encoder_9, state.elements.fader_9]))),
          frame=Frame(header=(view_based_content('Session', 'Arrangement')),
          footer=(
         Icon(IconType.MIXER, IconState.OPENED if state.continuous_control_modes.selected_mode == 'mixer' else IconState.CLOSED),
         Icon(IconType.ARM, IconState.FRAMED if is_track_armed(state.target_track.target_track) else IconState.UNFRAMED),
         Icon(view_based_content(IconType.LEFT_ARROW, IconType.UP_ARROW)),
         Icon(view_based_content(IconType.RIGHT_ARROW, IconType.DOWN_ARROW)))),
          popup=None if (state.continuous_control_modes.previous_mode is None) and not (state.device_bank_navigation.has_changed_bank_index) else (('Device control', 'Page 1' if state.device_bank_navigation.bank_index == 0 else 'Page 2') if state.continuous_control_modes.selected_mode == 'device' else (
         'Tracks control',
         'Page 1' if state.mixer_session_ring.offset[0] == 0 else 'Page 2')))

    return view.CompoundView(view.DisconnectedView(), view.NotificationView(lambda _, content: content
), main_view)


def view_based_content(session_content, arrangement_content):
    if is_arrangement_view_active():
        return arrangement_content
    return session_content


def protocol(elements):

    def display(content):
        if content:
            display_primary_content(content.primary, content.primary_icon)
            display_frame(content.frame)
            display_popup(content.popup)
            display_parameters(content.parameters)

    def display_primary_content(text, icon):
        if text:
            with elements.display_full_screen_command.deferring_send():
                elements.display_line_1.display_message(text[0])
                elements.display_line_2.display_message(text[1])
                elements.display_full_screen_command.send_value(screen_id=(26 if icon.value else 18),
                  line3=(icon.value))

    def display_frame(frame):
        if frame:
            elements.display_header_command.send_value(Text(frame.header).as_ascii())
            (elements.display_footer_command.send_value)(*frame.footer)

    def display_popup(popup):
        if popup:
            line1, line2 = (popup, None) if isinstance(popup, str) else popup
            elements.display_popup_command.send_value(line1=(Text(line1).as_ascii()),
              line2=(Text(line2).as_ascii() if line2 else None))

    def display_parameters(parameters):
        for command, parameter in list(list(zip(elements.display_parameter_commands, parameters))):
            if parameter:
                command.send_value(32, Line1Text(parameter[0]).as_ascii(), Line2Text(parameter[1]).as_ascii())
            else:
                command.send_value(33)

    return display


display_specification = DisplaySpecification(create_root_view=create_root_view,
  protocol=protocol,
  notifications=Notifications)