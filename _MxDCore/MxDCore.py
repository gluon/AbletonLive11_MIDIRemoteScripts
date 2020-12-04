#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/_MxDCore/MxDCore.py
from __future__ import absolute_import, print_function, unicode_literals
from builtins import str
from builtins import map
from builtins import range
from builtins import object
from future.utils import string_types
import json
import logging
import Live.Base
from functools import partial, reduce, wraps
from ableton.v2.base import old_hasattr, PY2
import _Framework
from _Framework.Disconnectable import Disconnectable
from .MxDUtils import TupleWrapper, StringHandler
from .MxDControlSurfaceAPI import MxDControlSurfaceAPI
from .LomUtils import LomInformation, LomIntrospection, LomPathCalculator, LomPathResolver
from .LomTypes import ENUM_TYPES, LIVE_APP, CONTROL_SURFACES, PROPERTY_TYPES, ROOT_KEYS, MFLPropertyFormats, get_control_surfaces, get_exposed_lom_types, get_exposed_property_info, get_root_prop, is_lom_object, is_cplusplus_lom_object, is_object_iterable, LomNoteOperationWarning, LomNoteOperationError, LomAttributeError, LomObjectError, verify_object_property, data_dict_to_json
from .NotesAPIUtils import midi_note_to_dict, verify_note_specification_requirements
logger = logging.getLogger(__name__)

def get_current_max_device(device_id):
    assert MxDCore.instance != None and MxDCore.instance.manager != None
    return MxDCore.instance.manager.get_max_device(device_id)


PATH_KEY = u'CURRENT_PATH'
ID_KEY = u'CURRENT_LOM_ID'
TYPE_KEY = u'CURRENT_TYPE'
PROP_KEY = u'CURRENT_PROPERTY'
PROP_LISTENER_KEY = u'PROPERTY_LISTENER'
PATH_LISTENER_KEY = u'PATH_LISTENERS'
OPEN_OPERATIONS_KEY = u'OPEN_OPERATION'
NOTE_BUFFER_KEY = u'NOTE_BUFFER'
NOTE_OPERATION_KEY = u'NOTE_OPERATION'
NOTE_COUNT_KEY = u'NOTE_COUNT'
NOTE_REPLACE_KEY = u'NOTE_REPLACE'
NOTE_SET_KEY = u'NOTE_SET'
CONTAINS_CS_ID_KEY = u'CONTAINS_CS_ID_KEY'
LAST_SENT_ID_KEY = u'LAST_SENT_ID'
INVALID_DICT_ENTRY_ERROR = u'Invalid entry in the dictionary'
MALFORMATTED_DICTIONARY_ERROR = u'Malformatted dictionary argument'
NOTES_API_MAIN_KEY_ERROR = u"Expecting 'notes' as the main dictionary's key"
NOTE_ID_MISSING_ERROR = u"Required key 'note_id' is missing"
PRIVATE_PROP_WARNING = u'Warning: Calling private property. This property might change or be removed in the future.'
INVALID_NOTE_ID_ERROR = u"Provided note ID doesn't exist in the clip"

def concatenate_strings(string_list, string_format = u'%s %s'):
    return str(reduce(lambda s1, s2: string_format % (s1, s2), string_list) if len(string_list) > 0 else u'')


def parameter_to_bool(parameter):
    bool_value = False
    if isinstance(parameter, (int, type(False))):
        bool_value = parameter
    elif str(parameter) in (u'True', u'False'):
        bool_value = str(parameter) == u'True'
    return bool_value


def note_from_parameters(parameters):
    new_note = [parameters[0], parameters[1], parameters[2]]
    new_note.append(int(parameters[3]) if len(parameters) > 3 and isinstance(parameters[3], (int, float)) else 100)
    new_note.append(len(parameters) > 4 and parameter_to_bool(parameters[4]))
    return tuple(new_note)


class MxDCore(object):
    u""" Central class for the Max-integration """
    instance = None

    def __init__(self, *a, **k):
        super(MxDCore, self).__init__(*a, **k)
        self.device_contexts = {}
        self.manager = None
        self.lom_classes = []
        self.epii_version = (-1, -1)
        self._cs_api = MxDControlSurfaceAPI(self)
        self._call_handler = {u'get_notes': self._object_get_notes_handler,
         u'set_notes': self._object_set_notes_handler,
         u'get_selected_notes': self._object_selected_notes_handler,
         u'replace_selected_notes': self._object_replace_selected_notes_handler,
         u'get_notes_by_id': self._object_get_notes_by_id_handler,
         u'get_notes_extended': self._object_notes_extended_handler,
         u'get_selected_notes_extended': self._object_notes_extended_handler,
         u'add_new_notes': self._object_add_new_notes_handler,
         u'apply_note_modifications': self._object_apply_note_modifications_handler,
         u'remove_notes_by_id': self._object_remove_notes_by_id_handler,
         u'notes': self._object_notes_handler,
         u'note': self._object_note_handler,
         u'done': self._object_done_handler,
         u'get_control_names': self._cs_api.object_get_control_names,
         u'get_control': self._cs_api.object_get_control,
         u'grab_control': self._cs_api.object_grab_control,
         u'release_control': self._cs_api.object_release_control,
         u'send_midi': self._cs_api.object_send_midi,
         u'send_receive_sysex': self._cs_api.object_send_receive_sysex,
         u'grab_midi': self._cs_api.object_grab_midi,
         u'release_midi': self._cs_api.object_release_midi}
        self.lom_classes = get_exposed_lom_types()
        self.lom_classes += LomIntrospection(_Framework).lom_classes
        self.appointed_lom_ids = {0: None}

    def disconnect(self):
        for dev_id in list(self.device_contexts.keys()):
            device_context = self.device_contexts[dev_id]
            if device_context[CONTAINS_CS_ID_KEY]:
                self.release_device_context(dev_id, -1, u'')

        TupleWrapper.forget_tuple_wrapper_instances()
        self.manager.set_manager_callbacks(None, None, None, None)
        self.manager = None
        del self.appointed_lom_ids
        del self.lom_classes

    def set_manager(self, manager):
        self.manager = manager
        manager.set_manager_callbacks(self.update_observer_listener, self.install_observer_listener, self.uninstall_observer_listener, self.update_remote_timeable)
        self.epii_version = manager.get_epii_version()

    def _get_lom_object_by_lom_id(self, referring_device_id, lom_id):
        if lom_id > 0:
            return self.manager.get_lom_object(referring_device_id, lom_id)
        return self.appointed_lom_ids[lom_id]

    def _lom_id_exists(self, referring_device_id, lom_id):
        if lom_id > 0:
            return self.manager.lom_id_exists(referring_device_id, lom_id)
        return lom_id in self.appointed_lom_ids

    def _get_lom_id_by_lom_object(self, lom_object):
        if is_cplusplus_lom_object(lom_object):
            return self.manager.get_lom_id(lom_object)
        for id, object in self.appointed_lom_ids.items():
            if object == lom_object:
                return id

        id = -len(self.appointed_lom_ids)
        self.appointed_lom_ids[id] = lom_object
        if isinstance(lom_object, Disconnectable):

            def unregister_lom_object(f):

                @wraps(f)
                def wrapper(*a, **k):
                    try:
                        del self.appointed_lom_ids[id]
                    except KeyError:
                        pass

                    return f(*a, **k)

                return wrapper

            lom_object.disconnect = unregister_lom_object(lom_object.disconnect)
        return id

    def _get_lom_id_observers_and_remotes(self, lom_id):
        u"""returns a list of (device_id, object_id) tuples that observe the given lom_id"""
        assert lom_id != 0
        observers = []
        remotes = []
        for device_id, device_context in self.device_contexts.items():
            for object_id, _ in device_context.items():
                if not isinstance(object_id, int):
                    continue
                type = self._get_current_type(device_id, object_id)
                if type == u'obs':
                    if self._get_current_lom_id(device_id, object_id) == int(lom_id):
                        observers.append((device_id, object_id))
                elif type == u'rmt':
                    if self._get_current_lom_id(device_id, object_id) == int(lom_id):
                        remotes.append((device_id, object_id))

        return (observers, remotes)

    def _get_object_path(self, device_id, lom_object):
        resolver = LomPathCalculator(lom_object, get_current_max_device(device_id))
        return concatenate_strings(resolver.path_components)

    def _is_integer(self, s):
        if s[0] in (u'-', u'+'):
            return s[1:].isdigit()
        return s.isdigit()

    def _set_current_lom_id(self, device_id, object_id, lom_id, type):
        u"""set the CURRENT_LOM_ID of obj/obs/rmt objects"""
        if self.manager.set_current_lom_id(device_id, object_id, lom_id):
            self.device_contexts[device_id][object_id][ID_KEY] = 0
        else:
            self.device_contexts[device_id][object_id][ID_KEY] = lom_id
            self._set_current_type(device_id, object_id, type)
            if type == u'obs':
                self._observer_update_listener(device_id, object_id)
            elif type == u'rmt':
                self._remote_update_timeable(device_id, object_id, True)

    def _get_current_lom_id(self, device_id, object_id):
        u"""get the CURRENT_LOM_ID of obj/obs/rmt objects"""
        current_id = self.manager.get_current_lom_id(device_id, object_id)
        if current_id != 0:
            return current_id
        return self.device_contexts[device_id][object_id][ID_KEY]

    def _set_current_type(self, device_id, object_id, type):
        u"""set the CURRENT_TYPE of obj/obs/rmt objects"""
        if type == u'obj':
            old_type = self.device_contexts[device_id][object_id][TYPE_KEY]
            if old_type is None:
                self.device_contexts[device_id][object_id][TYPE_KEY] = type
        else:
            self.device_contexts[device_id][object_id][TYPE_KEY] = type

    def _get_current_type(self, device_id, object_id):
        u"""get the CURRENT_TYPE of obj/obs/rmt objects"""
        current_type = self.manager.get_type(device_id, object_id)
        if current_type != -1:
            return {0: u'obs',
             1: None,
             2: u'obj',
             3: u'obs',
             4: u'rmt'}[current_type]
        return self.device_contexts[device_id][object_id][TYPE_KEY]

    def _set_current_property(self, device_id, object_id, property_name):
        u"""set the name of the observed property"""
        if not self.manager.set_current_property(device_id, object_id, property_name):
            self.device_contexts[device_id][object_id][PROP_KEY] = property_name
            self._set_current_type(device_id, object_id, u'obs')
            self._observer_update_listener(device_id, object_id)

    def _get_current_property(self, device_id, object_id):
        u"""get the name of the observed property, or an empty string"""
        property_name = self.manager.get_current_property(device_id, object_id)
        if property_name != u'':
            return property_name
        return self.device_contexts[device_id][object_id][PROP_KEY]

    def update_device_context(self, device_id, object_id):
        if device_id not in list(self.device_contexts.keys()):
            self.device_contexts[device_id] = {CONTAINS_CS_ID_KEY: False}
        if object_id not in list(self.device_contexts[device_id].keys()):
            self.device_contexts[device_id][object_id] = {PATH_KEY: [],
             ID_KEY: 0,
             TYPE_KEY: None,
             PROP_KEY: u'',
             PROP_LISTENER_KEY: (None, None, None),
             PATH_LISTENER_KEY: {},
             OPEN_OPERATIONS_KEY: {},
             LAST_SENT_ID_KEY: None}

    def release_device_context(self, device_id, object_id, parameters):
        device_context = self.device_contexts[device_id]
        for key in list(device_context.keys()):
            if isinstance(key, int):
                object_context = device_context[key]
                self._observer_uninstall_listener(device_id, key)
                self._cs_api.release_control_surface_midi(device_id, key)
                if len(object_context[PATH_KEY]) > 0:
                    object_context[PATH_KEY] = []
                    self._install_path_listeners(device_id, key, self._path_listener_callback)

        del self.device_contexts[device_id]

    def prepare_control_surface_update(self, device_id, object_id, parameters):
        found_cs_references = False
        for dev_id in list(self.device_contexts.keys()):
            device_context = self.device_contexts[dev_id]
            if device_context[CONTAINS_CS_ID_KEY]:
                found_cs_references = True
                self.release_device_context(dev_id, -1, parameters)
                self.manager.refresh_max_device(dev_id)

        if found_cs_references:
            TupleWrapper.forget_tuple_wrapper_instances()
            self.appointed_lom_ids = {0: None}

    def path_set_path(self, device_id, object_id, parameters):
        assert isinstance(parameters, string_types)
        pure_path = parameters.strip().strip(u'"')
        path_components = pure_path.split(u' ')
        if len(pure_path) > 0 and path_components[0] not in ROOT_KEYS:
            self._raise(device_id, object_id, u'set path: invalid path')
        else:
            self.device_contexts[device_id][object_id][PATH_KEY] = []
            self.path_goto(device_id, object_id, parameters)

    def path_goto(self, device_id, object_id, parameters):
        assert isinstance(parameters, string_types)
        self._goto_path(device_id, object_id, parameters)
        device_context = self.device_contexts[device_id]
        object_context = device_context[object_id]
        result_object = self._object_from_path(device_id, object_id, object_context[PATH_KEY], must_exist=False)
        result_id = str(self._get_lom_id_by_lom_object(result_object))
        device_context[CONTAINS_CS_ID_KEY] |= CONTROL_SURFACES in object_context[PATH_KEY]
        result_path = str(concatenate_strings(object_context[PATH_KEY]))
        for msg_type, value in ((u'path_curr_path', result_path), (u'path_orig_id', result_id), (u'path_curr_id', result_id)):
            self.manager.send_message(device_id, object_id, msg_type, value)

        self._install_path_listeners(device_id, object_id, self._path_listener_callback)

    def path_get_id(self, device_id, object_id, parameters):
        device_context = self.device_contexts[device_id]
        object_context = device_context[object_id]
        lom_object = self._object_from_path(device_id, object_id, object_context[PATH_KEY], must_exist=False)
        result_id = str(self._get_lom_id_by_lom_object(lom_object))
        for msg_type, value in ((u'path_orig_id', result_id), (u'path_curr_id', result_id)):
            self.manager.send_message(device_id, object_id, msg_type, value)

    def path_bang(self, device_id, object_id, parameters):
        self.path_get_id(device_id, object_id, parameters)

    def _get_path_and_object(self, device_id, object_id):
        device_context = self.device_contexts[device_id]
        object_context = device_context[object_id]
        current_path = object_context[PATH_KEY]
        current_object = self._object_from_path(device_id, object_id, current_path, must_exist=True)
        return (current_path, current_object)

    def _get_lom_object_properties(self, device_id, object_id, looking_for):
        current_path, current_object = self._get_path_and_object(device_id, object_id)
        if len(current_path) == 0:
            result = concatenate_strings(ROOT_KEYS)
        elif current_object != None:
            current_object = self._disambiguate_object(current_object)
            if is_object_iterable(current_object):
                result = u'%d list elements, no %s' % (len(current_object), looking_for)
            else:
                lom_info = LomInformation(current_object, self.epii_version)
                path_props = [ info[0] for info in lom_info.lists_of_children + lom_info.children ]
                result = concatenate_strings(sorted(path_props))
        return result

    def path_get_props(self, device_id, object_id, parameters):
        result = self._get_lom_object_properties(device_id, object_id, u'properties') or u'No path properties'
        self.manager.send_message(device_id, object_id, u'path_props', result)

    def path_get_children(self, device_id, object_id, parameters):
        result = self._get_lom_object_properties(device_id, object_id, u'children') or u'No children'
        self.manager.send_message(device_id, object_id, u'path_children', result)

    def path_get_count(self, device_id, object_id, parameters):
        assert isinstance(parameters, string_types)
        device_context = self.device_contexts[device_id]
        object_context = device_context[object_id]
        current_path = object_context[PATH_KEY]
        current_object = self._object_from_path(device_id, object_id, current_path, must_exist=True)
        property = None
        if len(current_path) == 0:
            if parameters in ROOT_KEYS:
                property = get_root_prop(get_current_max_device(device_id), parameters)
        elif current_object != None:
            if old_hasattr(current_object, parameters):
                property = getattr(current_object, parameters)
        if property != None:
            count = str(len(property) if is_object_iterable(property) else -1)
            self.manager.send_message(device_id, object_id, u'path_count', concatenate_strings((parameters, count)))
        else:
            self._raise(device_id, object_id, u'getcount: invalid property name')

    def obj_set_id(self, device_id, object_id, parameter):
        if self._is_integer(parameter) and self._lom_id_exists(device_id, int(parameter)):
            self._set_current_lom_id(device_id, object_id, int(parameter), u'obj')
        else:
            self._raise(device_id, object_id, u'set id: invalid id')

    def obj_get_id(self, device_id, object_id, parameter):
        self.manager.send_message(device_id, object_id, u'obj_id', str(self._get_current_lom_id(device_id, object_id)))

    def obj_get_path(self, device_id, object_id, parameters):
        lom_object = self._get_current_lom_object(device_id, object_id)
        path = self._get_object_path(device_id, lom_object)
        if len(path) == 0 and lom_object != None:
            self._raise(device_id, object_id, u'get path: error calculating the path')
        else:
            self.manager.send_message(device_id, object_id, u'obj_path', str(path).strip())

    def obj_get_type(self, device_id, object_id, parameters):
        current_object = self._get_current_lom_object(device_id, object_id)
        object_type = u'unknown'
        if current_object != None:
            current_object = self._disambiguate_object(current_object)
            object_type = current_object.__class__.__name__
        self.manager.send_message(device_id, object_id, u'obj_type', str(object_type))

    def obj_get_info(self, device_id, object_id, parameters):
        current_object = self._get_current_lom_object(device_id, object_id)
        object_info = u'No object'
        if current_object != None:
            object_info = u'id %s\n' % str(self._get_lom_id_by_lom_object(current_object))
            current_object = self._disambiguate_object(current_object)
            lom_info = LomInformation(current_object, self.epii_version)
            object_info += u'type %s\n' % str(current_object.__class__.__name__)
            object_info += u'%s\n' % lom_info.description
            if not is_object_iterable(current_object):

                def accumulate_info(info_list, label):
                    result = u''
                    if len(info_list) > 0:
                        str_format = u'%s %s %s\n' if len(info_list[0]) > 1 else u'%s %s\n'
                        formatter = lambda info: str_format % ((label,) + info)
                        result = concatenate_strings(list(map(formatter, info_list)), string_format=u'%s%s')
                    return result

                object_info += accumulate_info(lom_info.lists_of_children, u'children') + accumulate_info(lom_info.children, u'child') + accumulate_info(lom_info.properties, u'property') + accumulate_info(lom_info.functions, u'function')
            object_info += u'done'
        self.manager.send_message(device_id, object_id, u'obj_info', str(object_info))

    def obj_set_val(self, device_id, object_id, parameters):
        self.obj_set(device_id, object_id, parameters)

    def _set_property_value(self, lom_object, property_name, value):
        verify_object_property(lom_object, property_name, self.epii_version)
        prop = getattr(lom_object, property_name)
        prop_info = get_exposed_property_info(type(lom_object), property_name, self.epii_version)
        if prop_info and prop_info.from_json:
            value = prop_info.from_json(lom_object, value)
            if value is None:
                raise LomAttributeError(u'set: invalid value')
        elif property_name in list(PROPERTY_TYPES.keys()):
            if not is_lom_object(value, self.lom_classes):
                raise LomAttributeError(u'set: no valid object id')
            if not isinstance(value, PROPERTY_TYPES[property_name]):
                raise LomAttributeError(u'set: type mismatch')
        elif isinstance(prop, (int, bool)):
            if str(value) in (u'True', u'False'):
                value = int(str(value) == u'True')
            elif not isinstance(value, int):
                raise LomAttributeError(u'set: invalid value')
        elif isinstance(prop, float):
            if not isinstance(value, (int, float)):
                raise LomAttributeError(u'set: type mismatch')
            value = float(value)
        elif isinstance(prop, string_types):
            if not isinstance(value, (string_types, int, float)):
                raise LomAttributeError(u'set: type mismatch')
            value = str(value)
        elif isinstance(prop, tuple):
            prop_info = get_exposed_property_info(type(lom_object), property_name, self.epii_version)
            if prop_info and prop_info.format == MFLPropertyFormats.JSON:
                package = json.loads(value)
                value = tuple(package[property_name])
            else:
                raise LomAttributeError(u'set: unsupported property type')
        else:
            raise LomAttributeError(u'set: unsupported property type')
        setattr(lom_object, property_name, value)

    def _warn_if_using_private_property(self, device_id, object_id, property_name):
        did_warn = False
        warn = partial(self._warn, device_id, object_id)
        if property_name.startswith(u'_'):
            warn(PRIVATE_PROP_WARNING)
            did_warn = True
        return did_warn

    def obj_set(self, device_id, object_id, parameters):
        assert isinstance(parameters, string_types)
        current_object = self._get_current_lom_object(device_id, object_id)
        if current_object != None:
            parsed_params = self._parse(device_id, object_id, parameters)
            property_name = parsed_params[0]
            property_values = parsed_params[1:]
            value = property_values[0]
            try:
                self._set_property_value(current_object, property_name, value)
                self._warn_if_using_private_property(device_id, object_id, property_name)
            except LomAttributeError as e:
                self._raise(device_id, object_id, str(e))

    def obj_get_val(self, device_id, object_id, parameters):
        self.obj_get(device_id, object_id, parameters)

    def obj_get(self, device_id, object_id, parameters):
        assert isinstance(parameters, string_types)
        current_object = self._get_current_lom_object(device_id, object_id)
        result_value = None
        if current_object != None:
            try:
                if parameters.isdigit():
                    assert is_object_iterable(current_object)
                    assert int(parameters) in range(len(current_object))
                    result_value = current_object[int(parameters)]
                else:
                    if not self._warn_if_using_private_property(device_id, object_id, parameters):
                        verify_object_property(current_object, parameters, self.epii_version)
                    result_value = getattr(current_object, parameters)
                    if isinstance(result_value, ENUM_TYPES):
                        result_value = int(result_value)
                prop_info = get_exposed_property_info(type(current_object), parameters, self.epii_version)
                if prop_info and prop_info.to_json:
                    result = self.str_representation_for_object(prop_info.to_json(current_object))
                else:
                    result = self.str_representation_for_object(result_value)
                self.manager.send_message(device_id, object_id, u'obj_prop_val', result)
            except LomAttributeError as e:
                self._warn(device_id, object_id, str(e))

        else:
            self._warn(device_id, object_id, u'get: no valid object set')

    def obj_call(self, device_id, object_id, parameters):
        assert isinstance(parameters, string_types)
        current_object = self._get_current_lom_object(device_id, object_id)
        if current_object != None:
            try:
                param_comps = self._parse(device_id, object_id, parameters)
                func_name = str(param_comps[0])
                handler = self._call_handler[func_name] if func_name in list(self._call_handler.keys()) else self._object_default_call_handler
                handler(device_id, object_id, current_object, param_comps)
            except AttributeError as e:
                self._raise(device_id, object_id, str(e))
            except RuntimeError as e:
                self._raise(device_id, object_id, u"%s: '%s'" % (str(e), parameters))
            except Exception as e:
                reason = u'Invalid ' + (u'arguments' if isinstance(e, TypeError) else u'syntax')
                self._raise(device_id, object_id, u"%s: '%s'" % (reason, parameters))

        else:
            self._warn(device_id, object_id, u'call %s: no valid object set' % parameters)

    def obs_set_id(self, device_id, object_id, parameter):
        if self._is_integer(parameter) and self._lom_id_exists(device_id, int(parameter)):
            self.device_contexts[device_id][object_id][LAST_SENT_ID_KEY] = None
            self._set_current_lom_id(device_id, object_id, int(parameter), u'obs')
        else:
            self._raise(device_id, object_id, u'set id: invalid id')

    def obs_get_id(self, device_id, object_id, parameter):
        self.manager.send_message(device_id, object_id, u'obs_id', str(self._get_current_lom_id(device_id, object_id)))

    def obs_set_prop(self, device_id, object_id, parameter):
        assert isinstance(parameter, string_types)
        self._set_current_property(device_id, object_id, parameter)

    def obs_get_prop(self, device_id, object_id, parameter):
        self.manager.send_message(device_id, object_id, u'obs_prop', str(self._get_current_property(device_id, object_id)))

    def obs_get_type(self, device_id, object_id, parameter):
        current_object = self._get_current_lom_object(device_id, object_id)
        property_name = self._get_current_property(device_id, object_id)
        result = u'unknown'
        if current_object != None and property_name != u'':
            if old_hasattr(current_object, property_name):
                result = getattr(current_object, property_name).__class__.__name__
            else:
                self._warn(device_id, object_id, u'gettype: no property with the name ' + property_name)
        self.manager.send_message(device_id, object_id, u'obs_type', str(result))

    def obs_bang(self, device_id, object_id, parameter):
        self._observer_property_callback(device_id, object_id)

    def rmt_set_id(self, device_id, object_id, parameter):
        if self._is_integer(parameter) and self._lom_id_exists(device_id, int(parameter)):
            new_id = int(parameter)
            lom_object = self._get_lom_object_by_lom_id(device_id, new_id)
            if isinstance(lom_object, (Live.DeviceParameter.DeviceParameter, type(None))):
                self._set_current_lom_id(device_id, object_id, new_id, u'rmt')
            else:
                self._raise(device_id, object_id, u'set id: only accepts objects of type DeviceParameter')
        else:
            self._raise(device_id, object_id, u'set id: invalid id')

    def _object_attr_path_iter(self, device_id, object_id, path_components):
        u"""Returns a generator of (object, attribute) tuples along the given path.
        It won't pack objects into a TupleWrapper."""
        if len(path_components) == 0:
            return
        assert path_components[0] in ROOT_KEYS
        cur_object = get_root_prop(get_current_max_device(device_id), path_components[0])
        for component in path_components[1:]:
            if cur_object == None:
                return
            yield (cur_object, component)
            if component.isdigit():
                assert is_object_iterable(cur_object)
                index = int(component)
                if index >= 0 and index < len(cur_object):
                    cur_object = cur_object[index]
                else:
                    return
            else:
                try:
                    cur_object = getattr(cur_object, component)
                except Exception:
                    return

    def _object_from_path(self, device_id, object_id, path_components, must_exist):
        lom_object = None
        try:
            resolver = LomPathResolver(path_components, get_current_max_device(device_id), self.lom_classes, self.manager)
            lom_object = resolver.lom_object
        except (LomAttributeError, LomObjectError) as e:
            if must_exist or isinstance(e, LomObjectError):
                self._raise(device_id, object_id, str(e))

        return lom_object

    def _get_current_lom_object(self, device_id, object_id):
        u"""retrieving current lom object for object_ids of type obj/obs/rmt"""
        return self._get_lom_object_by_lom_id(device_id, self._get_current_lom_id(device_id, object_id))

    def _object_for_id(self, device_id):
        lom_object = None
        try:
            lom_object = partial(self._get_lom_object_by_lom_id, device_id)
        except:
            pass

        return lom_object

    def str_representation_for_object(self, lom_object, mark_ids = True):
        result = u''
        lom_object = self._disambiguate_object(lom_object)
        if is_object_iterable(lom_object):
            result = concatenate_strings(list(map(self.str_representation_for_object, lom_object)))
        elif is_lom_object(lom_object, self.lom_classes):
            result = (u'id ' if mark_ids else u'') + str(self._get_lom_id_by_lom_object(lom_object))
        elif isinstance(lom_object, (int, bool)):
            result = str(int(lom_object))
        else:
            result = StringHandler.prepare_outgoing(str(lom_object))
        return result

    def _install_path_listeners(self, device_id, object_id, listener_callback):
        device_context = self.device_contexts[device_id]
        object_context = device_context[object_id]
        path_components = object_context[PATH_KEY]
        new_listeners = {}
        self._uninstall_path_listeners(device_id, object_id)
        listener = partial(listener_callback, device_id, object_id)
        obj_attr_iter = self._object_attr_path_iter(device_id, object_id, path_components)
        for lom_object, attribute in obj_attr_iter:
            attribute = self._listenable_property_for(attribute)
            if lom_object != None and old_hasattr(lom_object, attribute + u'_has_listener'):
                assert not getattr(lom_object, attribute + u'_has_listener')(listener)
                getattr(lom_object, u'add_%s_listener' % attribute)(listener)
                new_listeners[lom_object, attribute] = listener

        object_context[PATH_LISTENER_KEY] = new_listeners

    def _uninstall_path_listeners(self, device_id, object_id):
        device_context = self.device_contexts[device_id]
        object_context = device_context[object_id]
        old_listeners = object_context[PATH_LISTENER_KEY]
        for (lom_object, attribute), listener in old_listeners.items():
            if lom_object != None and getattr(lom_object, attribute + u'_has_listener')(listener):
                getattr(lom_object, u'remove_%s_listener' % attribute)(listener)

    def _path_listener_callback(self, device_id, object_id):
        device_context = self.device_contexts[device_id]
        object_context = device_context[object_id]
        resulting_id = self._get_lom_id_by_lom_object(self._object_from_path(device_id, object_id, object_context[PATH_KEY], must_exist=False))
        self.manager.send_message(device_id, object_id, u'path_curr_id', str(resulting_id))
        self._install_path_listeners(device_id, object_id, self._path_listener_callback)

    def _goto_path(self, device_id, object_id, parameters):
        device_context = self.device_contexts[device_id]
        object_context = device_context[object_id]
        try:
            pure_path = parameters.strip().strip(u'"')
            path_components = []
            if len(pure_path) > 0:
                path_components = pure_path.strip().split(u' ')
            if tuple(path_components[:2]) == (LIVE_APP, CONTROL_SURFACES):
                object_context[PATH_KEY] = [LIVE_APP, CONTROL_SURFACES]
                path_components = path_components[2:]
            for parameter in path_components:
                if parameter == u'up':
                    del object_context[PATH_KEY][-1]
                else:
                    if parameter in ROOT_KEYS:
                        object_context[PATH_KEY] = []
                    object_context[PATH_KEY].append(parameter)

        except:
            self._raise(device_id, object_id, u'goto: invalid path')
            return

    def _object_default_call_handler(self, device_id, object_id, lom_object, parameters):
        verify_object_property(lom_object, parameters[0], self.epii_version)
        self._warn_if_using_private_property(device_id, object_id, parameters[0])
        function = getattr(lom_object, parameters[0])
        result = function(*parameters[1:])
        result_str = self.str_representation_for_object(result)
        self.manager.send_message(device_id, object_id, u'obj_call_result', result_str)

    def _object_get_notes_handler(self, device_id, object_id, lom_object, parameters):
        assert isinstance(lom_object, Live.Clip.Clip) and lom_object.is_midi_clip
        assert parameters[0] == u'get_notes'
        notes = getattr(lom_object, u'get_notes')(parameters[1], parameters[2], parameters[3], parameters[4])
        self.manager.send_message(device_id, object_id, u'obj_call_result', self._create_notes_output(notes))

    def _object_notes_extended_handler(self, device_id, object_id, lom_object, parameters):
        function_name, function_parameters = parameters[0], parameters[1:]
        verify_object_property(lom_object, function_name, self.epii_version)
        midi_note_vector = getattr(lom_object, function_name)(*function_parameters)
        self.manager.send_message(device_id, object_id, u'obj_call_result', self.str_representation_for_object(self._midi_note_vector_to_dict_output(midi_note_vector)))

    def _object_get_notes_by_id_handler(self, device_id, object_id, lom_object, parameters):
        function_name, function_parameters = parameters[0], parameters[1:]
        verify_object_property(lom_object, function_name, self.epii_version)
        try:
            midi_note_vector = getattr(lom_object, function_name)(function_parameters)
        except ValueError:
            raise RuntimeError(INVALID_NOTE_ID_ERROR)

        self.manager.send_message(device_id, object_id, u'obj_call_result', self.str_representation_for_object(self._midi_note_vector_to_dict_output(midi_note_vector)))

    def _object_add_new_notes_handler(self, device_id, object_id, lom_object, parameters):
        function_name, function_parameter = parameters[0], parameters[1]
        verify_object_property(lom_object, function_name, self.epii_version)
        note_dicts = self._get_list_of_note_dictionaries(function_parameter)
        note_specifications = []
        for note_dict in note_dicts:
            verify_note_specification_requirements(note_dict)
            try:
                note_specifications.append(Live.Clip.MidiNoteSpecification(**note_dict))
            except TypeError:
                raise RuntimeError(INVALID_DICT_ENTRY_ERROR)

        result = getattr(lom_object, function_name)(note_specifications)
        self.manager.send_message(device_id, object_id, u'obj_call_result', self.str_representation_for_object(result))

    def _object_apply_note_modifications_handler(self, device_id, object_id, lom_object, parameters):
        function_name, function_parameter = parameters[0], parameters[1]
        verify_object_property(lom_object, function_name, self.epii_version)
        note_dicts = self._get_list_of_note_dictionaries(function_parameter)
        try:
            id_to_note_mapping = {note[u'note_id']:note for note in note_dicts}
        except KeyError:
            raise RuntimeError(NOTE_ID_MISSING_ERROR)

        midi_notes = lom_object.get_notes_by_id(id_to_note_mapping.keys())
        for midi_note in midi_notes:
            note_dict = id_to_note_mapping[midi_note.note_id]
            for property_name, value in note_dict.items():
                if property_name != u'note_id':
                    setattr(midi_note, property_name, value)

        result = getattr(lom_object, function_name)(midi_notes)
        self.manager.send_message(device_id, object_id, u'obj_call_result', self.str_representation_for_object(result))

    def _object_remove_notes_by_id_handler(self, device_id, object_id, lom_object, parameters):
        function_name, function_parameters = parameters[0], parameters[1:]
        verify_object_property(lom_object, function_name, self.epii_version)
        try:
            result = getattr(lom_object, function_name)(function_parameters)
        except ValueError:
            raise RuntimeError(INVALID_NOTE_ID_ERROR)

        self.manager.send_message(device_id, object_id, u'obj_call_result', self.str_representation_for_object(result))

    def _object_selected_notes_handler(self, device_id, object_id, lom_object, parameters):
        assert isinstance(lom_object, Live.Clip.Clip) and lom_object.is_midi_clip
        notes = getattr(lom_object, u'get_selected_notes')()
        self.manager.send_message(device_id, object_id, u'obj_call_result', self._create_notes_output(notes))

    def _object_set_notes_handler(self, device_id, object_id, lom_object, parameters):
        self._start_note_operation(device_id, object_id, lom_object, parameters, NOTE_SET_KEY)

    def _object_replace_selected_notes_handler(self, device_id, object_id, lom_object, parameters):
        self._start_note_operation(device_id, object_id, lom_object, parameters, NOTE_REPLACE_KEY)

    def _object_notes_handler(self, device_id, object_id, lom_object, parameters):
        assert isinstance(lom_object, Live.Clip.Clip) and lom_object.is_midi_clip
        assert isinstance(parameters[1], int)
        device_context = self.device_contexts[device_id][object_id]
        if NOTE_OPERATION_KEY in list(device_context[OPEN_OPERATIONS_KEY].keys()):
            device_context[OPEN_OPERATIONS_KEY][NOTE_COUNT_KEY] = parameters[1]
        else:
            self._raise(device_id, object_id, u'no operation in progress')

    def _object_note_handler(self, device_id, object_id, lom_object, parameters):
        assert isinstance(lom_object, Live.Clip.Clip) and lom_object.is_midi_clip
        assert isinstance(parameters[1], (int, float))
        assert isinstance(parameters[2], float)
        assert isinstance(parameters[3], float)
        device_context = self.device_contexts[device_id][object_id]
        operations = device_context[OPEN_OPERATIONS_KEY]
        try:
            if NOTE_OPERATION_KEY not in operations:
                raise LomNoteOperationError(u'no operation in progress')
            if NOTE_COUNT_KEY not in operations:
                raise LomNoteOperationError(u'no note count given')
            assert NOTE_BUFFER_KEY in operations
            if len(operations[NOTE_BUFFER_KEY]) >= operations[NOTE_COUNT_KEY]:
                raise LomNoteOperationError(u'too many notes')
            operations[NOTE_BUFFER_KEY].append(note_from_parameters(parameters[1:]))
        except LomNoteOperationError as e:
            self._raise(device_id, object_id, str(e))
            self._stop_note_operation(device_id, object_id)

    def _selector_for_note_operation(self, note_operation):
        if note_operation not in (NOTE_REPLACE_KEY, NOTE_SET_KEY):
            raise LomNoteOperationWarning(u'invalid note operation')
        if note_operation == NOTE_SET_KEY:
            return u'set_notes'
        return u'replace_selected_notes'

    def _object_done_handler(self, device_id, object_id, lom_object, parameters):
        assert isinstance(lom_object, Live.Clip.Clip) and lom_object.is_midi_clip
        device_context = self.device_contexts[device_id][object_id]
        open_operations = device_context[OPEN_OPERATIONS_KEY]
        if NOTE_OPERATION_KEY in open_operations and NOTE_COUNT_KEY in open_operations:
            assert NOTE_BUFFER_KEY in open_operations
            try:
                notes = tuple(open_operations[NOTE_BUFFER_KEY])
                if len(notes) != open_operations[NOTE_COUNT_KEY]:
                    raise LomNoteOperationWarning(u'wrong note count')
                operation = open_operations[NOTE_OPERATION_KEY]
                selector = self._selector_for_note_operation(operation)
                getattr(lom_object, selector)(notes)
            except LomNoteOperationWarning as w:
                self._warn(device_id, object_id, str(w))

            self._stop_note_operation(device_id, object_id)
        else:
            self._raise(device_id, object_id, u'no operation in progress')

    def _create_notes_output(self, notes):
        element_format = lambda el: str(int(el) if isinstance(el, bool) else el)
        note_format = lambda note: u'note %s\n' % concatenate_strings(list(map(element_format, note)))
        result = u'notes %d\n%sdone' % (len(notes), concatenate_strings(list(map(note_format, notes)), string_format=u'%s%s'))
        return result

    def _midi_note_vector_to_dict_output(self, notes):
        return data_dict_to_json(u'notes', [ midi_note_to_dict(note) for note in notes ])

    def _get_list_of_note_dictionaries(self, parameter):
        try:
            data_dict = json.loads(parameter)
        except Exception:
            raise RuntimeError(MALFORMATTED_DICTIONARY_ERROR)

        try:
            note_dicts = data_dict[u'notes']
        except KeyError:
            raise RuntimeError(NOTES_API_MAIN_KEY_ERROR)

        return note_dicts

    def _start_note_operation(self, device_id, object_id, lom_object, parameters, operation):
        assert isinstance(lom_object, Live.Clip.Clip) and lom_object.is_midi_clip
        device_context = self.device_contexts[device_id][object_id]
        if NOTE_OPERATION_KEY not in list(device_context[OPEN_OPERATIONS_KEY].keys()):
            assert NOTE_BUFFER_KEY not in list(device_context[OPEN_OPERATIONS_KEY].keys())
            assert NOTE_BUFFER_KEY not in list(device_context[OPEN_OPERATIONS_KEY].keys())
            device_context[OPEN_OPERATIONS_KEY][NOTE_BUFFER_KEY] = []
            device_context[OPEN_OPERATIONS_KEY][NOTE_OPERATION_KEY] = operation
        else:
            self._raise(device_id, object_id, u'an operation is already in progress')

    def _stop_note_operation(self, device_id, object_id):
        device_context = self.device_contexts[device_id][object_id]
        for key in (NOTE_OPERATION_KEY, NOTE_BUFFER_KEY, NOTE_COUNT_KEY):
            try:
                del device_context[OPEN_OPERATIONS_KEY][key]
            except KeyError:
                pass

    def update_observer_listener(self, device_id, object_id):
        self.update_device_context(device_id, object_id)
        self._observer_update_listener(device_id, object_id)

    def install_observer_listener(self, device_id, object_id):
        self.update_device_context(device_id, object_id)
        self._observer_install_listener(device_id, object_id)

    def uninstall_observer_listener(self, device_id, object_id):
        self.update_device_context(device_id, object_id)
        self._observer_uninstall_listener(device_id, object_id)

    def update_lom_id_observers_and_remotes(self, lom_id):
        u"""updates observer and remote~ links for the given lom_id"""
        observers, remotes = self._get_lom_id_observers_and_remotes(lom_id)
        for device_id, object_id in observers:
            self._observer_update_listener(device_id, object_id)

        for device_id, object_id in remotes:
            self._remote_update_timeable(device_id, object_id, False)

    def _observer_update_listener(self, device_id, object_id):
        self._observer_uninstall_listener(device_id, object_id)
        self._observer_install_listener(device_id, object_id)

    def _observer_install_listener(self, device_id, object_id):
        assert self.device_contexts[device_id][object_id][PROP_LISTENER_KEY] == (None, None, None)
        current_object = self._get_current_lom_object(device_id, object_id)
        property_name = self._get_current_property(device_id, object_id)
        self._warn_if_using_private_property(device_id, object_id, property_name)
        if property_name == u'id':
            self._observer_id_callback(device_id, object_id)
        elif current_object != None and property_name != u'':
            object_context = self.device_contexts[device_id][object_id]
            listener_callback = partial(self._observer_property_callback, device_id, object_id)
            transl_prop_name = self._listenable_property_for(property_name)
            if old_hasattr(current_object, transl_prop_name + u'_has_listener'):
                assert not getattr(current_object, transl_prop_name + u'_has_listener')(listener_callback)
                getattr(current_object, u'add_%s_listener' % transl_prop_name)(listener_callback)
                object_context[PROP_LISTENER_KEY] = (listener_callback, current_object, property_name)
                listener_callback()
            elif old_hasattr(current_object, transl_prop_name):
                self._warn(device_id, object_id, u'property cannot be listened to')

    def _observer_uninstall_listener(self, device_id, object_id):
        device_context = self.device_contexts[device_id]
        object_context = device_context[object_id]
        self._uninstall_path_listeners(device_id, object_id)
        listener_callback, current_object, property_name = object_context[PROP_LISTENER_KEY]
        if current_object != None and listener_callback != None:
            assert property_name != u''
            assert not isinstance(current_object, TupleWrapper)
            transl_prop_name = self._listenable_property_for(property_name)
            assert old_hasattr(current_object, transl_prop_name + u'_has_listener')
            if getattr(current_object, transl_prop_name + u'_has_listener')(listener_callback):
                getattr(current_object, u'remove_%s_listener' % transl_prop_name)(listener_callback)
        object_context[PROP_LISTENER_KEY] = (None, None, None)

    def _observer_property_message_type(self, prop, prop_info):
        prop_type = None
        if prop_info and prop_info.format == MFLPropertyFormats.JSON:
            prop_type = u'obs_dict_val'
        elif isinstance(prop, string_types):
            prop_type = u'obs_string_val'
        elif isinstance(prop, (int, bool)):
            prop_type = u'obs_int_val'
        elif isinstance(prop, float):
            prop_type = u'obs_float_val'
        elif is_object_iterable(prop):
            prop_type = u'obs_list_val'
        elif is_lom_object(prop, self.lom_classes):
            prop_type = u'obs_id_val'
        return prop_type

    def _observer_property_callback(self, device_id, object_id, *args):
        current_object = self._get_current_lom_object(device_id, object_id)
        property_name = self._get_current_property(device_id, object_id)
        prop_info = get_exposed_property_info(type(current_object), property_name, self.epii_version)
        if len(args) > 0:
            formatter = lambda arg: str(int(arg) if isinstance(arg, bool) else arg)
            args_type = self._observer_property_message_type(args if len(args) > 1 else args[0], prop_info)
            result = concatenate_strings(list(map(formatter, args)))
            self.manager.send_message(device_id, object_id, args_type, result)
        elif current_object != None and property_name != u'':
            assert not isinstance(current_object, TupleWrapper)
            if old_hasattr(current_object, property_name):
                prop = getattr(current_object, property_name)
                prop_type = self._observer_property_message_type(prop, prop_info)
                if prop_type == None:
                    self._warn(device_id, object_id, u'unsupported property type')
                else:
                    prop_value = self.str_representation_for_object(prop_info.to_json(current_object) if prop_info and prop_info.to_json else prop, mark_ids=False)
                    self.manager.send_message(device_id, object_id, prop_type, prop_value)
            elif old_hasattr(current_object, property_name + u'_has_listener'):
                self.manager.send_message(device_id, object_id, u'obs_string_val', u'bang')
            else:
                self._warn(device_id, object_id, u'property should be listenable')

    def _observer_id_callback(self, device_id, object_id):
        assert self._get_current_property(device_id, object_id) == u'id'
        object_context = self.device_contexts[device_id][object_id]
        current_object = self._get_current_lom_object(device_id, object_id)
        self._goto_path(device_id, object_id, self._get_object_path(device_id, current_object))
        self._install_path_listeners(device_id, object_id, self._observer_id_callback)
        current_id = 0 if current_object == None else self._get_current_lom_id(device_id, object_id)
        if current_id != object_context[LAST_SENT_ID_KEY]:
            object_context[LAST_SENT_ID_KEY] = current_id
            self.manager.send_message(device_id, object_id, u'obs_id_val', str(current_id))

    def update_remote_timeable(self, device_id, object_id):
        self.update_device_context(device_id, object_id)
        self._remote_update_timeable(device_id, object_id, False)

    def reset_all_current_lom_ids(self, device_id):
        if device_id in self.device_contexts:
            device_context = self.device_contexts[device_id]
            for object_id, _ in device_context.items():
                if isinstance(object_id, int):
                    type = self._get_current_type(device_id, object_id)
                    if type in (u'obs', u'obj', u'rmt'):
                        self._set_current_lom_id(device_id, object_id, 0, type)

    def _remote_update_timeable(self, device_id, object_id, validate_change_allowed):
        current_object = self._get_current_lom_object(device_id, object_id)
        if isinstance(current_object, Live.DeviceParameter.DeviceParameter):
            self.manager.register_remote_timeable(device_id, object_id, current_object, validate_change_allowed)
        else:
            self.manager.unregister_remote_timeable(device_id, object_id, validate_change_allowed)

    def _disambiguate_object(self, object):
        result = object
        if object.__class__.__name__ in (u'ListWrapper', u'TupleWrapper'):
            result = object.get_list()
        return result

    def _listenable_property_for(self, prop_name):
        if prop_name == u'clip':
            return u'has_clip'
        return prop_name

    def _parse(self, device_id, object_id, string):
        return StringHandler.parse(string, self._object_for_id(device_id))

    def _raise(self, device_id, object_id, message):
        logger.error(u'Error: ' + str(message))
        self.manager.print_message(device_id, object_id, u'error', str(message))

    def _warn(self, device_id, object_id, message):
        logger.warning(u'Warning: ' + str(message))
        self.manager.print_message(device_id, object_id, u'warning', str(message))
