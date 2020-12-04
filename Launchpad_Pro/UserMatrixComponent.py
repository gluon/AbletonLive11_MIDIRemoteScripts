#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Launchpad_Pro/UserMatrixComponent.py
from __future__ import absolute_import, print_function, unicode_literals
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent

def _disable_control(control):
    for button in control:
        button.set_enabled(False)


class UserMatrixComponent(ControlSurfaceComponent):
    u"""
    "Component" that expects ButtonMatrixElements that hold
    ConfigurableButtonElements, to then turn them off. This
    is done so the buttons' messages can be forwarded to Live's Tracks.
    """

    def __getattr__(self, name):
        if len(name) > 4 and name[:4] == u'set_':
            return _disable_control
        raise AttributeError(name)
