from __future__ import absolute_import, print_function, unicode_literals
from .MasterControl import MasterControl

def create_instance(c_instance):
    return MasterControl(c_instance)