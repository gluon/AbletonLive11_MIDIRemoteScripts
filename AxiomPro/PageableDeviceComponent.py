#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/AxiomPro/PageableDeviceComponent.py
from __future__ import absolute_import, print_function, unicode_literals
from builtins import str
from builtins import range
import Live
from _Generic.Devices import *
from _Framework.DeviceComponent import DeviceComponent
from _Framework.EncoderElement import EncoderElement
from _Framework.ButtonElement import ButtonElement
from _Framework.DisplayDataSource import DisplayDataSource
SPECIAL_NAME_DICT = {u'InstrumentImpulse': ((u'Pad1', u'Pad2'),
                        (u'Pad3', u'Pad4'),
                        (u'Pad5', u'Pad6'),
                        (u'Pad7', u'Pad8')),
 u'Operator': ((u'OscA', u'OscB', u'OscC', u'OscD'),
               (u'LFO', u'Fltr'),
               (u'Pitch',),
               (u'Glob.',)),
 u'MultiSampler': ((u'Vol.', u'Pitch'),
                   (u'Fltr', u'FEnv'),
                   (u'LFO1', u'LFO2', u'LFO3'),
                   (u'Osc',)),
 u'UltraAnalog': ((u'Osc',),
                  (u'Fltr', u'FEnv', u'FMod'),
                  (u'VEnv', u'Mix'),
                  (u'Out',)),
 u'LoungeLizard': ((u'Ma&Ti',),
                   (u'To&Da',),
                   (u'Pick', u'Mod'),
                   (u'Glob.',)),
 u'StringStudio': ((u'Ex&St', u'Damp'),
                   (u'Te&Pi', u'Body'),
                   (u'Fltr', u'LFO'),
                   (u'Glob.', u'Vibr')),
 u'Eq8': ((u'Bands', u'EQ1-3'),
          (u'Freq', u'Gain'),
          (u'Reso', u'Fltr'),
          (u'Glob.',))}
SPECIAL_DEVICE_DICT = {u'InstrumentImpulse': [(IMP_BANK1, IMP_BANK2),
                        (IMP_BANK3, IMP_BANK4),
                        (IMP_BANK5, IMP_BANK6),
                        (IMP_BANK7, IMP_BANK8)],
 u'Operator': [(OPR_BANK1,
                OPR_BANK2,
                OPR_BANK3,
                OPR_BANK4),
               (OPR_BANK5, OPR_BANK6),
               (OPR_BANK7,),
               (OPR_BANK8,)],
 u'MultiSampler': [(SAM_BANK1, SAM_BANK8),
                   (SAM_BANK2, SAM_BANK3),
                   (SAM_BANK4, SAM_BANK5, SAM_BANK6),
                   (SAM_BANK7,)],
 u'UltraAnalog': [(ALG_BANK1,),
                  (ALG_BANK2, ALG_BANK3, ALG_BANK4),
                  (ALG_BANK5, ALG_BANK6),
                  (ALG_BANK7,)],
 u'LoungeLizard': [(ELC_BANK1,),
                   (ELC_BANK2,),
                   (ELC_BANK3, ELC_BANK4),
                   (ELC_BANK5,)],
 u'StringStudio': [(TNS_BANK1, TNS_BANK2),
                   (TNS_BANK3, TNS_BANK4),
                   (TNS_BANK6, TNS_BANK7),
                   (TNS_BANK8, TNS_BANK5)],
 u'Eq8': [(EQ8_BANK1, EQ8_BANK7),
          (EQ8_BANK2, EQ8_BANK3),
          (EQ8_BANK4, EQ8_BANK5),
          (EQ8_BANK6,)]}

class PageableDeviceComponent(DeviceComponent):
    u""" Class representing a device on the AxiomPro """

    def __init__(self, *a, **k):
        super(PageableDeviceComponent, self).__init__(*a, **k)
        self._parameter_value_data_source = DisplayDataSource()
        self._parameter_name_data_sources = []
        self._page_name_data_sources = []
        self._page_index = [0,
         0,
         0,
         0]
        for new_index in range(8):
            self._parameter_name_data_sources.append(DisplayDataSource())
            self._page_name_data_sources.append(DisplayDataSource())
            self._parameter_name_data_sources[-1].set_display_string(u' - ')
            self._page_name_data_sources[-1].set_display_string(u' - ')

    def disconnect(self):
        self._parameter_value_data_source = None
        self._parameter_name_data_sources = None
        self._page_name_data_sources = None
        DeviceComponent.disconnect(self)

    def set_device(self, device):
        DeviceComponent.set_device(self, device)
        if self._device == None:
            for source in self._parameter_name_data_sources:
                source.set_display_string(u' - ')

            for source in self._page_name_data_sources:
                source.set_display_string(u' - ')

    def set_bank_buttons(self, buttons):
        assert buttons == None or isinstance(buttons, tuple) and len(buttons) == 4
        DeviceComponent.set_bank_buttons(self, buttons)

    def set_parameter_controls(self, controls):
        assert controls == None or isinstance(controls, tuple) and len(controls) == 8
        if self._parameter_controls != None:
            for control in self._parameter_controls:
                if self._device != None:
                    control.release_parameter()

        self._parameter_controls = controls
        if self._parameter_controls != None:
            for control in self._parameter_controls:
                assert control != None
                assert isinstance(control, EncoderElement)

        self.update()

    def parameter_value_data_source(self):
        return self._parameter_value_data_source

    def parameter_name_data_source(self, index):
        assert index in range(8)
        return self._parameter_name_data_sources[index]

    def page_name_data_source(self, index):
        assert index in range(8)
        return self._page_name_data_sources[index]

    def _bank_value(self, value, button):
        assert self._bank_buttons != None
        assert value != None
        assert button != None
        assert isinstance(value, int)
        assert isinstance(button, ButtonElement)
        assert list(self._bank_buttons).count(button) == 1
        if self.is_enabled():
            if not button.is_momentary() or value is not 0:
                bank = list(self._bank_buttons).index(button)
                if self._device != None:
                    if bank != self._bank_index:
                        self._bank_index = bank
                    else:
                        self._page_index[bank] += 1
                    self.update()

    def _assign_parameters(self):
        assert self.is_enabled()
        assert self._device != None
        assert self._parameter_controls != None
        if self._device.class_name in list(SPECIAL_DEVICE_DICT.keys()):
            self.__assign_parameters_special()
        elif self._device.class_name in list(DEVICE_DICT.keys()):
            self.__assign_parameters_normal()
        else:
            self.__assign_parameters_plugin()
        self._parameter_value_data_source.set_display_string(u'')
        for index in range(len(self._parameter_controls)):
            if self._parameter_controls[index].mapped_parameter() != None:
                self._parameter_name_data_sources[index].set_display_string(self._parameter_controls[index].mapped_parameter().name)
            else:
                self._parameter_name_data_sources[index].set_display_string(u' - ')

    def __assign_parameters_special(self):
        u""" Assign the controls to the parameters of a device with more than 4 pages """
        banks = SPECIAL_DEVICE_DICT[self._device.class_name]
        bank_names = SPECIAL_NAME_DICT[self._device.class_name]
        pages = banks[self._bank_index]
        self._page_index[self._bank_index] %= len(pages)
        self._bank_name = bank_names[self._bank_index][self._page_index[self._bank_index]]
        page = pages[self._page_index[self._bank_index]]
        assert len(page) >= len(self._parameter_controls)
        for index in range(len(self._parameter_controls)):
            parameter = get_parameter_by_name(self._device, page[index])
            if parameter != None:
                self._parameter_controls[index].connect_to(parameter)
            else:
                self._parameter_controls[index].release_parameter()

        for index in range(len(self._page_name_data_sources)):
            if index < len(bank_names):
                page_names = bank_names[index]
                if index == self._bank_index:
                    self._page_name_data_sources[index].set_display_string(page_names[(self._page_index[index] + 1) % len(page_names)])
                else:
                    self._page_name_data_sources[index].set_display_string(page_names[self._page_index[index] % len(page_names)])
            else:
                self._page_name_data_sources[index].set_display_string(u' - ')

    def __assign_parameters_normal(self):
        u""" Assign the controls to the parameters of a device with 4 pages or less """
        assert self._device.class_name in list(DEVICE_BOB_DICT.keys())
        self._page_index[self._bank_index] = 0
        banks = DEVICE_DICT[self._device.class_name]
        bank_names = []
        if len(banks) > self._bank_index:
            if self._device.class_name in list(BANK_NAME_DICT.keys()) and len(BANK_NAME_DICT[self._device.class_name]) > 1:
                bank_names = BANK_NAME_DICT[self._device.class_name]
            bank = banks[self._bank_index]
            if self._bank_index in range(len(bank_names)):
                self._bank_name = bank_names[self._bank_index]
            else:
                self._bank_name = u'Bank ' + str(self._bank_index + 1)
            assert len(bank) >= len(self._parameter_controls)
            for index in range(len(self._parameter_controls)):
                parameter = get_parameter_by_name(self._device, bank[index])
                if parameter != None:
                    self._parameter_controls[index].connect_to(parameter)
                else:
                    self._parameter_controls[index].release_parameter()

        for index in range(len(self._page_name_data_sources)):
            if index < len(bank_names):
                self._page_name_data_sources[index].set_display_string(bank_names[index])
            else:
                self._page_name_data_sources[index].set_display_string(u' - ')

    def __assign_parameters_plugin(self):
        u""" Assign the controls to the parameters of a plugin """
        num_controls = len(self._parameter_controls)
        num_banks = min(8, number_of_parameter_banks(self._device))
        num_double_pages = 0
        num_double_pages_before = 0
        parameters_to_use = self._device.parameters[1:]
        self._bank_name = u'Bank ' + str(self._bank_index + 1)
        if num_banks > 4:
            num_double_pages = num_banks - 4
        if self._bank_index < num_double_pages:
            self._page_index[self._bank_index] %= 2
            num_double_pages_before = self._bank_index
        else:
            self._page_index[self._bank_index] = 0
            num_double_pages_before = num_double_pages
        if self._bank_index + num_double_pages_before < num_banks:
            bank_offset = (self._bank_index + num_double_pages_before) * num_controls
            page_offset = bank_offset + self._page_index[self._bank_index] * num_controls
            for control in self._parameter_controls:
                if page_offset < len(parameters_to_use):
                    control.connect_to(parameters_to_use[page_offset])
                else:
                    control.release_parameter()
                page_offset += 1

            bank_names = []
            parameter_offset = 0
            for index in range(4):
                display_string = u' - '
                if index < num_banks:
                    if index < num_double_pages:
                        add_offset_before = index == self._bank_index and self._page_index[index] == 0 or index != self._bank_index and self._page_index[index] != 0
                        if add_offset_before:
                            parameter_offset += num_controls
                        display_string = str(parameter_offset + 1).rjust(2) + u'-' + str(parameter_offset + num_controls).rjust(2)
                        if not add_offset_before:
                            parameter_offset += num_controls
                    else:
                        display_string = str(parameter_offset + 1).rjust(2) + u'-' + str(parameter_offset + num_controls).rjust(2)
                self._page_name_data_sources[index].set_display_string(display_string)
                parameter_offset += num_controls
