from __future__ import absolute_import, print_function, unicode_literals
from .Axiom import Axiom

def create_instance(c_instance):
    return Axiom(c_instance)