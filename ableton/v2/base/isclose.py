# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v2/base/isclose.py
# Compiled at: 2021-06-29 09:33:48
# Size of source mod 2**32: 2204 bytes
from __future__ import absolute_import, print_function, unicode_literals
import math

def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    if a == b:
        return True
    if rel_tol < 0.0 or (abs_tol < 0.0):
        raise ValueError('error tolerances must be non-negative')
    if math.isinf(abs(a)) or (math.isinf(abs(b))):
        return False
    diff = abs(b - a)
    return diff <= abs(rel_tol * b) or diff <= abs(rel_tol * a) or diff <= abs_tol