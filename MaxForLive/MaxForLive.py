# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\MaxForLive\MaxForLive.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 2310 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface import SimpleControlSurface
from ableton.v2.control_surface.input_control_element import MIDI_CC_TYPE, MIDI_NOTE_TYPE, MIDI_PB_TYPE, InputControlElement
STATUS_TO_TYPE = {144:MIDI_NOTE_TYPE, 
 176:MIDI_CC_TYPE,  224:MIDI_PB_TYPE}

class MaxForLive(SimpleControlSurface):

    def __init__(self, *a, **k):
        (super(MaxForLive, self).__init__)(*a, **k)
        self._registered_control_names = []
        self._registered_messages = []

    def register_midi_control--- This code section failed: ---

 L.  24         0  LOAD_FAST                'status'
                2  LOAD_FAST                'number'
                4  BUILD_TUPLE_2         2 
                6  STORE_FAST               'message'

 L.  27         8  LOAD_GLOBAL              isinstance
               10  LOAD_FAST                'status'
               12  LOAD_GLOBAL              int
               14  CALL_FUNCTION_2       2  '2 positional arguments'
               16  POP_JUMP_IF_FALSE    62  'to 62'

 L.  28        18  LOAD_FAST                'status'
               20  LOAD_CONST               240
               22  BINARY_AND       
               24  LOAD_CONST               (144, 176, 224)
               26  COMPARE_OP               in
               28  POP_JUMP_IF_FALSE    62  'to 62'

 L.  29        30  LOAD_GLOBAL              isinstance
               32  LOAD_FAST                'number'
               34  LOAD_GLOBAL              int
               36  CALL_FUNCTION_2       2  '2 positional arguments'
               38  POP_JUMP_IF_FALSE    62  'to 62'

 L.  30        40  LOAD_CONST               0
               42  LOAD_FAST                'number'
               44  DUP_TOP          
               46  ROT_THREE        
               48  COMPARE_OP               <=
               50  POP_JUMP_IF_FALSE    60  'to 60'
               52  LOAD_CONST               127
               54  COMPARE_OP               <=
               56  POP_JUMP_IF_TRUE     70  'to 70'
               58  JUMP_FORWARD         62  'to 62'
             60_0  COME_FROM            50  '50'
               60  POP_TOP          
             62_0  COME_FROM            58  '58'
             62_1  COME_FROM            38  '38'
             62_2  COME_FROM            28  '28'
             62_3  COME_FROM            16  '16'

 L.  32        62  LOAD_GLOBAL              RuntimeError

 L.  33        64  LOAD_STR                 'register_midi_control requires parameters: name, status byte, note/CC number\n    name:\n        as used for grab/release\n    status byte:\n        0x9n for note-on/off\n        0xBn for control change\n        0xEn for pitch bend\n        where n is the channel in range 0x0..0xF\n    note/CC number:\n        0...127 (ignored for pitch bend)\n'
               66  CALL_FUNCTION_1       1  '1 positional argument'
               68  RAISE_VARARGS_1       1  'exception instance'
             70_0  COME_FROM            56  '56'

 L.  45        70  LOAD_FAST                'name'
               72  LOAD_FAST                'self'
               74  LOAD_ATTR                _registered_control_names
               76  COMPARE_OP               in
               78  POP_JUMP_IF_FALSE    92  'to 92'

 L.  46        80  LOAD_GLOBAL              RuntimeError
               82  LOAD_STR                 "a control called '%s' has already been registered"
               84  LOAD_FAST                'name'
               86  BINARY_MODULO    
               88  CALL_FUNCTION_1       1  '1 positional argument'
               90  RAISE_VARARGS_1       1  'exception instance'
             92_0  COME_FROM            78  '78'

 L.  48        92  LOAD_FAST                'message'
               94  LOAD_FAST                'self'
               96  LOAD_ATTR                _registered_messages
               98  COMPARE_OP               in
              100  POP_JUMP_IF_FALSE   114  'to 114'

 L.  49       102  LOAD_GLOBAL              RuntimeError

 L.  50       104  LOAD_STR                 'a control with status %d and note/CC number %d has already been registered'

 L.  51       106  LOAD_FAST                'message'
              108  BINARY_MODULO    
              110  CALL_FUNCTION_1       1  '1 positional argument'
              112  RAISE_VARARGS_1       1  'exception instance'
            114_0  COME_FROM           100  '100'

 L.  54       114  LOAD_FAST                'self'
              116  LOAD_METHOD              component_guard
              118  CALL_METHOD_0         0  '0 positional arguments'
              120  SETUP_WITH          180  'to 180'
              122  POP_TOP          

 L.  55       124  LOAD_GLOBAL              InputControlElement

 L.  56       126  LOAD_GLOBAL              STATUS_TO_TYPE
              128  LOAD_FAST                'status'
              130  LOAD_CONST               240
              132  BINARY_AND       
              134  BINARY_SUBSCR    

 L.  57       136  LOAD_FAST                'status'
              138  LOAD_CONST               15
              140  BINARY_AND       

 L.  58       142  LOAD_FAST                'number'

 L.  59       144  LOAD_FAST                'name'
              146  LOAD_CONST               ('msg_type', 'channel', 'identifier', 'name')
              148  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              150  STORE_FAST               'element'

 L.  61       152  LOAD_FAST                'self'
              154  LOAD_ATTR                _registered_control_names
              156  LOAD_METHOD              append
              158  LOAD_FAST                'name'
              160  CALL_METHOD_1         1  '1 positional argument'
              162  POP_TOP          

 L.  62       164  LOAD_FAST                'self'
              166  LOAD_ATTR                _registered_messages
              168  LOAD_METHOD              append
              170  LOAD_FAST                'message'
              172  CALL_METHOD_1         1  '1 positional argument'
              174  POP_TOP          
              176  POP_BLOCK        
              178  LOAD_CONST               None
            180_0  COME_FROM_WITH      120  '120'
              180  WITH_CLEANUP_START
              182  WITH_CLEANUP_FINISH
              184  END_FINALLY      

 L.  64       186  LOAD_FAST                'element'
              188  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_GLOBAL' instruction at offset 62