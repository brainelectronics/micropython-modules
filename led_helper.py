#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
handle LED operations on ESP32 Pico D4 board
"""

from machine import Pin
import neopixel
import _thread
import time

# not natively supported on micropython, see lib/typing.py
from typing import Union


class LedHelper(object):
    """docstring for LedHelper"""
    def __init__(self,
                 led_pin: int = 4,
                 neopixel_pin: int = 27,
                 neopixels: int = 1):
        """
        Initialize LedHelper.
        Default Neopixel color is red with intensity of 30/255

        :param      led_pin:        Pin of LED
        :type       led_pin:        int, optional
        :param      neopixel_pin:   Pin of Neopixel LED
        :type       neopixel_pin:   int, optional
        :param      neopixels:      Number of Neopixel LEDs
        :type       neopixels:      int, optional
        """
        self.led_pin = Pin(led_pin, Pin.OUT)
        neopixel_pin = Pin(neopixel_pin, Pin.OUT)
        self.pixel = neopixel.NeoPixel(pin=neopixel_pin, n=neopixels)

        # neopixel specific defines
        # 30/255 as default intensity to aviod getting blinded by the lights
        self._neopixel_colors = {
            'red': [30, 0, 0],
            'green': [0, 30, 0],
            'blue': [0, 0, 30],
            # onwards colors may need adjustment as they are just technically
            # correct, but maybe not colorwise
            'yellow': [30, 30, 0],
            'cyan': [0, 30, 30],
            'magenta': [30, 0, 30],
            'white': [30, 30, 30],
            'maroon': [30 // 2, 0, 0],
            'darkgreen': [0, 30 // 2, 0],
            'darkblue': [0, 0, 30 // 2],
            'olive': [30 // 2, 30 // 2, 0],
            'teal': [0, 30 // 2, 30 // 2],
            'purple': [30 // 2, 0, 30 // 2],
        }
        self._pwmtable_8D = [0, 1, 2, 2, 2, 3, 3, 4, 5, 6, 7, 8, 10, 11, 13, 16, 19, 23, 27, 32, 38, 45, 54, 64, 76, 91, 108, 128, 152, 181, 215, 255]
        self._neopixel_intensity = 30
        self._last_neopixel_intensity = self._neopixel_intensity
        self._neopixel_active = False
        self._neopixel_color = self._neopixel_colors['red']

        # blink specific defines
        self._blink_lock = _thread.allocate_lock()
        self._blink_delay = 250

        # fade specific defines
        self._fade_lock = _thread.allocate_lock()
        self._fade_delay = 50
        self._fading = False

    def flash_led(self, amount: int, delay_ms: int = 50) -> None:
        """
        Flash onboard led for given amount of iterations.

        :param      amount:     The amount of iterations
        :type       amount:     int
        :param      delay_ms:   The delay between a flash in milliseconds
        :type       delay_ms:   int, optional
        """
        self.toggle_pin(pin=self.led_pin, amount=amount, delay_ms=delay_ms)

    def blink_led(self, delay_ms: int = 250) -> None:
        """
        Blink onboard LED. Wrapper around property usage.

        :param      delay_ms:  The delay between pin changes in milliseconds
        :type       delay_ms:  int
        """
        self.blink_delay = delay_ms
        self.blinking = True

    def _blink(self, delay_ms: int, lock: lock) -> None:
        """
        Internal blink thread content.

        :param      delay_ms:  The delay between pin changes in milliseconds
        :type       delay_ms:  int
        :param      lock:      The lock object
        :type       lock:      lock
        """
        while lock.locked():
            self.onboard_led = not self.onboard_led
            time.sleep_ms(delay_ms)

        # turn LED finally off
        self.onboard_led_off()

    @property
    def blink_delay(self) -> int:
        """
        Get the blink delay in milliseconds.

        :returns:   Delay between pin changes in milliseconds
        :rtype:     int
        """
        return self._blink_delay

    @blink_delay.setter
    def blink_delay(self, delay_ms: int) -> None:
        """
        Set the blink delay in milliseconds.

        :param      delay_ms:  The delay between pin changes in milliseconds
        :type       delay_ms:  int
        """
        if delay_ms < 1:
            delay_ms = 1
        self._blink_delay = delay_ms

    @property
    def blinking(self) -> bool:
        """
        Get the blinking status.

        :returns:   Flag whether LED is blinking or not
        :rtype:     bool
        """
        return self._blink_lock.locked()

    @blinking.setter
    def blinking(self, value: bool) -> None:
        """
        Start or stop blinking of the onboard LED.

        :param      value:  The value
        :type       value:  bool
        """
        if value and (not self._blink_lock.locked()):
            # start blinking if not already blinking
            self._blink_lock.acquire()
            params = (self.blink_delay, self._blink_lock)
            _thread.start_new_thread(self._blink, params)
        elif (value is False) and self._blink_lock.locked():
            # stop blinking if not already stopped
            self._blink_lock.release()

    @staticmethod
    def toggle_pin(pin: Pin, amount: int, delay_ms: int = 50) -> None:
        """
        Toggle pin for given amount of iterations.

        :param      pin:        The pin to toggle
        :type       pin:        Pin
        :param      amount:     The amount of iterations
        :type       amount:     int
        :param      delay_ms:   The delay between a pin change in milliseconds
        :type       delay_ms:   int, optional
        """
        for x in range(1, amount + 1):
            pin.value(not pin.value())
            time.sleep_ms(delay_ms)
            pin.value(not pin.value())
            time.sleep_ms(delay_ms)

    @property
    def onboard_led(self) -> int:
        """
        Get state of onboard LED.

        LED is soldered from +3.3V to pin 4

        :returns:   State of onboard LED
        :rtype:     int
        """
        return not self.led_pin.value()

    @onboard_led.setter
    def onboard_led(self, value: Union[bool, int]) -> None:
        """
        Turn onboard led on or off.

        LED is soldered from +3.3V to pin 4
        """
        if bool(value) is False:
            # HIGH turns LED off
            self.led_pin.on()
        else:
            # LOW turns LED on
            self.led_pin.off()

    def onboard_led_on(self) -> None:
        """
        Turn onboard led on.
        """
        self.onboard_led = True

    def onboard_led_off(self) -> None:
        """
        Turn onboard led off.
        """
        self.onboard_led = False

    def neopixel_clear(self) -> None:
        """
        Turn neopixel off by setting the RGB color to [0, 0, 0]
        """
        self.set_neopixel(rgb=[0, 0, 0])

    def set_neopixel(self,
                     red: int = 0,
                     green: int = 0,
                     blue: int = 0,
                     rgb: list = None) -> None:
        """
        Set the neopixel color.

        A RGB value can be specified by a list or by setting the individual color.

        :param      red:    The red value
        :type       red:    int, optional
        :param      green:  The green value
        :type       green:  int, optional
        :param      blue:   The blue value
        :type       blue:   int, optional
        :param      rgb:    The RGB value
        :type       rgb:    list, optional
        """
        if rgb is None:
            color = (red, green, blue)
        else:
            color = tuple(rgb)

        self.pixel[0] = color
        self.pixel.write()

        # update neopixel properties
        if color != (0, 0, 0):
            self.neopixel_active = True
            if not self.fading:
                # only update if not called by fading
                # intensity would finally be 1 or zero
                self.neopixel_color = list(color)
                self.neopixel_intensity = max(color)
        else:
            # only update if not called by fading
            # neopixel would be cleared after every cycle
            if not self.fading:
                self.neopixel_active = False
                # do not clear color or intensity property

    def neopixel_red(self, intensity: int = 30) -> None:
        """
        Set the neopixel to red.

        :param      intensity:  The intensity
        :type       intensity:  int, optional
        """
        self.set_neopixel(red=intensity)

    def neopixel_green(self, intensity: int = 30) -> None:
        """
        Set the neopixel to green.

        :param      intensity:  The intensity
        :type       intensity:  int, optional
        """
        self.set_neopixel(green=intensity)

    def neopixel_blue(self, intensity: int = 30) -> None:
        """
        Set the neopixel to blue.

        :param      intensity:  The intensity
        :type       intensity:  int, optional
        """
        self.set_neopixel(blue=intensity)

    @property
    def neopixel_color(self) -> list:
        """
        Get the current set color of the Neopixel

        :returns:   Neopixel color if active
        :rtype:     list
        """
        return self._neopixel_color

    @neopixel_color.setter
    def neopixel_color(self, color: Union[list, str]) -> None:
        """
        Set a Neopixel color.

        :param      color:      The color
        :type       color:      Union[list, str]
        """
        if isinstance(color, str):
            if color in self.neopixel_colors:
                color = self.neopixel_colors[color]
            else:
                print('Color "{}" unknown, may add this color with '
                      '"neopixel_colors" function'.format(color))
                return

        if color != self.neopixel_color:
            self._neopixel_color = color

            if color != [0, 0, 0]:
                self.set_neopixel(rgb=color)
            else:
                self.neopixel_clear()

    @property
    def neopixel_intensity(self) -> int:
        """
        Get current Neopixel intensity.

        :returns:   Neopixel intensity
        :rtype:     int
        """
        return self._neopixel_intensity

    @neopixel_intensity.setter
    def neopixel_intensity(self, intensity: int) -> None:
        """
        Set new intensity for Neopixel.

        If Neopixel is active and is showing a color, the new intensity ratio
        will be applied

        :param      intensity:  The intensity
        :type       intensity:  int
        """
        do_update = False
        self._last_neopixel_intensity = intensity

        # update neopixel if new intensity is different from current one and
        # the Neopixel is currently active
        if ((self.neopixel_intensity != self._last_neopixel_intensity) and
            self.neopixel_active):
            # apply new intensity only if a valid color is set
            if self.neopixel_color != [0, 0, 0]:
                do_update = True

        if not intensity:
            self.neopixel_clear()

        self._neopixel_intensity = intensity

        if do_update:
            # intensity = 40
            # color = [60, 10, 7]
            # maximum_brightness = max(color) # 60
            # ratio = maximum_brightness / intensity  # 1.5
            # new_color = [round(ele / ratio) for ele in color]
            #  -> [40, 7, 5]
            ratio = max(self.neopixel_color) / intensity
            new_color = [round(ele / ratio) for ele in self.neopixel_color]
            self.set_neopixel(rgb=new_color)

    @property
    def neopixel_active(self) -> bool:
        """
        Get current status of Neopixel

        :returns:   Flag whether Neopixel is active or not
        :rtype:     bool
        """
        return self._neopixel_active

    @neopixel_active.setter
    def neopixel_active(self, value: bool) -> None:
        if value != self.neopixel_active:
            self._neopixel_active = value

            if value:
                self.set_neopixel(rgb=self.neopixel_color)
            else:
                self.neopixel_clear()

    @property
    def neopixel_colors(self) -> dict:
        """
        Get available colors of Neopixel.

        :returns:   Neopixel colors and their RGB value
        :rtype:     dict
        """
        return self._neopixel_colors

    @neopixel_colors.setter
    def neopixel_colors(self, value: dict) -> None:
        """
        Add new colors or change RGB value of existing color

        :param      value:  Color name as key and RGB intensity list as value
        :type       value:  dict
        """
        self._neopixel_colors.update(value)

    def neopixel_fade(self, delay_ms: int = 50) -> None:
        """
        Fade WS2812 LED. Wrapper around property usage.

        A fade delay below 30ms is not recommened due to high CPU load.
        REPL might get slow.

        :param      delay_ms:  The delay between intensity changes in milliseconds
        :type       delay_ms:  int
        """
        self.fade_delay = delay_ms
        self.fading = True

    def _fade(self, delay_ms: int, lock: lock) -> None:
        """
        Internal Neopixel fading thread content.

        :param      delay_ms:  The delay between intensity changes in milliseconds
        :type       delay_ms:  int
        :param      lock:      The lock object
        :type       lock:      lock
        """
        # find smallest value which is not zero in latest neopixel_color list
        maximum_intensity = min([val for val in self.neopixel_color if val != 0])

        # find closest match of maximum_intensity in _pwmtable_8D
        # set this as maximum_intensity
        closest_match = min(self._pwmtable_8D, key=lambda x: abs(x - maximum_intensity))
        closest_match_index = self._pwmtable_8D.index(closest_match)

        while lock.locked():
            for val in self._pwmtable_8D[:closest_match_index]:
                pixel_color = [val if ele != 0 else 0 for ele in self.neopixel_color]
                self.set_neopixel(rgb=pixel_color)
                time.sleep_ms(delay_ms)

            for val in self._pwmtable_8D[:closest_match_index][::-1]:
                pixel_color = [val if ele != 0 else 0 for ele in self.neopixel_color]
                self.set_neopixel(rgb=pixel_color)
                time.sleep_ms(delay_ms)

        # turn LED finally off
        self.neopixel_active = False
        self._fading = False

    @property
    def fade_delay(self) -> int:
        """
        Get the fade delay in milliseconds.

        :returns:   Delay between intensity changes in milliseconds
        :rtype:     int
        """
        return self._fade_delay

    @fade_delay.setter
    def fade_delay(self, delay_ms: int) -> None:
        """
        Set the Neopixel fade delay in milliseconds.

        :param      delay_ms:  The delay between intensity changes in milliseconds
        :type       delay_ms:  int
        """
        if delay_ms < 1:
            delay_ms = 1
        self._fade_delay = delay_ms

    @property
    def fading(self) -> bool:
        """
        Get the fading status.

        :returns:   Flag whether neopixel is fading or not
        :rtype:     bool
        """
        # returning self._fade_lock.locked() is not sufficient, as it will be
        # False after "fading = False" is called and the remaining
        # "set_neopixel" calls would change the color and intensity property
        # values until the for loop of "_fade" is finished
        return self._fading

    @fading.setter
    def fading(self, value: bool) -> None:
        """
        Start or stop fading of the Neopixel.

        :param      value:  The value
        :type       value:  bool
        """
        if value and (not self._fade_lock.locked()):
            # start blinking if not already blinking
            self._fade_lock.acquire()
            self.neopixel_active = True
            self._fading = True
            params = (self.fade_delay, self._fade_lock)
            _thread.start_new_thread(self._fade, params)
        elif (value is False) and self._fade_lock.locked():
            # stop fading if not already stopped
            self._fade_lock.release()
