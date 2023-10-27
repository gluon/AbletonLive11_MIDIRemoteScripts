# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push\notification_component.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 9698 bytes
from __future__ import absolute_import, print_function, unicode_literals
import re
from functools import partial
from weakref import ref
from ableton.v2.base import forward_property, maybe, task
from ableton.v2.control_surface import Component, CompoundElement, ControlElement, Layer, get_element
from ableton.v2.control_surface.elements import adjust_string
from pushbase.consts import DISPLAY_LENGTH, MESSAGE_BOX_PRIORITY
from pushbase.message_box_component import FORMAT_SPECIFIER_WITH_MARKUP_PATTERN, MessageBoxComponent, Notification
from .special_physical_display import DISPLAY_BLOCK_LENGTH
BLANK_BLOCK = ' ' * DISPLAY_BLOCK_LENGTH

def adjust_arguments(format_string, original_arguments):
    adjusted_arguments = list(original_arguments)
    matches = re.finditer(FORMAT_SPECIFIER_WITH_MARKUP_PATTERN, format_string)
    for index, match in enumerate(matches):
        has_markup = match.group(1)
        original_format_specifier = match.group(3)
        if has_markup is not None:
            desired_length = int(match.group(2))
            original_argument = original_arguments[index]
            if original_format_specifier != 's':
                if original_format_specifier.find('*') != -1:
                    raise ValueError('Format specifiers using * for field width/precision are not supported')
                else:
                    original_argument = ('%' + original_format_specifier) % original_argument
            else:
                adjusted_arguments[index] = adjust_string(original_argument, desired_length)

    return tuple(adjusted_arguments)


def apply_formatting(text_spec):
    if isinstance(text_spec, tuple):
        format_string = text_spec[0]
        original_arguments = text_spec[1:]
        adjusted_arguments = adjust_arguments(format_string, original_arguments)
        format_string = re.sub(FORMAT_SPECIFIER_WITH_MARKUP_PATTERN, '%s', format_string)
        return format_string % adjusted_arguments
    return text_spec


def align_none(width, text):
    return text


def align_left(width, text):
    while text.startswith(BLANK_BLOCK):
        text = text[DISPLAY_BLOCK_LENGTH:]

    return text


def align_right(width, text):
    text = text.ljust(width)
    while text.endswith(BLANK_BLOCK):
        text = BLANK_BLOCK + text[:1 - DISPLAY_BLOCK_LENGTH]

    return text


class _CallbackControl(CompoundElement):
    _is_resource_based = True

    def __init__(self, token=None, callback=None, *a, **k):
        (super(_CallbackControl, self).__init__)(*a, **k)
        self._callback = callback
        self.register_control_element(token)

    def on_nested_control_element_received(self, control):
        self._callback()

    def on_nested_control_element_lost(self, control):
        pass


class _TokenControlElement(ControlElement):

    def reset(self):
        pass


class NotificationComponent(Component):
    _default_align_text_fn = partial(maybe(partial(align_none, DISPLAY_LENGTH)))

    def __init__(self, default_notification_time=2.5, blinking_time=0.3, display_lines=[], *a, **k):
        (super(NotificationComponent, self).__init__)(*a, **k)
        self._display_lines = get_element(display_lines)
        self._token_control = _TokenControlElement()
        self._align_text_fn = self._default_align_text_fn
        self._message_box = MessageBoxComponent(parent=self)
        self._message_box.set_enabled(False)
        self._default_notification_time = default_notification_time
        self._blinking_time = blinking_time
        self._original_text = None
        self._blink_text = None
        self._blink_text_task = self._tasks.add(task.loop(task.sequence(task.run(lambda: self._message_box.__setattr__('text', self._original_text)
), task.wait(self._blinking_time), task.run(lambda: self._message_box.__setattr__('text', self._blink_text)
), task.wait(self._blinking_time)))).kill()

    message_box_layer = forward_property('_message_box')('layer')

    def show_notification(self, text, blink_text=None, notification_time=None):
        self._create_tasks(notification_time)
        text = apply_formatting(text)
        text = self._align_text_fn(text)
        blink_text = self._align_text_fn(blink_text)
        if blink_text is not None:
            self._original_text = text
            self._blink_text = blink_text
            self._blink_text_task.restart()
        self._message_box.text = text
        self._message_box.set_enabled(True)
        self._notification_timeout_task.restart()
        self._current_notification = Notification(self)
        return ref(self._current_notification)

    def hide_notification(self):
        self._blink_text_task.kill()
        self._message_box.set_enabled(False)

    def use_single_line(self, line_index, line_slice=None, align=align_none):
        display = self._display_lines[line_index]
        if line_slice is not None:
            display = display.subdisplay[line_slice]
        layer = Layer(priority=MESSAGE_BOX_PRIORITY, display_line1=display)
        return _CallbackControl(self._token_control, partial(self._set_message_box_layout, layer, maybe(partial(align, display.width))))

    def use_full_display(self, message_line_index=2):
        layer = Layer(priority=MESSAGE_BOX_PRIORITY, **dict([('display_line1' if i == message_line_index else 'bg%d' % i, line) for i, line in enumerate(self._display_lines)]))
        return _CallbackControl(self._token_control, partial(self._set_message_box_layout, layer))

    def _set_message_box_layout(self, layer, align_text_fn=None):
        self._message_box.layer = layer
        self._align_text_fn = partial(align_text_fn or self._default_align_text_fn)

    def _create_tasks(self, notification_time):
        duration = notification_time if notification_time is not None else self._default_notification_time
        self._notification_timeout_task = self._tasks.add(task.sequence(task.wait(duration), task.run(self.hide_notification))).kill() if duration != -1 else self._tasks.add(task.Task())