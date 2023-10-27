# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\APC64\display.py
# Compiled at: 2023-10-06 16:19:02
# Size of source mod 2**32: 5005 bytes
from __future__ import absolute_import, print_function, unicode_literals
from dataclasses import dataclass
from math import floor
from typing import Optional, Tuple
from ableton.v3.control_surface.display import DefaultNotifications, DisplaySpecification, Text, view
from ableton.v3.live import display_name, liveobj_name, parameter_owner, song
from .colors import SimpleColor, make_color_for_liveobj
CONTROL_SURFACE_DISPLAY_PAD_MODES = [
 'session', 'session_overview', 'drum']

@dataclass
class Content:
    header_color: SimpleColor
    lines: Optional[Tuple[(str, str, str)]]


class Notifications(DefaultNotifications):
    controlled_range = DefaultNotifications.DefaultText()
    generic = DefaultNotifications.DefaultText()

    class Transport(DefaultNotifications.Transport):
        metronome = DefaultNotifications.DefaultText()
        record_quantize = DefaultNotifications.DefaultText()

    class Track(DefaultNotifications.Track):
        select = 'default_lines'

    class Device(DefaultNotifications.Device):
        select = 'default_lines'
        bank = 'default_lines'


def get_active_parameter--- This code section failed: ---

 L.  49         0  LOAD_FAST                'state'
                2  LOAD_ATTR                active_parameter
                4  LOAD_ATTR                parameter
                6  JUMP_IF_TRUE_OR_POP    32  'to 32'

 L.  51         8  LOAD_FAST                'state'
               10  LOAD_ATTR                encoder_modes
               12  LOAD_ATTR                selected_mode
               14  LOAD_CONST               ('fixed_length', 'quantize')
               16  COMPARE_OP               in
               18  POP_JUMP_IF_FALSE    30  'to 30'
               20  LOAD_FAST                'state'
               22  LOAD_ATTR                elements
               24  LOAD_ATTR                encoder
               26  LOAD_ATTR                mapped_object
               28  RETURN_VALUE     
             30_0  COME_FROM            18  '18'

 L.  52        30  LOAD_CONST               None
             32_0  COME_FROM             6  '6'
               32  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 32_0


def get_default_lines(state):
    return (
     liveobj_name(state.target_track.target_track),
     liveobj_name(state.device.device) or '-',
     state.device.bank_name or '-')


def format_notification(state, notification_text):
    if notification_text == 'default_lines':
        lines = get_default_lines(state)
    else:
        if 'ERROR' in notification_text or 'INFO' in notification_text:
            lines = [Text(t, max_width=(Text.ContentWidth())) for t in notification_text.split('\n')]
        else:
            text = notification_text.split('\n')
            lines = ('', Text((text[0]), max_width=(Text.ContentWidth())), text[1].title())
    return Content(header_color=(make_color_for_liveobj(state.target_track.target_track)),
      lines=(tuple(lines)))


def create_root_view() -> view.View[Optional[Content]]:

    @view.View
    def main_view(state) -> Optional[Content]:
        active_parameter = get_active_parameter(state)
        return Content(header_color=(make_color_for_liveobj(state.target_track.target_track)),
          lines=(('', 'Tempo', '{} BPM'.format(floor(song().tempo))) if (getattr(parameter_owner(active_parameter), 'name', ''), Text((display_name(active_parameter)), max_width=(Text.ContentWidth() if display_name(active_parameter) in ('Fixed Length',
                                                                                                            'Quantization') else None)), str(active_parameter)) if active_parameter else state.encoder_modes.selected_mode == 'tempo' else get_default_lines(state) if state.pad_modes.selected_mode in CONTROL_SURFACE_DISPLAY_PAD_MODES else None))

    return view.CompoundView(view.DisconnectedView(render_condition=(lambda state: not state.identification.is_identified or not state.connected or state.encoder_modes.selected_mode == 'swing'
)), view.NotificationView(format_notification,
      suppressing_signals=(
     lambda state, _: get_active_parameter(state) is not None or state.elements.tempo_button.is_pressed
,),
      render_condition=(lambda state, notification: notification != 'default_lines' or state.pad_modes.selected_mode not in CONTROL_SURFACE_DISPLAY_PAD_MODES
),
      supports_new_line=True), main_view)


def protocol(elements):

    def display(content):
        if content:
            elements.track_color_element.set_light(content.header_color)
        if content and content.lines:
            elements.display_ownership_command.send_value(1)
            elements.display_line_1.display_message(content.lines[0])
            elements.display_line_2.display_message(content.lines[1])
            elements.display_line_3.display_message(content.lines[2])
        else:
            elements.display_ownership_command.send_value(0)

    return display


display_specification = DisplaySpecification(create_root_view=create_root_view,
  protocol=protocol,
  notifications=Notifications)