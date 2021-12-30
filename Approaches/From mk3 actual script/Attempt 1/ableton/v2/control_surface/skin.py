#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v2/control_surface/skin.py
from __future__ import absolute_import, print_function, unicode_literals
from future.utils import iteritems
from itertools import chain
from ableton.v2.base import depends, const, liveobj_valid, EventObject
from ableton.v2.control_surface.elements.color import is_dynamic_color_factory

class SkinColorMissingError(Exception):
    pass


class DynamicColorNotAvailableError(Exception):
    msg = u'In order to use dynamic colors, you need to inject the song while creating         the skin'


class Skin(EventObject):

    @depends(song=const(None))
    def __init__(self, colors = None, song = None, *a, **k):
        super(Skin, self).__init__(*a, **k)
        self._colors = {}
        self._factory_to_instance_map = {}
        if colors is not None:
            self._fill_colors(colors, song=song)

    def _fill_colors(self, colors, pathname = u'', song = None):
        if getattr(colors, u'__bases__', None):
            for base in colors.__bases__:
                self._fill_colors(base, song=song, pathname=pathname)

        for k, v in iteritems(colors.__dict__):
            if k[:1] != u'_':
                if callable(v):
                    self._fill_colors(v, pathname + k + u'.', song=song)
                else:
                    if is_dynamic_color_factory(v):
                        v = self._get_dynamic_color(v, song)
                    self._colors[pathname + k] = v

    def __getitem__(self, key):
        try:
            return self._colors[key]
        except KeyError:
            raise SkinColorMissingError(u'Skin color missing: %s' % str(key))

    def iteritems(self):
        return iteritems(self._colors)

    def _get_dynamic_color(self, color_factory, song):
        if not liveobj_valid(song):
            raise DynamicColorNotAvailableError
        else:
            if color_factory not in self._factory_to_instance_map:
                self._factory_to_instance_map[color_factory] = self._create_dynamic_color(color_factory, song)
            return self._factory_to_instance_map[color_factory]

    def _create_dynamic_color(self, color_factory, song):
        return self.register_disconnectable(color_factory.instantiate(song))


def merge_skins(*skins):
    skin = Skin()
    skin._colors = dict(chain(*map(lambda s: s._colors.items(), skins)))
    return skin
