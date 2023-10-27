# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v2\control_surface\control_element.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 7111 bytes
from __future__ import absolute_import, print_function, unicode_literals
from future.utils import iteritems, string_types
import logging, re, traceback
from ..base import Disconnectable, Event, EventObject, const, depends, lazy_attribute, nop, second, task
from .resource import StackingResource
logger = logging.getLogger(__name__)

class ControlElementClient(object):

    def set_control_element(self, control_element, grabbed):
        pass


class ElementOwnershipHandler(object):

    def handle_ownership_change(self, control, client, status):
        client.set_control_element(control, status)


class OptimizedOwnershipHandler(ElementOwnershipHandler):

    def __init__(self, *a, **k):
        (super(OptimizedOwnershipHandler, self).__init__)(*a, **k)
        self._ownership_changes = {}
        self._sequence_number = 0

    def handle_ownership_change(self, control, client, status):
        if (
         control, client, not status) in self._ownership_changes:
            del self._ownership_changes[(control, client, not status)]
        else:
            self._ownership_changes[(control, client, status)] = self._sequence_number
        self._sequence_number += 1

    @depends(traceback=(const(traceback)))
    def commit_ownership_changes(self, traceback=None):
        notify = super(OptimizedOwnershipHandler, self).handle_ownership_change
        while self._ownership_changes:
            notifications = sorted((iteritems(self._ownership_changes)), key=second)
            self._ownership_changes.clear()
            for (control, client, status), _ in notifications:
                try:
                    notify(control, client, status)
                except Exception:
                    logger.error('Error when trying to give control: %s', control.name)
                    traceback.print_exc()

        self._ownership_changes.clear()
        self._sequence_number = 0


_element_list_access_expr = re.compile('(\\w+)\\[([+-]?\\d+)\\]')

@depends(element_container=(const(None)))
def get_element(obj, element_container=None):
    if isinstance(obj, string_types):
        if element_container is None:
            raise RuntimeError('Control elements can only be accessed by name, if an element container is available')
        match = _element_list_access_expr.match(obj)
        if match:
            name = match.group(1)
            index = int(match.group(2))
            obj = getattr(element_container, name)[index]
        else:
            obj = getattr(element_container, obj)
    return obj


class ControlElement(Disconnectable):

    class ProxiedInterface(object):
        send_midi = nop
        reset_state = nop

        def __init__(self, outer=None, *a, **k):
            (super(ControlElement.ProxiedInterface, self).__init__)(*a, **k)
            self._outer = outer

        @property
        def outer(self):
            return self._outer

    @lazy_attribute
    def proxied_interface(self):
        return self.ProxiedInterface(outer=self)

    canonical_parent = None
    name = ''
    optimized_send_midi = True
    _has_resource = False
    _resource_type = StackingResource
    _has_task_group = False

    @depends(send_midi=None, register_control=None)
    def __init__(self, name='', is_private=False, resource_type=None, optimized_send_midi=None, send_midi=None, register_control=None, *a, **k):
        (super(ControlElement, self).__init__)(*a, **k)
        self._send_midi = send_midi
        self.name = name
        self.is_private = is_private
        if resource_type is not None:
            self._resource_type = resource_type
        if optimized_send_midi is not None:
            self.optimized_send_midi = optimized_send_midi
        register_control(self)

    def disconnect(self):
        self.reset()
        super(ControlElement, self).disconnect()

    def send_midi(self, message):
        return self._send_midi(message, optimized=(self.optimized_send_midi))

    def clear_send_cache(self):
        pass

    def reset(self):
        raise NotImplementedError

    def reset_state(self):
        pass

    @property
    def resource(self):
        return self._resource

    @lazy_attribute
    def _resource(self):
        self._has_resource = True
        return self._resource_type(self._on_resource_received, self._on_resource_lost)

    @lazy_attribute
    @depends(parent_task_group=(task.TaskGroup))
    def _tasks(self, parent_task_group=None):
        tasks = parent_task_group.add(task.TaskGroup())
        self._has_task_group = True
        return tasks

    def _on_resource_received(self, client, *a, **k):
        self.notify_ownership_change(client, True)

    def _on_resource_lost(self, client):
        self.notify_ownership_change(client, False)

    @depends(element_ownership_handler=(const(ElementOwnershipHandler())))
    def notify_ownership_change(self, client, grabbed, element_ownership_handler=None):
        element_ownership_handler.handle_ownership_change(self, client, grabbed)


class NotifyingControlElement(EventObject, ControlElement):
    __events__ = (
     Event(name='value',
       doc=' Called when the control element receives a MIDI value\n                             from the hardware '),)