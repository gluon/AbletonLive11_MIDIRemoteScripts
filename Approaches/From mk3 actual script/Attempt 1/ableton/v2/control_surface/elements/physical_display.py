#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v2/control_surface/elements/physical_display.py
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
from builtins import filter
from builtins import map
from builtins import zip
from past.builtins import unicode
from past.utils import old_div
from itertools import starmap, chain
from functools import partial
from ...base import const, first, group, in_range, lazy_attribute, maybe, nop, second, slice_size, slicer, task, to_slice
from ..control_element import ControlElement, NotifyingControlElement
from ..resource import StackingResource, ProxyResource, ClientWrapper
from .display_data_source import adjust_string
from .logical_display_segment import LogicalDisplaySegment

class _DisplayCentralResource(StackingResource):
    u"""
    Resource to be used internally by the PhysicalDisplayElement.  All
    sub-displays and the display itself will compete against this
    central resource.  The central resource will take into account
    whether there is any free area in the display for a client, to
    decide whether he gets it or not.
    """

    def __init__(self, root_display = None, *a, **k):
        super(_DisplayCentralResource, self).__init__(*a, **k)
        self._root_display = root_display

    def _actual_owners(self):
        remaining_indexes = set(self._root_display.display_indexes)

        def filter_client(client):
            display = client[0][0]
            result = remaining_indexes & display.display_indexes
            remaining_indexes.difference_update(display.display_indexes)
            return bool(result)

        return list(reversed(list(map(first, filter(filter_client, reversed(self._clients))))))


class DisplayError(Exception):
    pass


class DisplaySegmentationError(DisplayError):
    pass


class DisplayElement(ControlElement):
    u"""
    Base class for character-based displays.
    """

    class ProxiedInterface(ControlElement.ProxiedInterface):
        set_num_segments = nop
        set_data_sources = nop
        segment = const(LogicalDisplaySegment(1, nop))

    def __init__(self, width_in_chars = None, num_segments = 1, *a, **k):
        super(DisplayElement, self).__init__(*a, **k)
        assert width_in_chars is not None
        assert num_segments is not None
        self._width = width_in_chars
        self._logical_segments = []
        self.set_num_segments(num_segments)

    def __repr__(self):
        return u'<%s %r>' % (self.__class__.__name__, self.display_string)

    @property
    def display_string(self):
        return u''.join(map(unicode, self._logical_segments))

    @property
    def width(self):
        return self._width

    @lazy_attribute
    def display_slice(self):
        return slicer(1)(nop)()[:]

    @lazy_attribute
    def display_indexes(self):
        u"""
        Indexes of the current display w.r.t. the parent display indexes.
        """
        return set(range(self._width))

    def disconnect(self):
        self._disconnect_segments()
        super(DisplayElement, self).disconnect()

    def _disconnect_segments(self):
        for segment in self._logical_segments:
            segment.disconnect()

    @property
    def num_segments(self):
        return len(self._logical_segments)

    def set_num_segments(self, num_segments):
        width = self._width
        if not in_range(num_segments, 1, width) or width % num_segments != 0:
            raise DisplaySegmentationError(u'Can not split display of size %d into %d segments' % (self.width, num_segments))
        if num_segments != len(self._logical_segments):
            self._disconnect_segments()
            self._width_per_segment = old_div(width, num_segments)
            self._logical_segments = [ LogicalDisplaySegment(self._width_per_segment, self.update) for _ in range(num_segments) ]

    def set_data_sources(self, sources):
        u"""
        Given a sequences of data sources, divides the display into
        the number of segments needed to accommodate them and connects
        the logical segments to the data sources.
        """
        if not sources:
            self.set_num_segments(1)
            self.reset()
        else:
            self.set_num_segments(len(sources))
            for segment, source in zip(self._logical_segments, sources):
                segment.set_data_source(source)

    @property
    def segments(self):
        return tuple(self._logical_segments)

    def segment(self, index):
        return self._logical_segments[index]

    def reset(self):
        for segment in self._logical_segments:
            segment.set_data_source(None)

    def update(self):
        pass


class PhysicalDisplayElement(DisplayElement, NotifyingControlElement):
    u"""
    A physical character based display control element.
    """
    ascii_translations = {u'0': 48,
     u'1': 49,
     u'2': 50,
     u'3': 51,
     u'4': 52,
     u'5': 53,
     u'6': 54,
     u'7': 55,
     u'8': 56,
     u'9': 57,
     u'A': 65,
     u'B': 66,
     u'C': 67,
     u'D': 68,
     u'E': 69,
     u'F': 70,
     u'G': 71,
     u'H': 72,
     u'I': 73,
     u'J': 74,
     u'K': 75,
     u'L': 76,
     u'M': 77,
     u'N': 78,
     u'O': 79,
     u'P': 80,
     u'Q': 81,
     u'R': 82,
     u'S': 83,
     u'T': 84,
     u'U': 85,
     u'V': 86,
     u'W': 87,
     u'X': 88,
     u'Y': 89,
     u'Z': 90,
     u'a': 97,
     u'b': 98,
     u'c': 99,
     u'd': 100,
     u'e': 101,
     u'f': 102,
     u'g': 103,
     u'h': 104,
     u'i': 105,
     u'j': 106,
     u'k': 107,
     u'l': 108,
     u'm': 109,
     u'n': 110,
     u'o': 111,
     u'p': 112,
     u'q': 113,
     u'r': 114,
     u's': 115,
     u't': 116,
     u'u': 117,
     u'v': 118,
     u'w': 119,
     u'x': 120,
     u'y': 121,
     u'z': 122,
     u'@': 64,
     u' ': 32,
     u'!': 33,
     u'"': 34,
     u'.': 46,
     u',': 44,
     u':': 58,
     u';': 59,
     u'?': 63,
     u'<': 60,
     u'>': 62,
     u'[': 91,
     u']': 93,
     u'_': 95,
     u'-': 45,
     u'|': 124,
     u'&': 38,
     u'^': 94,
     u'~': 126,
     u'`': 96,
     u"'": 39,
     u'%': 37,
     u'(': 40,
     u')': 41,
     u'/': 47,
     u'\\': 92,
     u'*': 42,
     u'+': 43}

    def __init__(self, *a, **k):
        self._central_resource = _DisplayCentralResource(root_display=self, on_received_callback=self._on_central_resource_received, on_lost_callback=self._on_central_resource_lost)
        super(PhysicalDisplayElement, self).__init__(resource_type=self.nested_display_resource_factory(self), *a, **k)
        self._translation_table = self.ascii_translations
        self._message_header = None
        self._message_tail = None
        self._message_clear_all = None
        self._message_to_send = None
        self._last_sent_message = None
        self._block_messages = False
        self._send_message_task = self._tasks.add(task.run(self._send_message))
        self._send_message_task.kill()

    def nested_display_resource_factory(self, display):
        wrapper = ClientWrapper(wrap=lambda c: (display, c), unwrap=partial(maybe(second)))
        return const(ProxyResource(proxied_resource=self._central_resource, client_wrapper=wrapper))

    def _on_central_resource_received(self, display_client):
        display_client[1].set_control_element(display_client[0], True)
        self.update()

    def _on_central_resource_lost(self, display_client):
        display_client[1].set_control_element(display_client[0], False)
        self.update()

    @property
    @slicer(1)
    def subdisplay(self, char_slice):
        char_slice = to_slice(char_slice)
        return SubDisplayElement(sub_display_slice=char_slice, parent_display=self)

    def set_message_parts(self, header, tail):
        u"""
        Takes message parts as tuples containing the sysex bytes for
        each part of the message.
        """
        self._message_header = header
        self._message_tail = tail

    @property
    def message_header(self):
        return self._message_header

    @property
    def message_tail(self):
        return self._message_tail

    def set_clear_all_message(self, message):
        self._message_clear_all = message

    def set_translation_table(self, translation_table):
        assert u'?' in translation_table[u'?']
        self._translation_table = translation_table

    def set_block_messages(self, block):
        if block != self._block_messages:
            self._block_messages = block
        self.clear_send_cache()

    def display_message(self, message):
        if not self._block_messages:
            message = adjust_string(message, self._width)
            self._message_to_send = self._message_header + tuple(self._translate_string(message)) + self._message_tail
            self._request_send_message()

    def update(self):
        assert self._message_header is not None
        if len(self._logical_segments) > 0 and not self._block_messages:
            self._message_to_send = None
            self._request_send_message()

    def clear_send_cache(self):
        self._last_sent_message = None
        self._request_send_message()

    def reset(self):
        assert self._message_clear_all is not None or self._message_header is not None
        super(PhysicalDisplayElement, self).reset()
        if not self._block_messages:
            if self._message_clear_all != None:
                self._message_to_send = self._message_clear_all
            else:
                self._message_to_send = tuple(chain(self._message_header, self._translate_string(u' ' * int(self._width)), self._message_tail))
            self._request_send_message()

    def send_midi(self, midi_bytes):
        if midi_bytes != self._last_sent_message:
            ControlElement.send_midi(self, midi_bytes)
            self._last_sent_message = midi_bytes

    def _request_send_message(self):
        self._send_message_task.restart()

    def _send_message(self):
        if not self._block_messages:
            if self._message_to_send is None:
                self._message_to_send = self._build_message(list(map(first, self._central_resource.owners)))
            self.send_midi(self._message_to_send)

    def _translate_char(self, char_to_translate):
        result = 63
        if char_to_translate in self._translation_table.keys():
            result = self._translation_table[char_to_translate]
        else:
            result = self._translation_table[u'?']
        return result

    def _translate_string(self, string):
        return list(map(self._translate_char, string))

    @staticmethod
    def can_be_translated(translation_table, string):
        keys = translation_table.keys()
        return any([ char in keys for char in string ])

    def _build_display_message(self, display):
        message_string = display.display_string
        segments = display._logical_segments
        width_per_segment = display._width_per_segment

        def wrap_segment_message(message, segment):
            return chain(segment.position_identifier(), self._translate_string(message))

        return chain(*starmap(wrap_segment_message, zip(group(message_string, width_per_segment), segments)))

    def _build_inner_message(self, displays):
        message = list(self._build_display_message(self))
        for display in displays:
            message[display.display_slice] = self._build_display_message(display)

        return message

    def _build_message(self, displays):
        return tuple(chain(self._message_header, self._build_inner_message(displays), self._message_tail))


class SubDisplayElement(DisplayElement):

    def __init__(self, sub_display_slice = slice(1), parent_display = None, *a, **k):
        super(SubDisplayElement, self).__init__(width_in_chars=slice_size(sub_display_slice, parent_display.width), resource_type=parent_display.nested_display_resource_factory(self), *a, **k)
        self._sub_display_slice = sub_display_slice
        self._parent_display = parent_display

    @lazy_attribute
    def display_slice(self):
        return self._sub_display_slice

    @lazy_attribute
    def display_indexes(self):
        return set(range(*self._sub_display_slice.indices(self._parent_display.width)))

    def _is_visible(self):
        return self in list(map(first, self.resource.proxied_object.owners))

    def update(self):
        if self._is_visible():
            self._parent_display.update()
