#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
handle LED operations on ESP32 Pico D4 board
"""

from machine import Pin
import neopixel
import time

led_pin = Pin(4, Pin.OUT)
neopixel_pin = Pin(27, Pin.OUT)
pixel = neopixel.NeoPixel(pin=neopixel_pin, n=1)
active_color_number = 1     # 0 represents all off


def flash_led(amount: int, delay: int = 50) -> None:
    """
    Flash onboard led for given amount of iterations.

    :param      amount:  The amount of iterations
    :type       amount:  int
    :param      delay:   The delay between a flash in milliseconds
    :type       delay:   int, optional
    """
    global led_pin
    toggle_pin(pin=led_pin, amount=amount, delay=delay)


def toggle_pin(pin: int, amount: int, delay: int = 50) -> None:
    """
    Toggle pin for given amount of iterations.

    :param      pin:     The pin to toggle
    :type       pin:     int
    :param      amount:  The amount of iterations
    :type       amount:  int
    :param      delay:   The delay between a pin change in milliseconds
    :type       delay:   int, optional
    """
    for x in range(1, amount + 1):
        pin.value(not pin.value())
        time.sleep_ms(delay)
        pin.value(not pin.value())
        time.sleep_ms(delay)


def onboard_led_on() -> None:
    """
    Turn onboard led on.

    LED is soldered from +3.3V to pin 4
    """
    global led_pin
    led_pin.value(0)


def onboard_led_off() -> None:
    """
    Turn onboard led off.

    LED is soldered from +3.3V to pin 4
    """
    global led_pin
    led_pin.value(1)


def neopixel_clear() -> None:
    """
    Turn neopixel off by setting the RGB color to [0, 0, 0]
    """
    set_neopixel(rgb=[0, 0, 0])


def set_neopixel(red: int = 0,
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
    global pixel

    if rgb is None:
        pixel[0] = (red, green, blue)
    else:
        pixel[0] = tuple(rgb)

    pixel.write()


def neopixel_red(intensity: int = 30) -> None:
    """
    Set the neopixel to red.

    :param      intensity:  The intensity
    :type       intensity:  int, optional
    """
    set_neopixel(red=intensity)


def neopixel_green(intensity: int = 30) -> None:
    """
    Set the neopixel to green.

    :param      intensity:  The intensity
    :type       intensity:  int, optional
    """
    set_neopixel(green=intensity)


def neopixel_blue(intensity: int = 30) -> None:
    """
    Set the neopixel to blue.

    :param      intensity:  The intensity
    :type       intensity:  int, optional
    """
    set_neopixel(blue=intensity)


def neopixel_color(color: str, intensity: int = 30) -> None:
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
        set_neopixel(rgb=color_code[color])


def neopixel_fade(finally_clear: bool = True,
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
    global active_color_number

    color = active_color_number

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

            set_neopixel(rgb=pixel_color)

            # no delay at the final intensity
            if intensity != maximum_intensity:
                time.sleep_ms(delay_ms)

        # change to next color on next call
        active_color_number += 1
    else:
        active_color_number = 1

    if finally_clear:
        neopixel_clear()
