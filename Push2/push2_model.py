<<<<<<< HEAD
=======
# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Push2/push2_model.py
# Compiled at: 2022-01-27 16:28:16
# Size of source mod 2**32: 2864 bytes
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
from __future__ import absolute_import, print_function, unicode_literals
from builtins import object
import json, logging
from pprint import pformat
from ableton.v2.base import PY2
from .model import RootModel
from model.generation import ModelUpdateNotifier, generate_mrs_model
logger = logging.getLogger(__name__)

class Sender(object):

    def __init__(self, message_sink=None, process_connected=None, *a, **k):
        (super(Sender, self).__init__)(*a, **k)
        self._message_sink = message_sink
        if process_connected is None:
            process_connected = lambda: True
        self._process_connected = process_connected
        self._attribute_paths = []
        self._structural_change = False
        self.notifier = ModelUpdateNotifier(delegate=self)

    def structural_change(self, path):
        self._attribute_paths.append((path, None))
        self._structural_change = True

    def attribute_changed(self, path, value):
        self._attribute_paths.append((path, value))

    def send(self, root_model, send_all=False):

        def send_data(data):
            if data['command'] == 'full-model-update':
                data['fingerprint'] = root_model.__fingerprint__
            raw = json.dumps(data, ensure_ascii=True)
            self._message_sink(raw)
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug('Model sent: %s', pformat(data))

        if send_all:
            send_data(dict(command='full-model-update', payload=(root_model.to_json())))
<<<<<<< HEAD
        else:
            if self._structural_change:
                root_keys = set((path[0][0] for path in self._attribute_paths))
                data = dict(command='full-model-update',
                  payload=(root_model.to_json(root_keys)))
                send_data(data)
            else:
                if self._attribute_paths:
                    data = dict(command='path-model-update', payload=(self._attribute_paths))
                    send_data(data)
=======
        elif self._structural_change:
            root_keys = set((path[0][0] for path in self._attribute_paths))
            data = dict(command='full-model-update',
              payload=(root_model.to_json(root_keys)))
            send_data(data)
        elif self._attribute_paths:
            data = dict(command='path-model-update', payload=(self._attribute_paths))
            send_data(data)
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
        self._attribute_paths = []
        self._structural_change = False


class Root(generate_mrs_model(RootModel)):

    def __init__(self, sender=None, *a, **k):
        self._sender = sender
        if sender is not None:
            k['notifier'] = sender.notifier
        (super(Root, self).__init__)(*a, **k)

    def commit_changes(self, send_all=False):
        if self._sender is not None:
            self._sender.send(self, send_all)

    def to_json(self, root_keys=None):
        if root_keys is None:
            return super(Root, self).to_json()
        res = {}
        for key in root_keys:
            res[key] = self.data[key].to_json()

        return res