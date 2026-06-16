# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_MxDCore\__init__.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 2312 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import str
from future.utils import string_types
import sys, warnings
from ableton.v2.base import old_hasattr
from .MxDCore import MxDCore as _MxDCore

def set_manager(manager):
    _MxDCore.instance = _MxDCore()
    _MxDCore.instance.set_manager(manager)


def disconnect():
    _MxDCore.instance.disconnect()
    del _MxDCore.instance


def execute_command(device_id, object_id, command, arguments):
    if old_hasattr(_MxDCore.instance, command):
        try:
            with warnings.catch_warnings(record=True) as caught_warnings:
                _MxDCore.instance.update_device_context(device_id, object_id)
                function = getattr(_MxDCore.instance, command)
                function(device_id, object_id, arguments)
                for warning in caught_warnings:
                    _MxDCore.instance._print_warning(device_id, object_id, str(warning.message))

        except:
            if sys.exc_info()[0].__name__ == 'RuntimeError':
                assert_reason = str(sys.exc_info()[1])
            else:
                assert_reason = 'Invalid syntax'
            _MxDCore.instance._print_error(device_id, object_id, assert_reason)

    else:
        _MxDCore.instance._print_error(device_id, object_id, 'Unknown command: ' + command)