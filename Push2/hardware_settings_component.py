# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\hardware_settings_component.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 4355 bytes
from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import round
from past.utils import old_div
import weakref, Live
from ableton.v2.base import clamp, listens, task
from ableton.v2.control_surface import Component
LED_FADE_IN_DELAY = 0.3
LED_FADE_IN_TIME = 200
LED_FADE_IN_FREQUENCY = 16
MIN_BRIGHTNESS_FOR_FADE_IN = 0

class HardwareSettingsComponent(Component):

    def __init__(self, led_brightness_element=None, display_brightness_element=None, settings=None, *a, **k):
        (super(HardwareSettingsComponent, self).__init__)(*a, **k)
        self._settings = settings
        self._led_brightness_element = led_brightness_element
        self._display_brightness_element = display_brightness_element
        component_ref = weakref.ref(self)

        def timer_callback():
            if component_ref():
                component_ref()._on_fade_in_led_brightness_timer()

        self._led_brightness_timer = Live.Base.Timer(callback=timer_callback,
          interval=LED_FADE_IN_FREQUENCY,
          repeat=True)
        self._target_led_brightness = 0
        self._led_brightness = 0
        self._fade_in_delay_task = self._tasks.add(task.sequence(task.wait(LED_FADE_IN_DELAY), task.run(self._led_brightness_timer.restart))).kill()
        self._HardwareSettingsComponent__on_led_brightness_changed.subject = settings
        self._HardwareSettingsComponent__on_display_brightness_changed.subject = settings

    def disconnect(self):
        super(HardwareSettingsComponent, self).disconnect()
        self._led_brightness_timer.stop()
        self._led_brightness_timer = None

    def hardware_initialized(self):
        self.fade_in_led_brightness(self._settings.led_brightness)
        self._display_brightness_element.send_value(self._settings.display_brightness)

    def fade_in_led_brightness(self, target_brightness):
        self._led_brightness = MIN_BRIGHTNESS_FOR_FADE_IN
        self._target_led_brightness = target_brightness
        self._led_brightness_element.send_value(MIN_BRIGHTNESS_FOR_FADE_IN)
        self._fade_in_delay_task.restart()

    def stop_fade_in_led_brightness(self):
        self._led_brightness_timer.stop()
        self._led_brightness = self._target_led_brightness = MIN_BRIGHTNESS_FOR_FADE_IN
        self._fade_in_delay_task.kill()

    def _on_fade_in_led_brightness_timer(self):
        if self._led_brightness < self._target_led_brightness:
            distance = float(self._target_led_brightness - MIN_BRIGHTNESS_FOR_FADE_IN)
            increment = old_div(distance, LED_FADE_IN_TIME) * LED_FADE_IN_FREQUENCY
            self._led_brightness = clamp(self._led_brightness + increment, MIN_BRIGHTNESS_FOR_FADE_IN, self._target_led_brightness)
            self._led_brightness_element.send_value(int(round(self._led_brightness)))
        else:
            self._led_brightness_timer.stop()

    @listens('led_brightness')
    def __on_led_brightness_changed(self, value):
        self.stop_fade_in_led_brightness()
        self._led_brightness_element.send_value(value)

    @listens('display_brightness')
    def __on_display_brightness_changed(self, value):
        self._display_brightness_element.send_value(value)

    def send(self):
        self.stop_fade_in_led_brightness()
        self._led_brightness_element.send_value(self._settings.led_brightness)
        self._display_brightness_element.send_value(self._settings.display_brightness)