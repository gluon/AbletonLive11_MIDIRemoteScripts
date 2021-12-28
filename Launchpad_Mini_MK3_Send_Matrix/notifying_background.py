from __future__ import absolute_import, print_function, unicode_literals
from functools import partial
from ableton.v2.control_surface.components import BackgroundComponent


class NotifyingBackgroundComponent(BackgroundComponent):
    __events__ = ("value",)

    def register_slot(self, control, *a):
        super(BackgroundComponent, self).register_slot(
            control, partial(self.__on_control_value, control), "value"
        )

    def __on_control_value(self, control, value):
        self.notify_value(control, value)
