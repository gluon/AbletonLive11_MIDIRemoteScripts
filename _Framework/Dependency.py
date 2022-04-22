# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/_Framework/Dependency.py
# Compiled at: 2022-01-27 16:28:16
# Size of source mod 2**32: 5363 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import object, str
__all__ = ('inject', 'depends', 'dependency')
from functools import wraps
from .Util import union

class DependencyError(Exception):
    pass


class InjectionRegistry(object):

    def __init__(self, parent=None, *a, **k):
        (super(InjectionRegistry, self).__init__)(*a, **k)
        self._key_registry = {}

    def register_key(self, key, injector):
        self._key_registry.setdefault(key, []).append(injector)

    def unregister_key(self, key, injector):
        self._key_registry[key].remove(injector)
        if not self._key_registry[key]:
            del self._key_registry[key]

    def get(self, key, default=None):
        try:
            return self._key_registry[key][(-1)].provides[key]
        except KeyError:
            return default


_global_injection_registry = InjectionRegistry()

def get_dependency_for(obj, name, default=None):
    accessor = _global_injection_registry.get(name, default)
    if accessor is not None:
        return accessor()
    raise DependencyError('Required dependency %s not provided for %s' % (name, str(obj)))


class dependency(object):

    def __init__(self, **k):
        self._dependency_name, self._dependency_default = list(k.items())[0]

    def __get__(self, obj, cls=None):
        if obj is None:
            obj = cls
        return get_dependency_for(obj, self._dependency_name, self._dependency_default)


def depends(**dependencies):

    def decorator(func):

        @wraps(func)
        def wrapper(self, *a, **explicit):
            deps = dict([(k, get_dependency_for(self, k, v)) for k, v in dependencies.items() if k not in explicit])
            return func(self, *a, **union(deps, explicit))

        return wrapper

    return decorator


class Injector(object):

    @property
    def provides(self):
        return {}

    def register(self):
        pass

    def unregister(self):
        pass

    def __enter__(self):
        self.register()
        return self

    def __exit__(self, *a):
        self.unregister()


class RegistryInjector(Injector):

    def __init__(self, provides=None, registry=None, *a, **k):
        (super(Injector, self).__init__)(*a, **k)
        self._provides_dict = provides
        self._registry = registry

    @property
    def provides(self):
        return self._provides_dict

    def register(self):
        registry = self._registry
        for k in self._provides_dict:
            registry.register_key(k, self)

    def unregister(self):
        registry = self._registry
        for k in self._provides_dict:
            registry.unregister_key(k, self)


class InjectionFactory(object):

    def __init__(self, provides=None, *a, **k):
        (super(InjectionFactory, self).__init__)(*a, **k)
        self._provides_dict = provides

    def everywhere(self):
        return RegistryInjector(provides=(self._provides_dict),
          registry=_global_injection_registry)

    into_object = NotImplemented
    into_class = NotImplemented


def inject(**k):
    return InjectionFactory(k)