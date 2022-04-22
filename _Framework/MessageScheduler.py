# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/_Framework/MessageScheduler.py
# Compiled at: 2022-01-27 16:28:16
# Size of source mod 2**32: 9234 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import object
from collections import namedtuple

class MessageScheduler(object):

    def __init__(self, send_message_callback, timer):
        self._send_message_callback = send_message_callback
        self._timer = timer
        self._state = 'idle'
        self._owner = None
        self._request_type = namedtuple('Request', 'action owner message timeout')
        self._request_queue = []

    @property
    def is_idling(self):
        return self._state == 'idle' and self._owner == None and len(self._request_queue) == 0

    def __repr__(self):
        return 'MessageScheduler(state={}, owner={})'.format(self._state, self._owner)

    def _process_request(self, request):
        if request.action == 'send':
            if not self._state == 'idle':
                if not self._state == 'grabbed' or self._owner == request.owner:
                    self._send_message_callback(request.message)
                    return True
                return False
        elif request.action == 'grab':
            if self._state == 'idle':
                self._state = 'grabbed'
                self._owner = request.owner
                self._owner.send_reply('grab', '1')
                return True
            if self._state == 'grabbed':
                request.owner.report_error('unexpected grab')
                return True
            return False
        elif request.action == 'release':
            if self._state == 'idle':
                request.owner.report_error('unexpected release')
                return True
            if self._state == 'grabbed':
                self._owner.send_reply('release', '1')
                self._state = 'idle'
                self._owner = None
                return True
            return False
        elif request.action == 'send_receive':
            if self._state == 'idle':
                self._send_message_callback(request.message)
                self._state = 'wait'
                self._owner = request.owner
                self._timer.start(request.timeout, self.handle_timeout)
                return True
            if self._state == 'grabbed':
                if self._owner == request.owner:
                    self._send_message_callback(request.message)
                    self._state = 'grabbed_wait'
                    self._timer.start(request.timeout, self.handle_timeout)
                    return True
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
        request = self._request_type('send', owner, message, 0)
        self._queue(request)
        self._process_queue()

    def grab(self, owner):
        request = self._request_type('grab', owner, None, 0)
        self._queue(request)
        self._process_queue()

    def release(self, owner):
        request = self._request_type('release', owner, None, 0)
        self._queue(request)
        self._process_queue()

    def send_receive(self, owner, message, timeout):
        request = self._request_type('send_receive', owner, message, timeout)
        self._queue(request)
        self._process_queue()

    def handle_message(self, message):
        if self._state == 'idle':
            pass
        elif self._state == 'wait':
            if self._owner.is_expected_reply(message):
                self._owner.send_reply('send_receive', message)
                self._state = 'idle'
                self._owner = None
                self._timer.cancel()
                self._process_queue()
        elif self._state == 'grabbed':
            self._owner.send_reply('received', message)
        elif self._state == 'grabbed_wait':
            if self._owner.is_expected_reply(message):
                self._owner.send_reply('send_receive', message)
                self._state = 'grabbed'
                self._timer.cancel()
                self._process_queue()
            else:
                self._owner.send_reply('received', message)

    def handle_timeout(self):
        if self._state == 'wait':
            self._owner.send_reply('send_receive', 'timeout')
            self._state = 'idle'
            self._owner = None
            self._process_queue()
        elif self._state == 'grabbed_wait':
            self._owner.send_reply('send_receive', 'timeout')
            self._state = 'grabbed'
            self._process_queue()

    def disconnect(self, owner):
        if self._state != 'idle':
            self._request_queue = [r for r in self._request_queue if r.owner != owner]
            if self._owner == owner:
                self._owner = None
                self._state = 'idle'
                self._timer.cancel()
            self._process_queue()