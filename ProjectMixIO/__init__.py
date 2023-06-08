from __future__ import absolute_import, print_function, unicode_literals
from .ProjectMixIO import ProjectMixIO

def create_instance(c_instance):
    return ProjectMixIO(c_instance)