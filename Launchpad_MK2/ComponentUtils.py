#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Launchpad_MK2/ComponentUtils.py
from __future__ import absolute_import, print_function, unicode_literals

def skin_scroll_component(component):
    for button in (component.scroll_up_button, component.scroll_down_button):
        button.color = u'Scrolling.Enabled'
        button.pressed_color = u'Scrolling.Pressed'
        button.disabled_color = u'Scrolling.Disabled'
