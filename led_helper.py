#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
handle LED operations on ESP32 Pico D4 board
"""

from machine import Pin
import neopixel
import time

# not natively supported on micropython, see lib/typing.py
from typing import Union


class LedHelper(object):
    """docstring for WifiHelper"""
    def __init__(self,
                 led_pin: Pin = 4,
                 neopixel_pin: Pin = 27,
                 neopixels: int = 1):
        """
        Initialize LedHelper

        :param      led_pin:        Pin of LED
        :type       led_pin:        Pin, optional
        :param      neopixel_pin:   Pin of Neopixel LED
        :type       neopixel_pin:   Pin, optional
        :param      neopixels:      Number of Neopixel LEDs
        :type       neopixels:      int, optional
        """
        self.led_pin = Pin(led_pin, Pin.OUT)
        self.neopixel_pin = Pin(neopixel_pin, Pin.OUT)
        self.pixel = neopixel.NeoPixel(pin=self.neopixel_pin, n=neopixels)
        self.active_color_number = 1     # 0 represents all off

    def flash_led(self, amount: int, delay_ms: int = 50) -> None:
        """
        Flash onboard led for given amount of iterations.

        :param      amount:     The amount of iterations
        :type       amount:     int
        :param      delay_ms:   The delay between a flash in milliseconds
        :type       delay_ms:   int, optional
        """
        self.toggle_pin(pin=self.led_pin, amount=amount, delay_ms=delay_ms)

    @staticmethod
    def toggle_pin(pin: Pin, amount: int, delay_ms: int = 50) -> None:
        """
        Toggle pin for given amount of iterations.

        :param      pin:        The pin to toggle
        :type       pin:        int
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

        :param      red:    The new value
        :type       red:    int, optional
        :param      green:  The green
        :type       green:  int. optional
        :param      blue:   The blue
        :type       blue:   int, optional
        :param      rgb:    The new value
        :type       rgb:    list, optional
        """
        if rgb is None:
            self.pixel[0] = (red, green, blue)
        else:
            self.pixel[0] = tuple(rgb)

        self.pixel.write()

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

    def neopixel_color(self, color: str, intensity: int = 30) -> None:
        """
        Set a predefined neopixel color.

        :param      color:      The color
        :type       color:      str
        :param      intensity:  The intensity
        :type       intensity:  int, optional
        """
        color_code = {
            'red': [intensity, 0, 0],
            'green': [0, intensity, 0],
            'blue': [0, 0, intensity],
            # onwards colors may need adjustment as they are just technically
            # correct, but maybe not colorwise
            'yellow': [intensity, intensity, 0],
            'cyan': [0, intensity, intensity],
            'magenta': [intensity, 0, intensity],
            'white': [intensity, intensity, intensity],
            'maroon': [intensity // 2, 0, 0],
            'darkgreen': [0, intensity // 2, 0],
            'darkblue': [0, 0, intensity // 2],
            'olive': [intensity // 2, intensity // 2, 0],
            'teal': [0, intensity // 2, intensity // 2],
            'purple': [intensity // 2, 0, intensity // 2],
        }
        if color in color_code:
            self.set_neopixel(rgb=color_code[color])

    def neopixel_fade(self,
                      finally_clear: bool = True,
                      delay_ms: int = 250,
                      maximum_intensity: int = 30) -> None:
        """
        Iterate through the neopixel colors.

        :param      finally_clear:      Flag to clear the neopixel finally
        :type       finally_clear:      bool, optional
        :param      delay_ms:           Delay between intensity changes in ms
        :type       delay_ms:           int, optional
        :param      maximum_intensity:  The maximum intensity
        :type       maximum_intensity:  int, optional
        """
        color = self.active_color_number

        if color <= 9:
            # for color in range(0, 8):
            # loop through all possible color combinations

            color_list = list('{:03b}'.format(color))
            # ['0', '0', '1'], ['0', '1', '0'], ['0', '1', '1'] ...

            # set upper intensity limit to 30 to avoid getting blinded by the light
            for intensity in range(0, maximum_intensity + 1, 5):
                # create empty list
                pixel_color = [0] * len(color_list)

                for idx, val in enumerate(color_list):
                    if val == '1':
                        pixel_color[idx] = intensity

                self.set_neopixel(rgb=pixel_color)

                # no delay at the final intensity
                if intensity != maximum_intensity:
                    time.sleep_ms(delay_ms)

            # change to next color on next call
            self.active_color_number += 1
        else:
            self.active_color_number = 1

        if finally_clear:
            self.neopixel_clear()
