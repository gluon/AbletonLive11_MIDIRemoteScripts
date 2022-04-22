# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/_Framework/DisplayDataSource.py
# Compiled at: 2022-01-27 16:28:16
# Size of source mod 2**32: 3548 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import object
from functools import partial

def adjust_string_crop(original, length):
    length = int(length)
    return original[:length].ljust(length)


def adjust_string(original, length):
    length = int(length)
    resulting_string = original
    if len(resulting_string) > length:
        unit_db = resulting_string.endswith('dB') and resulting_string.find('.') != -1
        if len(resulting_string.strip()) > length:
            if unit_db:
                resulting_string = resulting_string[:-2]
        if len(resulting_string) > length:
            for char in (' ', '_', 'i', 'o', 'u', 'e', 'a'):
                offset = 0 if char == ' ' else 1
                while len(resulting_string) > length:
                    if resulting_string.rfind(char, offset) > 0:
                        char_pos = resulting_string.rfind(char, offset)
                        resulting_string = resulting_string[:char_pos] + resulting_string[char_pos + 1:]

            resulting_string = resulting_string[:length]
    if len(resulting_string) < length:
        resulting_string = resulting_string.ljust(length)
    return resulting_string


class DisplayDataSource(object):
    _separator = ''
    _adjust_string_fn = partial(adjust_string)

    def __init__(self, display_string='', separator=None, adjust_string_fn=adjust_string, *a, **k):
        (super(DisplayDataSource, self).__init__)(*a, **k)
        if adjust_string_fn is not None:
            self._adjust_string_fn = partial(adjust_string_fn)
        if separator is not None:
            self._separator = separator
        self._display_string = display_string
        self._update_callback = None
        self._in_update = False

    def _get_separator(self):
        return self._separator

    def _set_separator(self, separator):
        if separator != self._separator:
            self._separator = separator
            self.update()

    separator = property(_get_separator, _set_separator)

    def set_update_callback(self, update_callback):
        self._update_callback = update_callback
        if update_callback:
            self.update()

    def set_display_string(self, new_string):
        if self._display_string != new_string:
            self._display_string = new_string
            self.update()

    def clear(self):
        self.set_display_string('')
        self.separator = ''

    def update(self):
        self._in_update = True
        if self._update_callback != None:
            self._update_callback()
        self._in_update = False

    def display_string(self):
        return self._display_string

    def adjust_string(self, width):
        return self._adjust_string_fn(self.display_string(), width)