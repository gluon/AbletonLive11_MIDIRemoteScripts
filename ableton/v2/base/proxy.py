# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v2\base\proxy.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 3352 bytes
from __future__ import absolute_import, print_function, unicode_literals
from .util import BooleanContext, old_hasattr

class ProxyBase(object):
    _skip_wrapper_lookup = None

    def __init__(self, *a, **k):
        (super(ProxyBase, self).__init__)(*a, **k)
        self._skip_wrapper_lookup = BooleanContext()

    def proxy_old_hasattr(self, attr):
        with self._skip_wrapper_lookup():
            return old_hasattr(self, attr)

    def __getattr__(self, name):
        if not self._skip_wrapper_lookup:
            obj = self.proxied_object
            interface = self.proxied_interface
            if obj:
                if old_hasattr(interface, name):
                    return getattr(obj, name)
            if interface:
                if old_hasattr(interface, name):
                    return getattr(interface, name)
        raise AttributeError('Does not have attribute %s' % name)

    def __setattr__(self, name, value):
        obj = self.proxied_object
        interface = self.proxied_interface
        if obj and old_hasattr(interface, name):
            if self.proxy_old_hasattr(name):
                raise AttributeError('Ambiguous set attribute: %s proxied: %s' % (name, obj))
            setattr(obj, name, value)
        else:
            if old_hasattr(interface, name):
                raise AttributeError('Ambiguous set attribute: %s proxied: %s' % (name, obj))
            self.__dict__[name] = value

    @property
    def proxied_object(self):
        pass

    @property
    def proxied_interface(self):
        obj = self.proxied_object
        return getattr(obj, 'proxied_interface', obj)


class Proxy(ProxyBase):
    proxied_object = None
    _proxied_interface = None

    @property
    def proxied_interface(self):
        return self._proxied_interface or super(Proxy, self).proxied_interface

    def __init__(self, proxied_object=None, proxied_interface=None, *a, **k):
        (super(Proxy, self).__init__)(*a, **k)
        self.proxied_object = proxied_object
        self._proxied_interface = proxied_interface