<<<<<<< HEAD
=======
# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v2/base/gcutil.py
# Compiled at: 2022-01-27 16:28:17
# Size of source mod 2**32: 1837 bytes
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
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

<<<<<<< HEAD
    hist = defaultdict(lambda: 0
)
=======
    hist = defaultdict(lambda: 0)
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
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