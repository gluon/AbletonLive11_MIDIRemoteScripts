from __future__ import absolute_import, print_function, unicode_literals
from _Framework.Control import ButtonControl
import _Framework.ControlSurfaceComponent as ControlSurfaceComponent

class LedLightingComponent(ControlSurfaceComponent):
    button = ButtonControl(color='Misc.Shift', pressed_color='Misc.ShiftOn')