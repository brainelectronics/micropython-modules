# MicroPython modules

Custom brainelectronics MicroPython helpers, modules and wrappers

---------------

## About

This is a collection of MicroPython modules required for ESP32 and other
brainelectronics projects.

## Available generators

For the individual usage of a helper, module or wrapper read the brief
description and usage instructions of each module.

## Setup

Copy the module(s) to the MicroPython board and import them as shown below

```bash
mkdir /pyboard/helpers
cp helpers/* /pyboard/helpers
```

```python
from helpers.led_helper import LedHelper
```

### LED Helper

Handle the onbaord LED on a ESP32/ESP8266 or Neopixel LEDs.

This example demonstrates how to get the current onboard LED state, set it and
turn the Neopixel LED on at red color.

```python
from helpers.led_helper import LedHelper

# Neopixel is by default attached to Pin 27 on ESP32
# Onboard LED is availabe on Pin 4 on ESP32
lh = LedHelper()
print('Onboard LED is ON: {}'.format(lh.onboard_led))

# turn onboard LED on
lh.onboard_led = True

# alternative way to turn onboard LED on
lh.onboard_led_on()

# turn onboard LED off
lh.onboard_led = False

# alternative way to turn onboard LED off
lh.onboard_led_off()

# turn Neopixel red with 50% intensity
lh.neopixel_red(50)

# turn Neopixel yellow with 10% intensity
lh.neopixel_color(color='yellow', intensity=10)

# get all available neopixel colors
lh.neopixel_colors
# >>> {'red': [30, 0, 0], 'green': [0, 30, 0], ...}

# define a custom color and set the neopixel to it
lh.neopixel_colors = {'myColor': [26, 3, 18]}
lh.neopixel_color(color='myColor')
```

### Path Helper

MicroPython does not have an `os.path.exists()` function. This small module
adds this function.

```python
from helpers.path_helper import PathHelper

path = 'registers/modbusRegisters.json'
isExist = PathHelper.exists(path=path)
print('File at path "{}" does exist: {}'.format(path, isExist))
```
