from __future__ import absolute_import, print_function, unicode_literals
import _Framework.ControlSurfaceComponent as ControlSurfaceComponent

def _disable_control(control):
    for button in control:
        button.set_enabled(False)


class UserMatrixComponent(ControlSurfaceComponent):

    def __getattr__(self, name):
        if len(name) > 4:
            if name[:4] == 'set_':
                return _disable_control
        raise AttributeError(name)