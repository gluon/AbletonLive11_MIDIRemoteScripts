# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\component_map.py
# Compiled at: 2023-09-14 15:51:08
# Size of source mod 2**32: 3832 bytes
from __future__ import absolute_import, print_function, unicode_literals
from functools import partial
from . import Component
from .components import AccentComponent, ActiveParameterComponent, ClipActionsComponent, DeviceComponent, DrumGroupComponent, MixerComponent, ModifierBackgroundComponent, RecordingComponent, SessionComponent, SessionNavigationComponent, SessionOverviewComponent, SimpleDeviceNavigationComponent, SlicedSimplerComponent, TranslatingBackgroundComponent, TransportComponent, UndoRedoComponent, ViewBasedRecordingComponent, ViewControlComponent, ViewToggleComponent

class ComponentMap(dict):

    def __init__(self, specification, *a, **k):
        (super().__init__)(*a, **k)
        self._create_component_map(specification)

    def get(self, key, **_):
        return self.__getitem__(key)

    def __getitem__(self, key):
        component_or_factory = super().__getitem__(key)
        if isinstance(component_or_factory, Component):
            return component_or_factory
        component = component_or_factory(is_enabled=False)
        self[key] = component
        return component

    def __contains__(self, key):
        return isinstance(super().get(key), Component)

    def _create_component_map(self, specification):
        self['Accent'] = AccentComponent
        self['Active_Parameter'] = ActiveParameterComponent
        self['Clip_Actions'] = ClipActionsComponent
        self['Device'] = partial(DeviceComponent,
          bank_definitions=(specification.parameter_bank_definitions),
          bank_size=(specification.parameter_bank_size),
          continuous_parameter_sensitivity=(specification.continuous_parameter_sensitivity),
          quantized_parameter_sensitivity=(specification.quantized_parameter_sensitivity))
        self['Device_Navigation'] = SimpleDeviceNavigationComponent
        self['Drum_Group'] = DrumGroupComponent
        self['Mixer'] = MixerComponent
        self['Modifier_Background'] = ModifierBackgroundComponent
        self['Recording'] = partial(RecordingComponent,
          recording_method_type=(specification.recording_method_type))
        self['Session'] = SessionComponent
        self['Session_Navigation'] = partial(SessionNavigationComponent,
          snap_track_offset=(specification.snap_track_offset))
        self['Session_Overview'] = SessionOverviewComponent
        self['Sliced_Simpler'] = SlicedSimplerComponent
        self['Translating_Background'] = TranslatingBackgroundComponent
        self['Transport'] = TransportComponent
        self['Undo_Redo'] = UndoRedoComponent
        self['View_Based_Recording'] = partial(ViewBasedRecordingComponent,
          recording_method_type=(specification.recording_method_type))
        self['View_Control'] = ViewControlComponent
        self['View_Toggle'] = ViewToggleComponent
        self.update(specification.component_map)