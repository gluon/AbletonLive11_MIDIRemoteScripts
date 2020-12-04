#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/_Framework/MessageScheduler.py
from __future__ import absolute_import, print_function, unicode_literals
from builtins import object
from collections import namedtuple

class MessageScheduler(object):
    u"""
    Schedules outgoing messages (sysex and other MIDI) sent to a
    MIDI port shared between multiple owners and synchronizes them
    with incoming messages (sysex only).
    For request/response message pairs this ensures that responses are
    sent back to where the requests came from (the owner).
    Also, it allows for a temporary routing of unexpected messages
    to an owner grabbing the device.
    """

    def __init__(self, send_message_callback, timer):
        self._send_message_callback = send_message_callback
        self._timer = timer
        self._state = u'idle'
        self._owner = None
        self._request_type = namedtuple(u'Request', u'action owner message timeout')
        self._request_queue = []

    @property
    def is_idling(self):
        return self._state == u'idle' and self._owner == None and len(self._request_queue) == 0

    def __repr__(self):
        return u'MessageScheduler(state={}, owner={})'.format(self._state, self._owner)

    def _process_request(self, request):
        assert self._owner == None or self._owner == request.owner
        if request.action == u'send':
            if self._state == u'idle' or self._state == u'grabbed' and self._owner == request.owner:
                self._send_message_callback(request.message)
                return True
            else:
                return False
        elif request.action == u'grab':
            if self._state == u'idle':
                self._state = u'grabbed'
                self._owner = request.owner
                self._owner.send_reply(u'grab', u'1')
                return True
            elif self._state == u'grabbed':
                request.owner.report_error(u'unexpected grab')
                return True
            else:
                return False
        elif request.action == u'release':
            if self._state == u'idle':
                request.owner.report_error(u'unexpected release')
                return True
            elif self._state == u'grabbed':
                assert self._owner == request.owner
                self._owner.send_reply(u'release', u'1')
                self._state = u'idle'
                self._owner = None
                return True
            else:
                return False
        elif request.action == u'send_receive':
            if self._state == u'idle':
                self._send_message_callback(request.message)
                self._state = u'wait'
                self._owner = request.owner
                self._timer.start(request.timeout, self.handle_timeout)
                return True
            elif self._state == u'grabbed' and self._owner == request.owner:
                self._send_message_callback(request.message)
                self._state = u'grabbed_wait'
                self._timer.start(request.timeout, self.handle_timeout)
                return True
            else:
                return False

    def _queue(self, request):
        if request.owner is not None:
            self._request_queue.append(request)

    def _process_single_request(self):
        for i, request in enumerate(self._request_queue):
            if self._owner in (None, request.owner):
                if self._process_request(request):
                    del self._request_queue[i]
                    return True
                else:
                    return False

        return False

    def _process_queue(self):
        while self._process_single_request():
            pass

    def send(self, owner, message):
        request = self._request_type(u'send', owner, message, 0)
        self._queue(request)
        self._process_queue()

    def grab(self, owner):
        request = self._request_type(u'grab', owner, None, 0)
        self._queue(request)
        self._process_queue()

    def release(self, owner):
        request = self._request_type(u'release', owner, None, 0)
        self._queue(request)
        self._process_queue()

    def send_receive(self, owner, message, timeout):
        request = self._request_type(u'send_receive', owner, message, timeout)
        self._queue(request)
        self._process_queue()

    def handle_message(self, message):
        if self._state == u'idle':
            pass
        elif self._state == u'wait':
            if self._owner.is_expected_reply(message):
                self._owner.send_reply(u'send_receive', message)
                self._state = u'idle'
                self._owner = None
                self._timer.cancel()
                self._process_queue()
        elif self._state == u'grabbed':
            self._owner.send_reply(u'received', message)
        elif self._state == u'grabbed_wait':
            if self._owner.is_expected_reply(message):
                self._owner.send_reply(u'send_receive', message)
                self._state = u'grabbed'
                self._timer.cancel()
                self._process_queue()
            else:
                self._owner.send_reply(u'received', message)

    def handle_timeout(self):
        if self._state == u'wait':
            self._owner.send_reply(u'send_receive', u'timeout')
            self._state = u'idle'
            self._owner = None
            self._process_queue()
        elif self._state == u'grabbed_wait':
            self._owner.send_reply(u'send_receive', u'timeout')
            self._state = u'grabbed'
            self._process_queue()

    def disconnect(self, owner):
        if self._state != u'idle':
            self._request_queue = [ r for r in self._request_queue if r.owner != owner ]
            if self._owner == owner:
                self._owner = None
                self._state = u'idle'
                self._timer.cancel()
            self._process_queue()
