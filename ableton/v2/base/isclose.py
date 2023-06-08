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