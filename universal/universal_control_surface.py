from __future__ import absolute_import, print_function, unicode_literals
from ableton.v3.control_surface import BANK_DEFINITIONS, DEFAULT_BANK_SIZE, DEFAULT_CONTINUOUS_PARAMETER_SENSITIVITY, DEFAULT_QUANTIZED_PARAMETER_SENSITIVITY, ControlSurface, ControlSurfaceSpecification, Layer
from .component_map import ComponentMap
from .mode import EnablingAddLayerMode, ModesComponent

def create_ucs_instance(name=None, specification=None, c_instance=None):
    return type(name, (UniversalControlSurface,), {})(specification,
      c_instance=c_instance)


class UniversalControlSurfaceSpecification(ControlSurfaceSpecification):
    create_mappings_function = lambda *x: {}
    component_map = {}
    parameter_bank_definitions = BANK_DEFINITIONS
    parameter_bank_size = DEFAULT_BANK_SIZE
    continuous_parameter_sensitivity = DEFAULT_CONTINUOUS_PARAMETER_SENSITIVITY
    quantized_parameter_sensitivity = DEFAULT_QUANTIZED_PARAMETER_SENSITIVITY


class UniversalControlSurface(ControlSurface):

    def __init__(self, specification, *a, **k):
        self.component_map = ComponentMap(specification)
        (super().__init__)(a, specification=specification, **k)

    def disconnect(self):
        super().disconnect()
        self.component_map = None

    def setup(self):
        self.component_map['Background'] = self._background
        self.component_map['Target_Track'] = self._target_track
        mappings = self.specification.create_mappings_function(self)
        component_names = self.component_map.keys()
        for name, section in mappings.items():
            if name in component_names:
                self._create_component(name, section)

        for name, section in mappings.items():
            if name not in component_names:
                self._create_modes_component(name, section)

    def _create_component(self, name, component_mappings):
        component = self.component_map[name]
        component.layer = Layer(**component_mappings)
        component.num_layers = 1
        component.set_enabled(True)

    def _create_modes_component(self, name, modes_config):
        should_enable = modes_config.pop('enable', True)
        component = ModesComponent(name=name,
          is_enabled=False,
          default_behaviour=(modes_config.pop('default_behaviour', None)),
          support_momentary_mode_cycling=(modes_config.pop('support_momentary_mode_cycling', True)))
        self.component_map[name] = component
        mode_control_layer = {}
        for mode_or_control_name, mode_or_element in modes_config.items():
            if isinstance(mode_or_element, str):
                mode_control_layer[mode_or_control_name] = mode_or_element
                continue
            else:
                self._add_mode(mode_or_control_name, mode_or_element, component)

        component.layer = Layer(**mode_control_layer)
        if component.selected_mode is None:
            component.selected_mode = component.modes[0]
        component.set_enabled(should_enable)

    def _add_mode(self, mode_name, mode_spec, modes_component):
        is_dict = isinstance(mode_spec, dict)
        behaviour = mode_spec.pop('behaviour', None) if is_dict else None
        selector = mode_spec.pop('selector', None) if is_dict else None
        mode = mode_spec
        if is_dict:
            if 'modes' in mode_spec:
                mode = [self._create_mode_part(m) for m in mode_spec.pop('modes')]
            else:
                mode = self._create_mode_part(mode_spec)
        modes_component.add_mode(mode_name, mode, behaviour=behaviour, selector=selector)

    def _create_mode_part(self, mode_mappings):
        if isinstance(mode_mappings, dict):
            component = self.component_map[mode_mappings.pop('component')]
            if mode_mappings:
                return EnablingAddLayerMode(component=component,
                  layer=Layer(**mode_mappings))
            return component
        return mode_mappings