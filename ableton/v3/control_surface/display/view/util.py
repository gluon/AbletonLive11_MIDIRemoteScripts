# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\display\view\util.py
# Compiled at: 2023-06-08 07:52:37
# Size of source mod 2**32: 560 bytes
from __future__ import absolute_import, print_function, unicode_literals
from typing import List, Optional
from ..state import State

def suppress_notifications(state: State, exclude: Optional[List[str]]=None):
    if exclude is None:
        exclude = []
    for notification in getattr(state, '_notifications', set()) - set(exclude):
        setattr(state, notification, None)