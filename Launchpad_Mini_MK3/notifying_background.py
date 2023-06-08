from __future__ import absolute_import, print_function, unicode_literals
from functools import partial
from ableton.v2.base import nop
from ableton.v2.control_surface.components import BackgroundComponent
from ableton.v2.control_surface.elements import ButtonMatrixElement

class NotifyingBackgroundComponent(BackgroundComponent):
    __events__ = ('value', )

    def register_slot(self, control, *a):
        listener = nop if isinstance(control, ButtonMatrixElement) else partial(self._NotifyingBackgroundComponent__on_control_value, control)
        return super(BackgroundComponent, self).register_slot(control, listener, 'value')

    def __on_control_value(self, control, value):
        self.notify_value(control, value)