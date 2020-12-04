#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/_MxDCore/MxDUtils.py
from __future__ import absolute_import, print_function, unicode_literals
from past.builtins import cmp
from builtins import str
from builtins import range
from builtins import object
from future.utils import string_types
import logging
from ableton.v2.base import old_hasattr
logger = logging.getLogger(__name__)

class TupleWrapper(object):
    u""" Wrapper class for the access to volatile lists and tuples in the Python API """
    _tuple_wrapper_registry = {}

    def forget_tuple_wrapper_instances():
        TupleWrapper._tuple_wrapper_registry = {}

    forget_tuple_wrapper_instances = staticmethod(forget_tuple_wrapper_instances)

    def get_tuple_wrapper(parent, attribute, element_filter = None):
        if (parent, attribute) not in TupleWrapper._tuple_wrapper_registry:
            TupleWrapper._tuple_wrapper_registry[parent, attribute] = TupleWrapper(parent, attribute, element_filter)
        return TupleWrapper._tuple_wrapper_registry[parent, attribute]

    get_tuple_wrapper = staticmethod(get_tuple_wrapper)

    def __init__(self, parent, attribute, element_filter = None):
        assert isinstance(attribute, string_types)
        self._parent = parent
        self._attribute = attribute
        self._element_filter = element_filter

    def get_list(self):
        result = ()
        parent = self._parent
        if parent == None:
            parent = __builtins__
        if isinstance(parent, dict):
            if self._attribute in list(parent.keys()):
                result = parent[self._attribute]
        elif old_hasattr(parent, self._attribute):
            result = getattr(parent, self._attribute)
        if self._element_filter:
            return [ (e if self._element_filter(e) else None) for e in result ]
        return result


STATE_NEUTRAL = u'neutral'
STATE_QUOTED_STR = u'quoted'
STATE_UNQUOTED_STR = u'unquoted'
STATE_PENDING_NR = u'number'
STATE_PENDING_FLOAT = u'float'
QUOTE_ENTITY = u'&quot;'
QUOTE_SIMPLE = u'"'

class StringHandler(object):
    u""" Class that can parse incoming strings and format outgoing strings """

    def prepare_incoming(string):
        assert isinstance(string, string_types)
        return string.replace(QUOTE_ENTITY, QUOTE_SIMPLE)

    prepare_incoming = staticmethod(prepare_incoming)

    def prepare_outgoing(string):
        assert isinstance(string, string_types)
        result = string.replace(QUOTE_SIMPLE, QUOTE_ENTITY)
        if result.find(u' ') >= 0:
            result = QUOTE_SIMPLE + result + QUOTE_SIMPLE
        return result

    prepare_outgoing = staticmethod(prepare_outgoing)

    def parse(string, id_callback):
        assert isinstance(string, string_types)
        return StringHandler(id_callback).parse_string(string)

    parse = staticmethod(parse)

    def __init__(self, id_callback):
        self._state = STATE_NEUTRAL
        self._sub_string = u''
        self._open_quote_index = -1
        self._id_callback = id_callback

    def parse_string(self, string):
        self._arguments = []
        self._sub_string = u''
        self._state = STATE_NEUTRAL
        self._open_quote_index = -1
        for index in range(len(string)):
            char = string[index]
            handle_selector = u'_' + str(self._state) + u'_handle_char'
            if old_hasattr(self, handle_selector):
                getattr(self, handle_selector)(char, index)
            else:
                logger.info(u'Unknown state ' + str(self._state))
                assert False

        finalize_selector = u'_finalize_' + str(self._state)
        if len(self._sub_string) > 0 and old_hasattr(self, finalize_selector):
            getattr(self, finalize_selector)()
        return self._arguments

    def _neutral_handle_char(self, char, index):
        if char == u'"':
            self._open_quote_index = index
            self._state = STATE_QUOTED_STR
        elif char != u' ':
            self._sub_string += char
            if str(char).isdigit():
                self._state = STATE_PENDING_NR
            else:
                self._state = STATE_UNQUOTED_STR

    def _number_handle_char(self, char, index):
        if char == u' ':
            if len(self._sub_string) > 0:
                self._finalize_number()
            else:
                self._state = STATE_NEUTRAL
        else:
            if char == u'.':
                self._state = STATE_PENDING_FLOAT
            elif not str(char).isdigit():
                self._state = STATE_UNQUOTED_STR
            self._sub_string += char

    def _float_handle_char(self, char, index):
        if char == u' ':
            self._add_argument(float(self._sub_string))
        else:
            if char in (u'.', u'e', u'E'):
                if char in self._sub_string:
                    self._state = STATE_UNQUOTED_STR
            elif not str(char).isdigit():
                self._state = STATE_UNQUOTED_STR
            self._sub_string += char

    def _unquoted_handle_char(self, char, index):
        if char == u' ':
            self._add_argument(self._sub_string)
        else:
            if str(char).isdigit():
                if self._sub_string == u'-':
                    self._state = STATE_PENDING_NR
                elif self._sub_string in (u'.', u'-.'):
                    self._state = STATE_PENDING_FLOAT
            self._sub_string += char

    def _quoted_handle_char(self, char, index):
        if char == u'"':
            self._open_quote_index = -1
            self._add_argument(self._sub_string)
        else:
            self._sub_string += char

    def _finalize_quoted(self):
        raise RuntimeError(u'no match for quote at index %d found' % self._open_quote_index)

    def _finalize_unquoted(self):
        self._add_argument(self._sub_string)

    def _finalize_float(self):
        self._add_argument(float(self._sub_string))

    def _finalize_number(self):
        argument = int(self._sub_string)
        if str(self._arguments[-1]) == u'id':
            self._arguments.pop()
            try:
                argument = self._id_callback(argument)
            except KeyError:
                raise RuntimeError(u'Invalid id')

        self._add_argument(argument)

    def _add_argument(self, argument):
        if isinstance(argument, string_types):
            argument = StringHandler.prepare_incoming(argument)
        self._arguments.append(argument)
        self._sub_string = u''
        self._state = STATE_NEUTRAL
