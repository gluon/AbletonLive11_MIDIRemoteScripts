from __future__ import absolute_import, print_function, unicode_literals
from base.util import as_ascii
from .. import NotifyingControlElement
from ..display import Content, updating_display

class DisplayLineElement(NotifyingControlElement):

    def __init__(self, display_fn=None, formatting_fn=lambda message: tuple(as_ascii(message))
, *a, **k):
        (super().__init__)(*a, **k)
        self._display_fn = display_fn
        self._formatting_fn = formatting_fn
        self._last_native_content = Content(None)

    def display_message(self, content):
        text = Content.from_object(content).value
        if updating_display:
            if self._last_native_content != content:
                self.grabbed or self._do_display(text)
                self._last_native_content = Content.from_object(content)
        else:
            self._do_display(text)

    def _do_display(self, message):
        self._display_fn(self._formatting_fn(message))

    @property
    def grabbed(self):
        return self.resource.stack_size > 1

    def reset(self):
        if self.grabbed:
            self._do_display('')
        else:
            self._redisplay_last_native_content()

    def _redisplay_last_native_content(self):
        if self._last_native_content != Content(None):
            self._do_display(self._last_native_content.value)