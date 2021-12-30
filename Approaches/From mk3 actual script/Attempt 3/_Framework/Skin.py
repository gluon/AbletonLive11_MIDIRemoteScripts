#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/_Framework/Skin.py
from __future__ import absolute_import, print_function, unicode_literals
from builtins import map
from builtins import str
from builtins import object
from future.utils import raise_
from itertools import chain

class SkinColorMissingError(Exception):
    pass


class Skin(object):

    def __init__(self, colors = None, *a, **k):
        super(Skin, self).__init__(*a, **k)
        self._colors = {}
        if colors is not None:
            self._fill_colors(colors)

    def _fill_colors(self, colors, pathname = u''):
        if getattr(colors, u'__bases__', None):
            for base in colors.__bases__:
                self._fill_colors(base)

        for k, v in colors.__dict__.items():
            if k[:1] != u'_':
                if callable(v):
                    self._fill_colors(v, pathname + k + u'.')
                else:
                    self._colors[pathname + k] = v

    def __getitem__(self, key):
        try:
            return self._colors[key]
        except KeyError:
            raise_(SkinColorMissingError, u'Skin color missing: %s' % str(key))

    def iteritems(self):
        return iter(self._colors.items())


def merge_skins(*skins):
    skin = Skin()
    skin._colors = dict(chain(*[ list(s._colors.items()) for s in skins ]))
    return skin
