from __future__ import absolute_import, print_function, unicode_literals
from ableton.v3.base import as_ascii, task
from ableton.v3.control_surface import NotifyingControlElement
from ableton.v3.control_surface.elements import adjust_string
MAX_CENTER_DISPLAY_LENGTH = 18

class SimpleDisplayElement(NotifyingControlElement):

    def __init__(self, header, tail, *a, **k):
        (super().__init__)(*a, **k)
        self._message_header = header
        self._message_tail = tail
        self._message_to_send = None
        self._last_sent_message = None
        self._send_message_task = self._tasks.add(task.run(self._send_message))
        self._send_message_task.kill()

    def display_message(self, message):
        if message:
            is_reset_message = message == ' '
            self._message_to_send = self._message_header + tuple(as_ascii(' ' if is_reset_message else adjust_string(message, MAX_CENTER_DISPLAY_LENGTH).strip())) + self._message_tail
            self._request_send_message()

    def update(self):
        self._last_sent_message = None
        self._request_send_message()

    def clear_send_cache(self):
        self._last_sent_message = None
        self._request_send_message()

    def reset(self):
        self.display_message(' ')

    def send_midi(self, message):
        if message != self._last_sent_message:
            NotifyingControlElement.send_midi(self, message)
            self._last_sent_message = message

    def _request_send_message(self):
        self._send_message_task.restart()

    def _send_message(self):
        if self._message_to_send:
            self.send_midi(self._message_to_send)