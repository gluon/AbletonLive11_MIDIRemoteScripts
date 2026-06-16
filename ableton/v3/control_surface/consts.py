# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\consts.py
# Compiled at: 2023-06-08 07:52:37
# Size of source mod 2**32: 807 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface import DEFAULT_PRIORITY
LOW_PRIORITY = DEFAULT_PRIORITY - 1
HIGH_PRIORITY = DEFAULT_PRIORITY + 1
M4L_PRIORITY = HIGH_PRIORITY + 1
MOMENTARY_DELAY = 0.3
ACTIVE_PARAMETER_TIMEOUT = 0.75