from __future__ import absolute_import, print_function, unicode_literals
from functools import partial
from ableton.v3.control_surface import Component
from ableton.v3.control_surface.components import AccentComponent, ClipActionsComponent, DeviceComponent, DrumGroupComponent, MixerComponent, ModifierBackgroundComponent, SessionComponent, SessionNavigationComponent, SessionOverviewComponent, SimpleDeviceNavigationComponent, SlicedSimplerComponent, TranslatingBackgroundComponent, TransportComponent, UndoRedoComponent, ViewControlComponent, ViewToggleComponent

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
        component.num_layers = 0
        self[key] = component
        return component

    def __contains__(self, key):
        return isinstance(super().get(key), Component)

    def _create_component_map(self, specification):
        self['Accent'] = AccentComponent
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
        self['Session'] = SessionComponent
        self['Session_Navigation'] = SessionNavigationComponent
        self['Session_Overview'] = SessionOverviewComponent
        self['Sliced_Simpler'] = SlicedSimplerComponent
        self['Translating_Background'] = TranslatingBackgroundComponent
        self['Transport'] = TransportComponent
        self['Undo_Redo'] = UndoRedoComponent
        self['View_Control'] = ViewControlComponent
        self['View_Toggle'] = ViewToggleComponent
        self.update(specification.component_map)