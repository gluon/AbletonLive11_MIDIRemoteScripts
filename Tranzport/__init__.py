from __future__ import absolute_import, print_function, unicode_literals
from .Tranzport import Tranzport

def create_instance(c_instance):
    return Tranzport(c_instance)


def exit_instance():
    pass