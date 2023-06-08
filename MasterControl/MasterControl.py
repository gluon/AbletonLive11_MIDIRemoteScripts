from __future__ import absolute_import, print_function, unicode_literals
import MackieControl.MackieControl as MackieControl

class MasterControl(MackieControl):

    def __init__(self, c_instance):
        MackieControl.__init__(self, c_instance)