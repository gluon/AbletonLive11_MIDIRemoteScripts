# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_MxDCore\LomUtils.py
# Compiled at: 2023-10-06 16:19:02
# Size of source mod 2**32: 14987 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import filter, object
from past.builtins import basestring
import sys, types
from itertools import chain
from ableton.v2.base import old_hasattr
from .ControlSurfaceWrapper import is_real_control_surface
from .LomTypes import ENUM_TYPES, EXTRA_CS_FUNCTIONS, LIVE_APP, PROPERTY_TYPES, ROOT_KEYS, TUPLE_TYPES, LomAttributeError, LomObjectError, MFLPropertyFormats, cs_base_classes, get_control_surfaces, get_exposed_property_info, get_exposed_property_names_for_type, get_root_prop, is_class, is_cplusplus_lom_object, is_lom_object, is_object_iterable
from .MxDUtils import TupleWrapper

def create_lom_doc_string(lom_object):
    description = ''
    if old_hasattr(lom_object, '__doc__'):
        if isinstance(lom_object.__doc__, basestring):
            if len(lom_object.__doc__) > 0:
                description = 'description %s' % lom_object.__doc__.replace('\n', ' ').replace(',', '\\,')
    return description


class LomInformation(object):

    def __init__(self, lom_object, epii_version, *a, **k):
        (super(LomInformation, self).__init__)(*a, **k)
        self._lists_of_children = []
        self._children = []
        self._functions = []
        self._properties = []
        self._description = create_lom_doc_string(lom_object)
        self._generate_object_info(lom_object, epii_version)

    @property
    def description(self):
        return self._description

    @property
    def lists_of_children(self):
        return tuple(self._lists_of_children)

    @property
    def children(self):
        return tuple(self._children)

    @property
    def functions(self):
        return tuple(self._functions)

    @property
    def properties(self):
        return tuple(self._properties)

    def _add_list_of_children(self, prop_name):
        type_name = TUPLE_TYPES[prop_name].__name__
        self._lists_of_children.append((prop_name, type_name))

    def _add_child(self, real_prop, prop_name):
        type_name = (real_prop.__class__ if real_prop != None else PROPERTY_TYPES[prop_name]).__name__
        self._children.append((prop_name, type_name))

    def _generate_object_info(self, lom_object, epii_version):
        if isinstance(lom_object, cs_base_classes()):
            property_names = list(filter(lambda prop: not prop.startswith('_')
, dir(lom_object)))
            functions_implemented_by_mxdcore = EXTRA_CS_FUNCTIONS
        else:
            property_names = get_exposed_property_names_for_type(type(lom_object), epii_version)
            functions_implemented_by_mxdcore = []
        for name in property_names:
            self._generate_property_info(name, lom_object, epii_version)

        if functions_implemented_by_mxdcore:
            for function_name in functions_implemented_by_mxdcore:
                self._functions.append((function_name,))

            self._functions.sort()

    def _generate_property_info(self, prop_name, lom_object, epii_version):
        try:
            real_prop = getattr(lom_object, prop_name)
            if not is_class(real_prop):
                prop_info = get_exposed_property_info(type(lom_object), prop_name, epii_version)
                prop_type = real_prop.__class__.__name__
                if prop_info and prop_info.format == MFLPropertyFormats.JSON:
                    self._properties.append((prop_name, 'dict'))
                else:
                    if prop_name in TUPLE_TYPES:
                        self._add_list_of_children(prop_name)
                    else:
                        if prop_name in list(PROPERTY_TYPES.keys()):
                            self._add_child(real_prop, prop_name)
                        else:
                            if prop_name == 'canonical_parent':
                                if real_prop != None:
                                    self._children.append((prop_name, prop_type))
                            else:
                                if callable(real_prop):
                                    if not prop_name.endswith('_listener'):
                                        self._functions.append((prop_name,))
                                else:
                                    if prop_type == 'unicode' or prop_type == 'str':
                                        self._properties.append((prop_name, 'str'))
                                    else:
                                        if prop_type not in ('type', 'Enum'):
                                            info_type = 'int' if isinstance(real_prop, ENUM_TYPES) else prop_type
                                            self._properties.append((prop_name, info_type))
        except (AssertionError, RuntimeError):
            pass


class LomIntrospection(object):

    def __init__(self, directory, exclude=[], *a, **k):
        (super(LomIntrospection, self).__init__)(*a, **k)
        self._lom_classes = []
        self._lom_modules = []
        self._excluded = exclude
        self._create_introspection_for_dir(directory)

    @property
    def lom_classes(self):
        return self._lom_classes

    def _is_relevant_class(self, class_object):
        return is_class(class_object) and old_hasattr(class_object, '__module__') and sys.modules.get(class_object.__module__) in self._lom_modules and class_object not in self._lom_classes and class_object not in self._excluded

    def _process_class(self, class_object):
        processed = False
        if self._is_relevant_class(class_object):
            self._lom_classes.append(class_object)
            processed = True
        return processed

    def _is_relevant_module(self, module_object):
        return isinstance(module_object, types.ModuleType) and module_object not in self._lom_modules

    def _process_module(self, module_object):
        processed = False
        if self._is_relevant_module(module_object):
            self._lom_modules.append(module_object)
            processed = True
        return processed

    def _create_introspection_for_module_or_class(self, attribute):
        self._process_class(attribute)
        for sub_attr_name in dir(attribute):
            try:
                sub_attribute = getattr(attribute, sub_attr_name)
                if self._process_class(sub_attribute):
                    for sub_sub_attr_name in dir(sub_attribute):
                        try:
                            self._process_class(getattr(sub_attribute, sub_sub_attr_name))
                        except:
                            pass

            except:
                pass

    def _create_introspection_for_dir(self, directory):
        for attr_name in list(dir(directory)):
            try:
                attribute = getattr(directory, attr_name)
                if attribute not in self._excluded:
                    if self._process_module(attribute) or is_class(attribute):
                        self._create_introspection_for_module_or_class(attribute)
            except:
                pass


class TopLevelControlSurfaceListParent:

    @property
    def control_surfaces(self):
        return get_control_surfaces()


_control_surface_list_parent = TopLevelControlSurfaceListParent()

def is_control_surfaces_list(path_component):
    return path_component in ('cs', 'control_surfaces')


def wrap_control_surfaces_list(parent, cs_wrapper_registry):
    global _control_surface_list_parent
    return TupleWrapper.get_tuple_wrapper((parent if parent is not None else _control_surface_list_parent),
      'control_surfaces',
      element_filter=is_real_control_surface,
      element_transform=(cs_wrapper_registry.wrap))


class LomPathCalculator(object):

    def __init__(self, lom_object, external_device, *a, **k):
        (super(LomPathCalculator, self).__init__)(*a, **k)
        self._path_components = self._calculate_path(lom_object, external_device)

    @property
    def path_components(self):
        return self._path_components

    def _find_root_object_path(self, external_device, lom_object):
        component = None
        for key in ROOT_KEYS:
            root_prop = get_root_prop(external_device, key)
            if not is_object_iterable(root_prop):
                if lom_object == root_prop:
                    component = key
                    break
            else:
                if lom_object in root_prop:
                    index = list(root_prop).index(lom_object)
                    component = '%s %d' % (key, index)
                    break

        return component

    def _find_property_object_path(self, lom_object, parent):
        component = None
        for key in list(PROPERTY_TYPES.keys()):
            if isinstance(lom_object, PROPERTY_TYPES[key]):
                if old_hasattr(parent, key):
                    if lom_object == getattr(parent, key):
                        component = key
                        break

        return component

    def _find_tuple_element_object_path(self, lom_object, parent):
        component = None
        for key in sorted(list(TUPLE_TYPES.keys())):
            if old_hasattr(parent, key):
                property = getattr(parent, key)
                if lom_object in property:
                    index = list(property).index(lom_object)
                    component = '%s %d' % (key, index)
                    break

        return component

    def _prepend_path_component(self, component, components):
        if component != None:
            return [component] + components
        return []

    def _calculate_path(self, lom_object, external_device_getter):
        components = []
        while lom_object != None:
            component = None
            parent = lom_object.canonical_parent
            if parent != None:
                component = self._find_property_object_path(lom_object, parent) or self._find_tuple_element_object_path(lom_object, parent)
                components = self._prepend_path_component(component, components)
                if components == []:
                    break
            else:
                component = self._find_root_object_path(external_device_getter, lom_object)
                components = self._prepend_path_component(component, components)
                break
            lom_object = parent

        return components


class LomPathResolver(object):

    def __init__(self, path_components, external_device, lom_classes, list_manager, cs_wrapper_registry=None, *a, **k):
        (super(LomPathResolver, self).__init__)(*a, **k)
        self._external_device = external_device
        self._lom_classes = lom_classes
        self._list_manager = list_manager
        self._cs_wrapper_registry = cs_wrapper_registry
        self._lom_object = self._calculate_object_from_path(path_components)

    @property
    def lom_object(self):
        return self._lom_object

    def _tuple_element_from_path(self, path_components):
        lom_object = None
        parent = None
        attribute = path_components[-1]
        if len(path_components) > 1:
            parent = self._calculate_object_from_path(path_components[:-1])
        if is_control_surfaces_list(attribute):
            lom_object = wrap_control_surfaces_list(parent, self._cs_wrapper_registry)
        else:
            if parent != None:
                if old_hasattr(parent, attribute):
                    selector = self._list_manager.get_list_wrapper if is_cplusplus_lom_object(parent) else TupleWrapper.get_tuple_wrapper
                    lom_object = selector(parent, attribute)
        return lom_object

    def _property_object_from_path(self, path_components):
        prev_component = path_components[0]
        lom_object = get_root_prop(self._external_device, path_components[0])
        components = [lom_object]
        for component in path_components[1:]:
            try:
                if component.isdigit():
                    index = int(component)
                    if is_control_surfaces_list(prev_component):
                        parent = components[-2] if len(components) > 1 else None
                        tuple_wrapper = wrap_control_surfaces_list(parent, self._cs_wrapper_registry)
                        lom_object = tuple_wrapper.get_list()[index]
                    else:
                        lom_object = lom_object[index]
                else:
                    lom_object = getattr(lom_object, component)
                components.append(lom_object)
            except IndexError:
                raise LomAttributeError("invalid index of component '%s'" % prev_component)
            except AttributeError:
                raise LomAttributeError("invalid path component '%s'" % component)
            else:
                prev_component = component

        if not is_lom_object(lom_object, self._lom_classes):
            raise LomObjectError("component '%s' is not an object" % prev_component)
        return lom_object

    def _calculate_object_from_path(self, path_components):
        lom_object = None
        if len(path_components) > 0:
            selector = self._tuple_element_from_path if path_components[-1] in list(TUPLE_TYPES.keys()) else self._property_object_from_path
            lom_object = selector(path_components)
        return lom_object