from __future__ import absolute_import, print_function, unicode_literals
import _Framework.SysexValueControl as SysexValueControl

class ButtonSysexControl(SysexValueControl):

    def set_light(self, value):
        pass

    def is_momentary(self):
        return False