from __future__ import absolute_import, print_function, unicode_literals
from .FireOne import FireOne

def create_instance(c_instance):
    return FireOne(c_instance)