# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/_Framework/Layer.py
# Compiled at: 2022-01-27 16:28:16
# Size of source mod 2**32: 6736 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import object, str
from future.utils import raise_
from itertools import repeat
from .ControlElement import ControlElementClient
from .Disconnectable import Disconnectable
from .Resource import CompoundResource, ExclusiveResource
from .Util import nop

class LayerError(Exception):
    pass


class UnhandledControlError(LayerError):
    pass


class SimpleLayerOwner(Disconnectable):

    def __init__(self, layer=None):
        self._layer = layer
        self._layer.grab(self)

    def disconnect(self):
        self._layer.release(self)


class LayerClient(ControlElementClient):

    def __init__(self, layer=None, layer_client=None, *a, **k):
        (super(LayerClient, self).__init__)(*a, **k)
        self.layer_client = layer_client
        self.layer = layer

    def set_control_element(self, control_element, grabbed):
        layer = self.layer
        owner = self.layer_client
        names = layer._control_to_names[control_element]
        if not grabbed:
            control_element = None
        for name in names:
            try:
                handler = getattr(owner, 'set_' + name)
            except AttributeError:
                try:
                    control = getattr(owner, name)
                    handler = control.set_control_element
                except AttributeError:
                    if name[0] != '_':
                        raise_(UnhandledControlError, 'Component %s has no handler for control_element %s' % (
                         str(owner), name))
                    else:
                        handler = nop

            handler(control_element or None)
            layer._name_to_controls[name] = control_element


class LayerBase(object):
    pass


class CompoundLayer(LayerBase, CompoundResource):

    def _get_priority(self):
        return self.first.priority

    def _set_priority(self, priority):
        self.first.priority = priority
        self.second.priority = priority

    priority = property(_get_priority, _set_priority)

    def __getattr__(self, key):
        try:
            return getattr(self.first, key)
        except AttributeError:
            return getattr(self.second, key)


class Layer(LayerBase, ExclusiveResource):

    def __init__(self, priority=None, **controls):
        super(Layer, self).__init__()
        self._priority = priority
        self._name_to_controls = dict(zip(iter(controls.keys()), repeat(None)))
        self._control_to_names = dict()
        self._control_clients = dict()
        for name, control in controls.items():
            self._control_to_names.setdefault(control, []).append(name)

    def __add__(self, other):
        return CompoundLayer(self, other)

    def _get_priority(self):
        return self._priority

    def _set_priority(self, priority):
        if priority != self._priority:
            if self.owner:
                raise RuntimeError("Cannot change priority of a layer while it's owned")
            self._priority = priority

    priority = property(_get_priority, _set_priority)

    def __getattr__(self, name):
        try:
            return self._name_to_controls[name]
        except KeyError:
            raise AttributeError

    def grab(self, client, *a, **k):
        if client == self.owner:
            (self.on_received)(client, *a, **k)
            return True
        return (super(Layer, self).grab)(client, *a, **k)

    def on_received(self, client, *a, **k):
        for control in self._control_to_names.keys():
            k.setdefault('priority', self._priority)
            (control.resource.grab)(self._get_control_client(client), *a, **k)

    def on_lost(self, client):
        for control in self._control_to_names.keys():
            control.resource.release(self._get_control_client(client))

    def _get_control_client(self, client):
        try:
            control_client = self._control_clients[client]
        except KeyError:
            control_client = self._control_clients[client] = LayerClient(layer_client=client,
              layer=self)

        return control_client