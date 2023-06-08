from __future__ import absolute_import, print_function, unicode_literals
from future.builtins import range
import gc
from collections import defaultdict
from .util import old_hasattr

def typename(obj):
    if old_hasattr(obj, '__class__'):
        return obj.__class__.__name__
    if old_hasattr(obj, '__name__'):
        return obj.__name__
    return '<unknown>'


def histogram(name_filter=None, objs=None):
    all_ = gc.get_objects() if objs is None else objs

    def _name_filter(name):
        return name_filter is None or name_filter in name

    hist = defaultdict(lambda: 0
)
    for o in all_:
        n = typename(o)
        if _name_filter(n):
            hist[n] += 1

    return hist


def instances_by_name(name_filter):
    return [o for o in gc.get_objects() if name_filter == typename(o)]


def refget(objs, level=1):
    for _ in range(level):
        refs = (gc.get_referrers)(*objs)
        try:
            refs.remove(objs)
        except ValueError:
            pass

        objs = refs

    return refs