# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\display\notifications\util.py
# Compiled at: 2023-08-04 12:30:20
# Size of source mod 2**32: 619 bytes
from __future__ import absolute_import, annotations, print_function, unicode_literals
from typing import TYPE_CHECKING, Callable
if TYPE_CHECKING:
    from typing_extensions import LiteralString
else:
    LiteralString = str

def toggle_text_generator(format_string: 'LiteralString') -> 'Callable[[bool], str]':

    def notification_fn(is_on):
        return format_string.format('on' if is_on else 'off')

    return notification_fn