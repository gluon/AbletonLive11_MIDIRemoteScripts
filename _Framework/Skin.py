from __future__ import absolute_import, print_function, unicode_literals
from builtins import map, object, str
from future.utils import raise_
from itertools import chain

class SkinColorMissingError(Exception):
    pass


class Skin(object):

    def __init__(self, colors=None, *a, **k):
        (super(Skin, self).__init__)(*a, **k)
        self._colors = {}
        if colors is not None:
            self._fill_colors(colors)

    def _fill_colors(self, colors, pathname=''):
        if getattr(colors, '__bases__', None):
            for base in colors.__bases__:
                self._fill_colors(base)

        for k, v in colors.__dict__.items():
            if k[:1] != '_':
                if callable(v):
                    self._fill_colors(v, pathname + k + '.')
                else:
                    self._colors[pathname + k] = v

    def __getitem__(self, key):
        try:
            return self._colors[key]
        except KeyError:
            raise_(SkinColorMissingError, 'Skin color missing: %s' % str(key))

    def iteritems(self):
        return iter(self._colors.items())


def merge_skins(*skins):
    skin = Skin()
    skin._colors = dict(chain(*[list(s._colors.items()) for s in skins]))
    return skin