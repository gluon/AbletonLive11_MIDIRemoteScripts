from __future__ import absolute_import, print_function, unicode_literals
from .MackieControlXT import MackieControlXT

def create_instance(c_instance):
    return MackieControlXT(c_instance)