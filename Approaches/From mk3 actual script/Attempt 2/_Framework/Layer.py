#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/_Framework/Layer.py
u"""
Module implementing a way to resource-based access to controls in an
unified interface dynamic.
"""
from __future__ import absolute_import, print_function, unicode_literals
from builtins import str
from builtins import object
from future.utils import raise_
from itertools import repeat
from .ControlElement import ControlElementClient
from .Util import nop
from .Resource import ExclusiveResource, CompoundResource
from .Disconnectable import Disconnectable

class LayerError(Exception):
    pass


class UnhandledControlError(LayerError):
    pass


class SimpleLayerOwner(Disconnectable):
    u"""
    Simple owner that grabs a given layer until it's disconnected
    """

    def __init__(self, layer = None):
        self._layer = layer
        self._layer.grab(self)

    def disconnect(self):
        self._layer.release(self)


class LayerClient(ControlElementClient):
    u"""
    Client of the indivial controls that delivers the controls to the
    layer owner.
    """

    def __init__(self, layer = None, layer_client = None, *a, **k):
        super(LayerClient, self).__init__(*a, **k)
        assert layer_client
        assert layer
        self.layer_client = layer_client
        self.layer = layer

    def set_control_element(self, control_element, grabbed):
        layer = self.layer
        owner = self.layer_client
        assert owner
        assert control_element in layer._control_to_names, u'Control not in layer: %s' % (control_element,)
        names = layer._control_to_names[control_element]
        if not grabbed:
            control_element = None
        for name in names:
            try:
                handler = getattr(owner, u'set_' + name)
            except AttributeError:
                try:
                    control = getattr(owner, name)
                    handler = control.set_control_element
                except AttributeError:
                    if name[0] != u'_':
                        raise_(UnhandledControlError, u'Component %s has no handler for control_element %s' % (str(owner), name))
                    else:
                        handler = nop

            handler(control_element or None)
            layer._name_to_controls[name] = control_element


class LayerBase(object):
    pass


class CompoundLayer(LayerBase, CompoundResource):
    u"""
    A compound resource takes two layers and makes them look like one,
    grabbing both of them.  Both can have different priorities
    thought.
    """

    def _get_priority(self):
        assert self.first.priority == self.second.priority
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
    u"""
    A layer provides a convenient interface to control resources. In a
    layer, you can group several controls by name.  The layer itself
    is an exclusive resource.  When grabbing the layer, it will try to
    grab all controls and will forward them to its own owner when he
    receives them, and will take them from him when they are
    release. The layer with give and take away the controls from its
    client using methods of the form::
    
        client.set[control-name](control)
    
    Where [control-name] is the name the control was given in this
    layer.  This way, layers are a convenient way to provide controls
    to components indirectly, with automatic handling of competition
    for them.
    
    Note that [control-name] can not be any of the following reserved
    names: priority, grab, release, on_received, on_lost, owner,
    get_owner
    
    If [control-name] starts with an underscore (_) it is considered
    private.  It is grabbed but it is not delivered to the client.
    """

    def __init__(self, priority = None, **controls):
        super(Layer, self).__init__()
        self._priority = priority
        self._name_to_controls = dict(zip(iter(controls.keys()), repeat(None)))
        self._control_to_names = dict()
        self._control_clients = dict()
        for name, control in controls.items():
            assert control is not None, name
            self._control_to_names.setdefault(control, []).append(name)

    def __add__(self, other):
        return CompoundLayer(self, other)

    def _get_priority(self):
        return self._priority

    def _set_priority(self, priority):
        if priority != self._priority:
            if self.owner:
                raise RuntimeError(u"Cannot change priority of a layer while it's owned")
            self._priority = priority

    priority = property(_get_priority, _set_priority)

    def __getattr__(self, name):
        u""" Provides access to controls """
        try:
            return self._name_to_controls[name]
        except KeyError:
            raise AttributeError

    def grab(self, client, *a, **k):
        if client == self.owner:
            self.on_received(client, *a, **k)
            return True
        return super(Layer, self).grab(client, *a, **k)

    def on_received(self, client, *a, **k):
        u""" Override from ExclusiveResource """
        for control in self._control_to_names.keys():
            k.setdefault(u'priority', self._priority)
            control.resource.grab(self._get_control_client(client), *a, **k)

    def on_lost(self, client):
        u""" Override from ExclusiveResource """
        for control in self._control_to_names.keys():
            control.resource.release(self._get_control_client(client))

    def _get_control_client(self, client):
        try:
            control_client = self._control_clients[client]
        except KeyError:
            control_client = self._control_clients[client] = LayerClient(layer_client=client, layer=self)

        return control_client
