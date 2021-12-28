#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/_Framework/CompoundElement.py
from __future__ import absolute_import, print_function, unicode_literals
from builtins import filter
from builtins import map
from .ControlElement import ControlElementClient
from .SubjectSlot import subject_slot_group, SlotManager
from .NotifyingControlElement import NotifyingControlElement
from .Util import BooleanContext, first, second

class NestedElementClient(ControlElementClient):

    def __init__(self, compound = None, client = None, **k):
        super(NestedElementClient, self).__init__(**k)
        self.compound = compound
        self.client = client

    def set_control_element(self, element, grabbed):
        self.compound.set_control_element(element, grabbed)


class CompoundElement(NotifyingControlElement, SlotManager, ControlElementClient):
    u"""
    Utility class that helps in writing Elements that act as a facade
    to nested elements, hiding the complexity oif making sure that
    resource ownership rules are preserved.
    """
    _is_resource_based = False

    def __init__(self, *a, **k):
        super(CompoundElement, self).__init__(*a, **k)
        resource = self.resource
        original_grab_resource = resource.grab
        original_release_resource = resource.release

        def grab_resource(client, **k):
            self._grab_nested_control_elements(client, **k)
            original_grab_resource(client, **k)

        def release_resource(client):
            original_release_resource(client)
            self._release_nested_control_elements(client)

        self.resource.grab = grab_resource
        self.resource.release = release_resource
        self._nested_control_elements = dict()
        self._nested_element_clients = dict()
        self._disable_notify_owner_on_button_ownership_change = BooleanContext()
        self._listen_nested_requests = 0

    def on_nested_control_element_received(self, control):
        u"""
        Notifies that the nested control can be used by the compound
        """
        raise NotImplementedError

    def on_nested_control_element_lost(self, control):
        u"""
        Notifies that we lost control over the control.
        """
        raise NotImplementedError

    def on_nested_control_element_value(self, value, control):
        u"""
        Notifies that an owned control element has received a value.
        """
        raise NotImplementedError

    def get_control_element_priority(self, element, priority):
        u"""
        Override to change priority for control element.
        """
        assert self._has_resource
        return priority

    def register_control_elements(self, *elements):
        return list(map(self.register_control_element, elements))

    def register_control_element(self, element):
        assert element not in self._nested_control_elements
        self._nested_control_elements[element] = False
        if self._listen_nested_requests > 0:
            self._on_nested_control_element_value.add_subject(element)
        if self._is_resource_based and self.resource.owner:
            priority = self.get_control_element_priority(element, self.resource.max_priority)
            nested_client = self._get_nested_client(self.resource.owner)
            element.resource.grab(nested_client, priority=priority)
        elif not self._is_resource_based:
            with self._disable_notify_owner_on_button_ownership_change():
                element.notify_ownership_change(self, True)
        return element

    def unregister_control_elements(self, *elements):
        return list(map(self.unregister_control_element, elements))

    def unregister_control_element(self, element):
        assert element in self._nested_control_elements
        if self._is_resource_based:
            for client in self.resource.clients:
                nested_client = self._get_nested_client(client)
                element.resource.release(nested_client)

        else:
            with self._disable_notify_owner_on_button_ownership_change():
                element.notify_ownership_change(self, False)
        if self._listen_nested_requests > 0:
            self._on_nested_control_element_value.remove_subject(element)
        del self._nested_control_elements[element]
        return element

    def has_control_element(self, control):
        return control in self._nested_control_elements

    def owns_control_element(self, control):
        return self._nested_control_elements.get(control, False)

    def owned_control_elements(self):
        return list(map(first, filter(second, iter(self._nested_control_elements.items()))))

    def nested_control_elements(self):
        return iter(self._nested_control_elements.keys())

    def reset(self):
        for element in self.owned_control_elements():
            element.reset()

    def reset_state(self):
        for element in self.owned_control_elements():
            element.reset_state()

    def add_value_listener(self, *a, **k):
        if self.value_listener_count() == 0:
            self.request_listen_nested_control_elements()
        super(CompoundElement, self).add_value_listener(*a, **k)

    def remove_value_listener(self, *a, **k):
        super(CompoundElement, self).remove_value_listener(*a, **k)
        if self.value_listener_count() == 0:
            self.unrequest_listen_nested_control_elements()

    def request_listen_nested_control_elements(self):
        u"""
        By default, the compound control element will listen to its
        nested control elements IFF he himself has listeners.  This is
        important, because for nested InputControlElements, the
        existence of listeners determine wether they will send the
        MIDI messages to Live or to the script.
        
        You can force the compound to listen to its nested elements
        using this methods.  The compound will then listen to them IFF
        the number of requests is greater than the number of
        unrequests OR it has listeners.
        """
        if self._listen_nested_requests == 0:
            self._connect_nested_control_elements()
        self._listen_nested_requests += 1

    def unrequest_listen_nested_control_elements(self):
        u"""
        See request_listen_nested_control_elements()
        """
        if self._listen_nested_requests == 1:
            self._disconnect_nested_control_elements()
        self._listen_nested_requests -= 1

    def _connect_nested_control_elements(self):
        self._on_nested_control_element_value.replace_subjects(list(self._nested_control_elements.keys()))

    def _disconnect_nested_control_elements(self):
        self._on_nested_control_element_value.replace_subjects([])

    def _on_nested_control_element_received(self, control):
        if control in self._nested_control_elements:
            if not self._nested_control_elements[control]:
                self._nested_control_elements[control] = True
        self.on_nested_control_element_received(control)

    def _on_nested_control_element_lost(self, control):
        if control in self._nested_control_elements:
            if self._nested_control_elements[control]:
                self._nested_control_elements[control] = False
        self.on_nested_control_element_lost(control)

    @subject_slot_group(u'value')
    def _on_nested_control_element_value(self, value, sender):
        if self.owns_control_element(sender):
            self.on_nested_control_element_value(value, sender)

    def set_control_element(self, control, grabbed):
        if grabbed:
            self._on_nested_control_element_received(control)
        else:
            self._on_nested_control_element_lost(control)
        owner = self._resource.owner
        if owner and not self._disable_notify_owner_on_button_ownership_change:
            self.notify_ownership_change(owner, True)

    def _grab_nested_control_elements(self, client, priority = None, **k):
        was_resource_based = self._is_resource_based
        self._is_resource_based = True
        nested_client = self._get_nested_client(client)
        with self._disable_notify_owner_on_button_ownership_change():
            for element in list(self._nested_control_elements.keys()):
                if not was_resource_based:
                    element.notify_ownership_change(self, False)
                nested_priority = self.get_control_element_priority(element, priority)
                element.resource.grab(nested_client, priority=nested_priority)

    def _release_nested_control_elements(self, client):
        assert self._is_resource_based
        nested_client = self._get_nested_client(client)
        with self._disable_notify_owner_on_button_ownership_change():
            for element in list(self._nested_control_elements.keys()):
                element.resource.release(nested_client)

    def _get_nested_client(self, client):
        try:
            nested_client = self._nested_element_clients[client]
        except KeyError:
            nested_client = self._nested_element_clients[client] = NestedElementClient(self, client)

        return nested_client
