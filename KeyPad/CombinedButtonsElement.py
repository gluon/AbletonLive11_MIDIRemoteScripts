from __future__ import absolute_import, print_function, unicode_literals
from _Framework.ButtonElement import OFF_VALUE
import _Framework.ButtonMatrixElement as ButtonMatrixElement
from _Framework.Util import BooleanContext, const

class CombinedButtonsElement(ButtonMatrixElement):

    def __init__(self, buttons=None, *a, **k):
        (super(CombinedButtonsElement, self).__init__)(a, rows=[buttons], **k)
        self._is_pressed = BooleanContext(False)

    def is_momentary(self):
        return True

    def is_pressed(self):
        return any(map(lambda b__: b__[0].is_pressed() if b__[0] is not None else False
, self.iterbuttons())) or bool(self._is_pressed)

    def on_nested_control_element_value(self, value, sender):
        with self._is_pressed():
            self.notify_value(value)
        if value != OFF_VALUE:
            if not getattr(sender, 'is_momentary', const(False))():
                self.notify_value(OFF_VALUE)

    def send_value(self, value):
        for button, _ in self.iterbuttons():
            if button:
                button.send_value(value)

    def set_light(self, value):
        for button, _ in self.iterbuttons():
            if button:
                button.set_light(value)