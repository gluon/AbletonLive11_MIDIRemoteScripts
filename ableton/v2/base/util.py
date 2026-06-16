# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v2\base\util.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 24651 bytes
from __future__ import absolute_import, print_function, unicode_literals
from future.builtins import map, range
from future.moves.itertools import zip_longest
from future.utils import iteritems
import sys
from contextlib import contextmanager
from functools import partial, reduce, wraps
from itertools import chain
from math import ceil, floor
from numbers import Number
PY2 = sys.version_info[0] < 3
PY3 = sys.version_info[0] >= 3

def clamp(val, minv, maxv):
    return max(minv, min(val, maxv))


def linear(minv, maxv, val):
    return minv + (maxv - minv) * val


def nop(*a, **k):
    if a:
        return a[0]


def negate(value):
    return not value


def old_round(value):
    if round(value + 1) - round(value) != 1:
        return value + abs(value) / value * 0.5
    return round(value)


def const(value):
    return lambda *a, **k: value


def in_range(value, lower_bound, upper_open_bound):
    if not isinstance(value, Number):
        return False
    return value >= lower_bound and value < upper_open_bound


def sign(value):
    if value >= 0.0:
        return 1.0
    return -1.0


def to_slice(obj):
    if isinstance(obj, slice):
        return obj
    if obj != -1:
        return slice(obj, obj + 1)
    return slice(obj, None)


def slice_size(slice, width):
    return len(range(width)[slice])


def chunks(lst, chunk_size):
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]


def maybe(fn):
    return lambda x: fn(x) if x is not None else None


def memoize(function):
    memoized = {}

    @wraps(function)
    def wrapper(*args):
        try:
            ret = memoized[args]
        except KeyError:
            ret = memoized[args] = function(*args)

        return ret

    return wrapper


@memoize
def mixin(*args):
    if len(args) == 1:
        return args[0]
    name = 'Mixin_%s' % '_'.join((cls.__name__ for cls in args))
    return type(str(name), args, {})


def monkeypatch(target, name=None, override=False, doc=None):

    def patcher(func):
        patchname = func.__name__ if name is None else name
        if not override:
            if old_hasattr(target, patchname):
                raise TypeError('Class %s already has method %s' % (target.__name__, patchname))
        setattr(target, patchname, func)
        try:
            func.__name__ = str(patchname)
        except AttributeError:
            pass

        if doc is not None:
            func.__doc__ = doc
        return func

    return patcher


def monkeypatch_extend(target, name=None):

    def patcher(func):
        newfunc = func
        patchname = func.__name__ if name is None else name
        if old_hasattr(target, patchname):
            oldfunc = getattr(target, patchname)
            if not callable(oldfunc):
                raise TypeError('Can not extend non callable attribute')

            @wraps(oldfunc)
            def extended(*a, **k):
                ret = oldfunc(*a, **k)
                func(*a, **k)
                return ret

            newfunc = extended
        else:
            pass
        setattr(target, patchname, newfunc)
        return func

    return patcher


def instance_decorator(decorator):

    class Decorator(object):

        def __init__(self, func=nop, *args, **kws):
            self.__name__ = func.__name__
            self.__doc__ = func.__doc__
            self._data_name = '%s_%d_decorated_instance' % (func.__name__, id(self))
            self._func = func
            self._args = args
            self._kws = kws

        def __get__(self, obj, cls=None):
            if obj is None:
                return
            data_name = self._data_name
            try:
                return obj.__dict__[data_name]
            except KeyError:
                decorated = decorator(obj, self._func, *(self._args), **self._kws)
                obj.__dict__[data_name] = decorated
                return decorated

    return Decorator


def forward_property(member):

    class Descriptor(object):

        def __init__(self, func_or_name):
            self._property_name = func_or_name.__name__ if callable(func_or_name) else func_or_name

        def __get__(self, obj, cls=None):
            return getattr(getattr(obj, member), self._property_name)

        def __set__(self, obj, value):
            return setattr(getattr(obj, member), self._property_name, value)

    return Descriptor


class lazy_attribute(object):

    def __init__(self, func, name=None):
        wraps(func)(self)
        self._func = func
        if name:
            self.__name__ = name

    def __get__(self, obj, cls=None):
        if obj is None:
            return self
        result = obj.__dict__[self.__name__] = self._func(obj)
        return result


def remove_if(predicate, lst):
    return [elem for elem in lst if not predicate(elem)]


def flatten(list):
    return chain(*list)


def group(lst, n):
    n = int(n)
    return list(zip_longest(*[lst[i::n] for i in range(n)]))


def find_if(predicate, seq):
    for x in seq:
        if predicate(x):
            return x


def index_if(predicate, seq):
    idx = 0
    for x in seq:
        if predicate(x):
            return idx
        else:
            idx += 1

    return idx


def union(a, b):
    a = dict(a)
    a.update(b)
    return a


def product(iter_a, iter_b):
    for a in iter_a:
        for b in iter_b:
            yield (
             a, b)


def next(iter):
    return iter.next()


def is_iterable(value):
    try:
        it = iter(value)
        return bool(it)
    except TypeError:
        return False


def recursive_map(fn, element, sequence_type=None):
    if sequence_type is None:
        return recursive_map(fn, element, type(element))
    if isinstance(element, sequence_type):
        return list(map(lambda x: recursive_map(fn, x, sequence_type)
, element))
    return fn(element)


def is_matrix(iterable):
    if is_iterable(iterable):
        if len(iterable) > 0:
            return all(map(lambda x: is_iterable(x) and len(iterable[0]) == len(x) and len(x) > 0
, iterable))
    return False


def first(seq):
    return seq[0]


def second(seq):
    return seq[1]


def third(seq):
    return seq[2]


def compose(*funcs):
    return lambda x: reduce(lambda x, f: f(x)
, funcs[::-1], x)


def is_contextmanager(value):
    return callable(getattr(value, '__enter__', None)) and callable(getattr(value, '__exit__', None))


def infinite_context_manager(generator):
    make_context_manager = contextmanager(generator)

    class InfiniteContextManager(object):

        def __enter__(self):
            self._delegate = make_context_manager()
            self._delegate.__enter__()

        def __exit__(self, type, err, trace):
            self._delegate.__exit__(type, err, trace)
            del self._delegate

    return InfiniteContextManager


@contextmanager
def aggregate_contexts(handlers):
    for handler in handlers:
        handler.__enter__()

    err = None
    exc_info = (None, None, None)
    try:
        yield
    except BaseException as e:
        try:
            exc_info = sys.exc_info()
            err = e
        finally:
            e = None
            del e

    for handler in reversed(handlers):
        if (handler.__exit__)(*exc_info):
            err = False
            exc_info = (None, None, None)

    if err:
        raise err


class BooleanContext(object):
    default_value = False

    def __init__(self, default_value=None, *a, **k):
        (super(BooleanContext, self).__init__)(*a, **k)
        if default_value is not None:
            self.default_value = default_value
        self._current_value = self.default_value

    def __nonzero__(self):
        return bool(self._current_value)

    def __bool__(self):
        return self.__nonzero__()

    def __call__(self, update_value=None):
        return self.Manager(self, update_value)

    @property
    def value(self):
        return self._current_value

    class Manager(object):

        def __init__(self, managed=None, update_value=None, *a, **k):
            (super(BooleanContext.Manager, self).__init__)(*a, **k)
            self._managed = managed
            self._update_value = update_value if update_value is not None else not managed.default_value

        def __enter__(self):
            managed = self._managed
            self._old_value = managed._current_value
            managed._current_value = self._update_value
            return self

        def __exit__(self, *a, **k):
            self._managed._current_value = self._old_value


class OutermostOnlyContext(object):

    def __init__(self, *a, **k):
        self._entered_count = 0

    @contextmanager
    def __call__(self, context):
        self._entered_count += 1
        if self._entered_count == 1:
            with context as result:
                yield result
        else:
            yield
        self._entered_count -= 1


def dict_diff(left, right):
    dummy = object()
    return dict(filter(lambda kv: left.get(kv[0], dummy) != kv[1]
, iteritems(right)))


class NamedTuple(object):

    def __init__(self, *others, **k):
        super(NamedTuple, self).__init__()
        for other in others:
            diff = dict_diff(self._eq_dict, other._eq_dict)
            self._eq_dict.update(diff)
            self.__dict__.update(diff)

        self.__dict__.update(k)
        if '_eq_dict' in self.__dict__:
            self._eq_dict.update(k)

    def __setattr__(self, name, value):
        raise AttributeError('Named tuple is constant')

    def __delattr__(self, name):
        raise AttributeError('Named tuple is constant')

    def __getitem__(self, name):
        return self.__dict__[name]

    @lazy_attribute
    def _eq_dict(self):

        def public(objdict):
            return dict(filter(lambda kv: not kv[0].startswith('_')
, iteritems(objdict)))

        return reduce(lambda a, b: union(b, a)
, map(lambda c: public(c.__dict__)
, self.__class__.__mro__), public(self.__dict__))

    def __eq__(self, other):
        return isinstance(other, NamedTuple) and self._eq_dict == other._eq_dict

    def __hash__(self):
        return hash(id(self))

    def __getstate__(self):
        res = dict(self.__dict__)
        try:
            del res['_eq_dict']
        except KeyError:
            pass

        return res


class Slicer(object):

    def __init__(self, dimensions=1, extractor=nop, keys=tuple(), *a, **k):
        (super(Slicer, self).__init__)(*a, **k)
        self._keys = keys
        self._dimensions = dimensions
        self._extractor = extractor

    def __getitem__(self, key):
        new = key if isinstance(key, tuple) else (key,)
        keys = self._keys + new
        if len(keys) == self._dimensions:
            return (self._extractor)(*keys)
        return Slicer(dimensions=(self._dimensions),
          extractor=(self._extractor),
          keys=keys)

    def __call__(self):
        return self


get_slice = Slicer()

def slicer(dimensions):

    def decorator(extractor):

        @wraps(extractor)
        def make_slicer(*a, **k):
            return Slicer(dimensions=dimensions, extractor=partial(extractor, *a, **k))

        return make_slicer

    return decorator


def print_message(*messages):
    print(' '.join(list(map(str, messages))))


def old_hasattr(obj, attr):
    try:
        getattr(obj, attr)
        return True
    except Exception:
        return False


class overlaymap(object):

    def __init__(self, *maps):
        self._maps = maps

    def __getitem__(self, key):
        for m in self._maps:
            if key in m:
                return m[key]

        raise KeyError(key)

    def keys(self):
        res = set()
        for key in chain.from_iterable(self._maps):
            res.add(key)

        return list(res)

    def values(self):
        return [self[key] for key in self.keys()]

    def iteritems(self):
        for key in self.keys():
            yield (key, self[key])


def trace_value(value, msg='Value: '):
    print(msg, value)
    return value


class Bindable(object):
    _bound_instances = None

    def __get__(self, obj, cls=None):
        import weakref
        if obj is None:
            return self
        if self._bound_instances is None:
            self._bound_instances = weakref.WeakKeyDictionary()
        bound_dict = self._bound_instances.setdefault(obj, weakref.WeakKeyDictionary())
        try:
            bound = bound_dict[self]
        except KeyError:
            bound = self.bind(weakref.proxy(obj))
            bound_dict[self] = bound

        return bound

    def bind(self, bind_to_object):
        raise NotImplementedError