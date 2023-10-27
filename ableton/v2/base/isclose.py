# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v2\base\isclose.py
# Compiled at: 2022-11-28 08:01:31
# Size of source mod 2**32: 2257 bytes
from __future__ import absolute_import, print_function, unicode_literals
import math

def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    if a == b:
        return True
    if rel_tol < 0.0 or abs_tol < 0.0:
        raise ValueError('error tolerances must be non-negative')
    if math.isinf(abs(a)) or math.isinf(abs(b)):
        return False
    diff = abs(b - a)
    return diff <= abs(rel_tol * b) or diff <= abs(rel_tol * a) or diff <= abs_tol