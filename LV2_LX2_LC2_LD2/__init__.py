from __future__ import absolute_import, print_function, unicode_literals
import Live
from .LV2_LX2_LC2_LD2 import LV2_LX2_LC2_LD2

def create_instance(c_instance):
    return LV2_LX2_LC2_LD2(c_instance)