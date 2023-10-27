# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\control_surface_mapping.py
# Compiled at: 2023-09-14 15:51:08
# Size of source mod 2**32: 4450 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ..base import Disconnectable
from .component_map import ComponentMap
from .layer import Layer
from .mode import EnablingAddLayerMode, ModesComponent

class ControlSurfaceMappingMixin(Disconnectable):

    def __init__(self, specification=None, *a, **k):
        self.component_map = ComponentMap(specification)
        (super().__init__)(*a, **k)

    def disconnect(self):
        super().disconnect()
        self.component_map = None

    def setup(self):
        self.component_map['Background'] = self._background
        self.component_map['Target_Track'] = self._target_track
        mappings = self.specification.create_mappings_function(self)
        component_names = self.component_map.keys()
        for name in list(mappings.keys()):
            if name in component_names:
                self._create_component(name, mappings.pop(name))

        for name, section in mappings.items():
            if name not in component_names:
                self._create_modes_component(name, section)

        for name, section in mappings.items():
            self._setup_modes_component(name, section)

    def _create_component(self, name, component_mappings):
        should_enable = component_mappings.pop('enable', True)
        component = self.component_map[name]
        component.layer = Layer(**component_mappings)
        component.set_enabled(should_enable)

    def _create_modes_component(self, name, modes_config):
        modes_component_type = modes_config.pop('modes_component_type', ModesComponent)
        component = modes_component_type(name=name,
          is_enabled=False,
          is_private=(modes_config.pop('is_private', False)),
          default_behaviour=(modes_config.pop('default_behaviour', None)),
          support_momentary_mode_cycling=(modes_config.pop('support_momentary_mode_cycling', True)))
        self.component_map[name] = component

    def _setup_modes_component(self, name, modes_config):
        should_enable = modes_config.pop('enable', True)
        component = self.component_map[name]
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