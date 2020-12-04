#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ATOMSQ/simple_display.py
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import task
from ableton.v2.control_surface import NotifyingControlElement
from ableton.v2.control_surface.elements import adjust_string
QUESTION_MARK = 63
MAX_CENTER_DISPLAY_LENGTH = 18

def as_ascii(message):
    result = []
    for char in message:
        ascii = ord(char)
        if ascii > 127:
            ascii = QUESTION_MARK
        result.append(ascii)

    return tuple(result)


class SimpleDisplayElement(NotifyingControlElement):

    def __init__(self, header, tail, *a, **k):
        super(SimpleDisplayElement, self).__init__(*a, **k)
        self._message_header = header
        self._message_tail = tail
        self._message_to_send = None
        self._last_sent_message = None
        self._send_message_task = self._tasks.add(task.run(self._send_message))
        self._send_message_task.kill()

    def display_message(self, message):
        if message:
            is_reset_message = message == u' '
            self._message_to_send = self._message_header + as_ascii(u' ' if is_reset_message else adjust_string(message, MAX_CENTER_DISPLAY_LENGTH).strip()) + self._message_tail
            self._request_send_message()

    def update(self):
        self._last_sent_message = None
        self._request_send_message()

    def clear_send_cache(self):
        self._last_sent_message = None
        self._request_send_message()

    def reset(self):
        self.display_message(u' ')

    def send_midi(self, midi_bytes):
        if midi_bytes != self._last_sent_message:
            NotifyingControlElement.send_midi(self, midi_bytes)
            self._last_sent_message = midi_bytes

    def _request_send_message(self):
        self._send_message_task.restart()

    def _send_message(self):
        if self._message_to_send:
            self.send_midi(self._message_to_send)
