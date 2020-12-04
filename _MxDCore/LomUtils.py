#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/_MxDCore/LomUtils.py
from __future__ import absolute_import, print_function, unicode_literals
from past.builtins import basestring
from builtins import filter
from builtins import object
import sys
import types
from itertools import chain
from ableton.v2.base import old_hasattr
from .MxDUtils import TupleWrapper
from .LomTypes import cs_base_classes, TUPLE_TYPES, PROPERTY_TYPES, EXTRA_CS_FUNCTIONS, ENUM_TYPES, ROOT_KEYS, LIVE_APP, MFLPropertyFormats, LomObjectError, LomAttributeError, get_exposed_property_names_for_type, get_exposed_property_info, is_class, get_root_prop, is_lom_object, is_cplusplus_lom_object, is_object_iterable

def create_lom_doc_string(lom_object):
    description = u''
    if old_hasattr(lom_object, u'__doc__') and isinstance(lom_object.__doc__, basestring) and len(lom_object.__doc__) > 0:
        description = u'description %s' % lom_object.__doc__.replace(u'\n', u' ').replace(u',', u'\\,')
    return description


class LomInformation(object):
    u""" Class that extracts information from a given LOM object """

    def __init__(self, lom_object, epii_version, *a, **k):
        super(LomInformation, self).__init__(*a, **k)
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
            property_names = list(filter(lambda prop: not prop.startswith(u'_'), dir(lom_object)))
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
                    self._properties.append((prop_name, u'dict'))
                elif prop_name in TUPLE_TYPES:
                    self._add_list_of_children(prop_name)
                elif prop_name in list(PROPERTY_TYPES.keys()):
                    self._add_child(real_prop, prop_name)
                elif prop_name == u'canonical_parent':
                    if real_prop != None:
                        self._children.append((prop_name, prop_type))
                elif callable(real_prop):
                    if not prop_name.endswith(u'_listener'):
                        self._functions.append((prop_name,))
                elif prop_type == u'unicode' or prop_type == u'str':
                    self._properties.append((prop_name, u'str'))
                elif prop_type not in (u'type', u'Enum'):
                    info_type = u'int' if isinstance(real_prop, ENUM_TYPES) else prop_type
                    self._properties.append((prop_name, info_type))
        except (AssertionError, RuntimeError):
            pass


class LomIntrospection(object):

    def __init__(self, directory, exclude = [], *a, **k):
        super(LomIntrospection, self).__init__(*a, **k)
        self._lom_classes = []
        self._lom_modules = []
        self._excluded = exclude
        self._create_introspection_for_dir(directory)

    @property
    def lom_classes(self):
        return self._lom_classes

    def _is_relevant_class(self, class_object):
        return is_class(class_object) and old_hasattr(class_object, u'__module__') and sys.modules.get(class_object.__module__) in self._lom_modules and class_object not in self._lom_classes and class_object not in self._excluded

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


def is_control_surfaces_list(path_component):
    return path_component in (u'cs', u'control_surfaces')


def wrap_control_surfaces_list(parent):
    assert parent in (None, get_root_prop(None, LIVE_APP))
    return TupleWrapper.get_tuple_wrapper(parent, u'control_surfaces', element_filter=lambda e: isinstance(e, cs_base_classes()))


class LomPathCalculator(object):

    def __init__(self, lom_object, external_device, *a, **k):
        super(LomPathCalculator, self).__init__(*a, **k)
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
            elif lom_object in root_prop:
                index = list(root_prop).index(lom_object)
                component = u'%s %d' % (key, index)
                break

        return component

    def _find_property_object_path(self, lom_object, parent):
        component = None
        for key in list(PROPERTY_TYPES.keys()):
            if isinstance(lom_object, PROPERTY_TYPES[key]) and old_hasattr(parent, key):
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
                    component = u'%s %d' % (key, index)
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

    def __init__(self, path_components, external_device, lom_classes, list_manager, *a, **k):
        super(LomPathResolver, self).__init__(*a, **k)
        self._external_device = external_device
        self._lom_classes = lom_classes
        self._list_manager = list_manager
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
            lom_object = wrap_control_surfaces_list(parent)
        elif parent != None and old_hasattr(parent, attribute):
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
                    assert is_object_iterable(lom_object)
                    assert prev_component in list(TUPLE_TYPES.keys())
                    index = int(component)
                    if is_control_surfaces_list(prev_component):
                        parent = components[-2] if len(components) > 1 else None
                        tuple_wrapper = wrap_control_surfaces_list(parent)
                        lom_object = tuple_wrapper.get_list()[index]
                    else:
                        lom_object = lom_object[index]
                else:
                    lom_object = getattr(lom_object, component)
                components.append(lom_object)
            except IndexError:
                raise LomAttributeError(u"invalid index of component '%s'" % prev_component)
            except AttributeError:
                raise LomAttributeError(u"invalid path component '%s'" % component)
            else:
                prev_component = component

        if not is_lom_object(lom_object, self._lom_classes):
            raise LomObjectError(u"component '%s' is not an object" % prev_component)
        return lom_object

    def _calculate_object_from_path(self, path_components):
        lom_object = None
        if len(path_components) > 0:
            assert path_components[0] in ROOT_KEYS
            selector = self._tuple_element_from_path if path_components[-1] in list(TUPLE_TYPES.keys()) else self._property_object_from_path
            lom_object = selector(path_components)
        return lom_object
