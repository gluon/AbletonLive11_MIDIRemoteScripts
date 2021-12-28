#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v2/control_surface/profile.py
u"""
Provides facilities to ease the profiling of Control Surfaces.
"""
from __future__ import absolute_import, print_function, unicode_literals
from functools import wraps, partial
ENABLE_PROFILING = False
if ENABLE_PROFILING:
    import cProfile
    PROFILER = cProfile.Profile()

def profile(fn):
    u"""
    Decorator to mark a function to be profiled.
    """
    if ENABLE_PROFILING:

        @wraps(fn)
        def wrapper(self, *a, **k):
            if PROFILER:
                return PROFILER.runcall(partial(fn, self, *a, **k))
            else:
                print(u'Can not profile (%s), it is probably reloaded' % fn.__name__)
                return fn(*a, **k)

        return wrapper
    else:
        return fn


def dump(name = u'default'):
    u"""
    Dumps profiling data to the working directory with the given `name`. Three files
    are created:
    
    1. [name].profile contains the profile data in pstats format.
    2. [name].profile.time.txt contains the data in human readable form, sorted
       by *total time* - i.e. how much time has been spent in each function itself,
       without counting the time spent in sub-functions.
    3. [name].profile.cumulative.txt contains the data sorted by cumulative time - i.e.
       how much time is spent in a function and its sub-calls.
    """
    assert ENABLE_PROFILING
    import pstats
    fname = name + u'.profile'
    PROFILER.dump_stats(fname)

    def save_human_data(sort):
        s = pstats.Stats(fname, stream=open(u'%s.%s.txt' % (fname, sort), u'w'))
        s.sort_stats(sort)
        s.print_stats()

    save_human_data(u'time')
    save_human_data(u'cumulative')
