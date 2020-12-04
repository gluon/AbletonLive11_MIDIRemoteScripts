#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Push/notification_component.py
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
BLANK_BLOCK = u' ' * DISPLAY_BLOCK_LENGTH

def adjust_arguments(format_string, original_arguments):
    adjusted_arguments = list(original_arguments)
    matches = re.finditer(FORMAT_SPECIFIER_WITH_MARKUP_PATTERN, format_string)
    for index, match in enumerate(matches):
        has_markup = match.group(1)
        original_format_specifier = match.group(3)
        if has_markup is not None:
            desired_length = int(match.group(2))
            original_argument = original_arguments[index]
            if original_format_specifier != u's':
                if original_format_specifier.find(u'*') != -1:
                    raise ValueError(u'Format specifiers using * for field width/precision are not supported')
                original_argument = (u'%' + original_format_specifier) % original_argument
            adjusted_arguments[index] = adjust_string(original_argument, desired_length)

    return tuple(adjusted_arguments)


def apply_formatting(text_spec):
    u"""
    Take a format string with arguments and format it. If given a plain string, just
    returns it.
    
    In addition to the normal format specifiers offered by the % operator, this function
    also supports special markup to specify a desired length for a sub string.
    The markup is basically an extended format specifier:
    
        %len=DESIRED_LENGTH,FORMAT_SPECIFIER
    
    FORMAT_SPECIFIER is everything you would normally specify after the % sign
    when using format strings. It can be as complicated as a normal format specifier,
    e.g. `-08d` or similar. If FORMAT_SPECIFIER is anything except `s`, the argument
    will first be converted to a string using FORMAT_SPECIFIER, and then the length
    adjustment is applied.
    
    NOTE: The * versions of field width and precision, e.g. %.*f, are not supported with
    the extended markup, and the function will raise a ValueError when trying to use them.
    
    DESIRED_LENGTH is used as argument to `adjust_string` when applying the length
    adjustment.
    """
    if isinstance(text_spec, tuple):
        format_string = text_spec[0]
        original_arguments = text_spec[1:]
        adjusted_arguments = adjust_arguments(format_string, original_arguments)
        format_string = re.sub(FORMAT_SPECIFIER_WITH_MARKUP_PATTERN, u'%s', format_string)
        return format_string % adjusted_arguments
    else:
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

    def __init__(self, token = None, callback = None, *a, **k):
        super(_CallbackControl, self).__init__(*a, **k)
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
    u"""
    Displays notifications to the user for a given amount of time. A notification time
    of -1 creates an infinite duration notification.
    
    To adjust the way notifications are shown in special cases, assign a generated
    control using use_single_line or use_full_display to a layer. If the layer is on
    top, it will set the preferred view.
    This will show the notification on line 1 if my_component is enabled and
    the priority premise of the layer is met:
    
        my_component.layer = Layer(
            _notification = notification_component.use_single_line(1))
    """
    _default_align_text_fn = partial(maybe(partial(align_none, DISPLAY_LENGTH)))

    def __init__(self, default_notification_time = 2.5, blinking_time = 0.3, display_lines = [], *a, **k):
        super(NotificationComponent, self).__init__(*a, **k)
        self._display_lines = get_element(display_lines)
        self._token_control = _TokenControlElement()
        self._align_text_fn = self._default_align_text_fn
        self._message_box = MessageBoxComponent(parent=self)
        self._message_box.set_enabled(False)
        self._default_notification_time = default_notification_time
        self._blinking_time = blinking_time
        self._original_text = None
        self._blink_text = None
        self._blink_text_task = self._tasks.add(task.loop(task.sequence(task.run(lambda : self._message_box.__setattr__(u'text', self._original_text)), task.wait(self._blinking_time), task.run(lambda : self._message_box.__setattr__(u'text', self._blink_text)), task.wait(self._blinking_time)))).kill()

    message_box_layer = forward_property(u'_message_box')(u'layer')

    def show_notification(self, text, blink_text = None, notification_time = None):
        u"""
        Triggers a notification with the given text.
        If text is a tuple, it will treat it as a format string + arguments.
        """
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
        u"""
        Hides the current notification, if any existing.
        """
        self._blink_text_task.kill()
        self._message_box.set_enabled(False)

    def use_single_line(self, line_index, line_slice = None, align = align_none):
        u"""
        Returns a control, that will change the notification to a single line view,
        if it is grabbed.
        """
        assert line_index >= 0 and line_index < len(self._display_lines)
        display = self._display_lines[line_index]
        if line_slice is not None:
            display = display.subdisplay[line_slice]
        layer = Layer(priority=MESSAGE_BOX_PRIORITY, display_line1=display)
        return _CallbackControl(self._token_control, partial(self._set_message_box_layout, layer, maybe(partial(align, display.width))))

    def use_full_display(self, message_line_index = 2):
        u"""
        Returns a control, that will change the notification to use the whole display,
        if it is grabbed.
        """
        layer = Layer(priority=MESSAGE_BOX_PRIORITY, **dict([ (u'display_line1' if i == message_line_index else u'bg%d' % i, line) for i, line in enumerate(self._display_lines) ]))
        return _CallbackControl(self._token_control, partial(self._set_message_box_layout, layer))

    def _set_message_box_layout(self, layer, align_text_fn = None):
        self._message_box.layer = layer
        self._align_text_fn = partial(align_text_fn or self._default_align_text_fn)

    def _create_tasks(self, notification_time):
        duration = notification_time if notification_time is not None else self._default_notification_time
        self._notification_timeout_task = self._tasks.add(task.sequence(task.wait(duration), task.run(self.hide_notification))).kill() if duration != -1 else self._tasks.add(task.Task())
