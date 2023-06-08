from __future__ import absolute_import, print_function, unicode_literals
import Live
from .OpenLabs import OpenLabs

def create_instance(c_instance):
    return OpenLabs(c_instance)