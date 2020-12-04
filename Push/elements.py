#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Push/elements.py
from __future__ import absolute_import, print_function, unicode_literals
from functools import partial
from ableton.v2.base import recursive_map
from ableton.v2.control_surface.elements import ButtonMatrixElement, ComboElement, SysexElement
from pushbase import consts
from pushbase.control_element_factory import create_note_button, make_send_message_generator
from pushbase.elements import Elements as ElementsBase
from pushbase.touch_strip_element import TouchStripElement
from .parameter_mapping_sensitivities import CONTINUOUS_MAPPING_SENSITIVITY, FINE_GRAINED_CONTINUOUS_MAPPING_SENSITIVITY
from .special_physical_display import SpecialPhysicalDisplay
from . import sysex

class Elements(ElementsBase):

    def __init__(self, *a, **k):
        super(Elements, self).__init__(continuous_mapping_sensitivity=CONTINUOUS_MAPPING_SENSITIVITY, fine_grained_continuous_mapping_sensitivity=FINE_GRAINED_CONTINUOUS_MAPPING_SENSITIVITY, *a, **k)
        self.display_line1 = self._create_display_line(sysex.CLEAR_LINE1, sysex.WRITE_LINE1, 0)
        self.display_line2 = self._create_display_line(sysex.CLEAR_LINE2, sysex.WRITE_LINE2, 1)
        self.display_line3 = self._create_display_line(sysex.CLEAR_LINE3, sysex.WRITE_LINE3, 2)
        self.display_line4 = self._create_display_line(sysex.CLEAR_LINE4, sysex.WRITE_LINE4, 3)
        self.display_lines = [self.display_line1,
         self.display_line2,
         self.display_line3,
         self.display_line4]
        with_shift = partial(ComboElement, modifier=self.shift_button)
        self.shifted_matrix = ButtonMatrixElement(name=u'Shifted_Button_Matrix', rows=recursive_map(with_shift, self.matrix_rows_raw))
        touch_strip_mode_element = SysexElement(send_message_generator=sysex.make_touch_strip_mode_message)
        touch_strip_light_element = SysexElement(send_message_generator=sysex.make_touch_strip_light_message)
        self.touch_strip_tap = create_note_button(12, u'Touch_Strip_Tap')
        self.touch_strip_control = TouchStripElement(name=u'Touch_Strip_Control', touch_button=self.touch_strip_tap, mode_element=touch_strip_mode_element, light_element=touch_strip_light_element)
        self.touch_strip_control.set_feedback_delay(-1)
        self.touch_strip_control.set_needs_takeover(False)
        base_message_generator = make_send_message_generator(sysex.SET_AFTERTOUCH_MODE)

        def make_aftertouch_mode_message(mode_id):
            assert mode_id in (u'polyphonic', u'mono')
            mode_message = sysex.POLY_AFTERTOUCH if mode_id == u'polyphonic' else sysex.MONO_AFTERTOUCH
            return base_message_generator(mode_message)

        self.aftertouch_control = SysexElement(sysex_identifier=sysex.SET_AFTERTOUCH_MODE, send_message_generator=make_aftertouch_mode_message, default_value=u'polyphonic')

    def _create_display_line(self, clear_cmd, write_cmd, index):
        line = SpecialPhysicalDisplay(consts.DISPLAY_LENGTH, 1)
        line.set_clear_all_message(clear_cmd)
        line.set_message_parts(write_cmd, (247,))
        line.name = u'Display_Line_%d' % index
        line.reset()
        return line
