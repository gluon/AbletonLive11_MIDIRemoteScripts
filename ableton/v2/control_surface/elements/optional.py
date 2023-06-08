from __future__ import absolute_import, print_function, unicode_literals
from ...base import listens
from .combo import ToggleElement

class ChoosingElement(ToggleElement):

    def __init__(self, flag=None, *a, **k):
        (super(ChoosingElement, self).__init__)(*a, **k)
        self._ChoosingElement__on_flag_changed.subject = flag
        self._ChoosingElement__on_flag_changed(flag.value)

    @listens('value')
    def __on_flag_changed(self, value):
        self.set_toggled(value)


class OptionalElement(ChoosingElement):

    def __init__(self, control=None, flag=None, value=None, *a, **k):
        on_control = control if value else None
        off_control = None if value else control
        (super(OptionalElement, self).__init__)(a, on_control=on_control, off_control=off_control, flag=flag, **k)