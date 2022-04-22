# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v3/control_surface/elements_base.py
# Compiled at: 2022-01-28 05:06:24
# Size of source mod 2**32: 10935 bytes
from __future__ import absolute_import, print_function, unicode_literals
from functools import partial
import Live
from ..base import chunks, depends, flatten, is_iterable, recursive_map
from . import ControlElement, PrioritizedResource
from .elements import ButtonElement, ButtonMatrixElement, ComboElement, EncoderElement, SysexElement

class MapMode:
    Absolute = Live.MidiMap.MapMode.absolute
    Absolute14Bit = Live.MidiMap.MapMode.absolute_14_bit
    AccelSignedBit = Live.MidiMap.MapMode.relative_signed_bit
    AccelSignedBit2 = Live.MidiMap.MapMode.relative_signed_bit2
    AccelBinaryOffset = Live.MidiMap.MapMode.relative_binary_offset
    AccelTwoCompliment = Live.MidiMap.MapMode.relative_two_compliment
    LinearSignedBit = Live.MidiMap.MapMode.relative_smooth_signed_bit
    LinearSignedBit2 = Live.MidiMap.MapMode.relative_smooth_signed_bit2
    LinearBinaryOffset = Live.MidiMap.MapMode.relative_smooth_binary_offset
    LinearTwoCompliment = Live.MidiMap.MapMode.relative_smooth_two_compliment


@depends(skin=None)
def create_button(identifier, name, **k):
    return ButtonElement(identifier, name=name, **k)


def create_encoder(identifier, name, **k):
    return EncoderElement(identifier, name=name, **k)


def create_sysex_element(identifier, name, send_message_generator=None, **k):
    return SysexElement(sysex_identifier=identifier, 
     send_message_generator=send_message_generator, 
     name=name, **k)


def create_combo_element(control=None, modifier=None, name=None):
    if not name:
        name = create_name_for_modified_control(control=control, modifier=modifier)
    return ComboElement(control=control, modifier=modifier, name=name)


def create_matrix_identifiers(start, stop, width=1, flip_rows=False):
    rows = list(chunks(list(range(start, stop)), width))
    if flip_rows:
        rows.reverse()
    return rows


def create_name_for_modified_control(control=None, modifier=None):
    modifier_name = modifier.name
    if modifier_name.lower().endswith('button'):
        modifier_name = modifier_name[:-7]
    preposition = 'With' if control.name[0].isupper() else 'with'
    return '{}_{}_{}'.format(control.name, preposition, modifier_name)


class ElementsBase:

    def __init__(self, global_channel=0, *a, **k):
        (super().__init__)(*a, **k)
        self._global_channel = global_channel

    def add_button(self, identifier, name, **k):
        attr_name = self._create_attribute_name(name)
        k['channel'] = k.get('channel', self._global_channel)
        setattr(self, attr_name, create_button(identifier, name, **k))

    def add_encoder(self, identifier, name, **k):
        attr_name = self._create_attribute_name(name)
        k['channel'] = k.get('channel', self._global_channel)
        setattr(self, attr_name, create_encoder(identifier, name, **k))

    def add_sysex_element(self, identifier, name, send_message_generator=None, **k):
        attr_name = self._create_attribute_name(name)
        setattr(self, attr_name, create_sysex_element(identifier, name, send_message_generator, **k))

    def add_element(self, name, element_factory, *a, **k):
        attr_name = self._create_attribute_name(name)
        setattr(self, attr_name, element_factory(a, name=name, **k))

    def add_modifier_button(self, identifier, name, *a, **k):
        (self.add_button)(identifier, name, *a, resource_type=PrioritizedResource, **k)

    def add_modified_control(self, control=None, modifier=None, name=None):
        if isinstance(control, ButtonMatrixElement):
            self._add_modified_matrix(control, modifier, name=name)
        else:
            element = create_combo_element(control=control, modifier=modifier, name=name)
            attr_name = self._create_attribute_name(element.name)
            setattr(self, attr_name, element)

    def add_matrix(self, identifiers, base_name, channels=None, element_factory=create_button, **k):
        channels = channels if channels is not None else self._global_channel
        if not is_iterable(channels):
            channels = [[channels] * len(row) for row in identifiers]
        sub_element_name = base_name[:-1] if base_name.endswith('s') else base_name

        def one_dimensional_name(x, _):
            return '{}_{}'.format(sub_element_name, x)

        def two_dimensional_name(x, y):
            return '{}_{}_{}'.format(x, sub_element_name, y)

        name_factory = two_dimensional_name if len(identifiers) > 1 else one_dimensional_name
        elements = [[element_factory(identifier, name=name_factory(column, row), channel=channel, **k) for column, (identifier, channel) in enumerate(zip(inner_identifiers, inner_channels))] for row, (inner_identifiers, inner_channels) in enumerate(zip(identifiers, channels))]
        attr_name = self._create_attribute_name(base_name)
        self._add_raw_elements(attr_name, elements)
        setattr(self, attr_name, ButtonMatrixElement(name=base_name, rows=elements))

    def add_button_matrix(self, identifiers, base_name, channels=None, *a, **k):
        (self.add_matrix)(
 identifiers, 
 base_name, *a, channels=channels, element_factory=create_button, **k)

    def add_encoder_matrix(self, identifiers, base_name, channels=None, *a, **k):
        (self.add_matrix)(
 identifiers, 
 base_name, *a, channels=channels, element_factory=create_encoder, **k)

    def add_submatrix(self, matrix, name, columns=None, rows=None):
        if not columns:
            columns = (
             0, matrix.width() + 1)
        if not rows:
            rows = (
             0, matrix.height() + 1)
        submatrix = matrix.submatrix[columns[0]:columns[1], rows[0]:rows[1]]
        submatrix.name = name
        attr_name = self._create_attribute_name(name)
        setattr(self, attr_name, submatrix)

    def _add_modified_matrix(self, matrix, modifier, name):
        modified_elements = recursive_map(partial(create_combo_element, modifier=modifier), matrix._orig_buttons)
        if not name:
            name = create_name_for_modified_control(control=matrix, modifier=modifier)
        attr_name = self._create_attribute_name(name)
        self._add_raw_elements(attr_name, modified_elements)
        setattr(self, attr_name, ButtonMatrixElement(name=name, rows=modified_elements))

    def _add_raw_elements(self, base_name, elements):
        setattr(self, '{}_raw'.format(base_name), list(flatten(elements)))

    def _create_attribute_name(self, name):
        attr_name = name.lower().replace(' ', '_')
        return attr_name