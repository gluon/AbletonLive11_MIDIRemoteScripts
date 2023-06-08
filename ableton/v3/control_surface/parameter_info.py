from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface import ParameterInfo as ParameterInfoBase
from ..base import liveobj_valid

class ParameterInfo(ParameterInfoBase):

    def __init__(self, parameter=None, name=None, *a, **k):
        (super().__init__)(a, parameter=parameter, name=name, **k)
        if liveobj_valid(parameter):
            if name is not None:
                parameter.display_name = name