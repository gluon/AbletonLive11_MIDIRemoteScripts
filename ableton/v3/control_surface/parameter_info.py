# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\parameter_info.py
# Compiled at: 2023-10-06 16:19:02
# Size of source mod 2**32: 978 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface import ParameterInfo as ParameterInfoBase
from ..live import liveobj_valid

class ParameterInfo(ParameterInfoBase):

    def __init__(self, parameter=None, name=None, *a, **k):
        (super().__init__)(a, parameter=parameter, name=name, **k)
        if liveobj_valid(parameter):
            if name is not None:
                parameter.display_name = name

    @property
    def original_name(self):
        if liveobj_valid(self.parameter):
            return self.parameter.original_name
        return ''