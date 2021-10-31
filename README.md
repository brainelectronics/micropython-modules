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

Install required dependencies (requires network connection, see WifiHelper)

```python
import upip
upip.install('micropython-ulogging')
```

### Generic Helper

Generic helper class with different usecases and functions.

```python
from helpers.generic_helper import GenericHelper
```

### LED Helper

Handle the onbaord LED on a ESP32/ESP8266 or Neopixel LEDs.

#### Onboard LED

This example demonstrates how to interact with the onboard LED

##### Basics

The onboard LED is availabe on Pin 4 on ESP32 Pico D4 board in inverted mode.

```python
from helpers.led_helper import Led

# Onboard LED is availabe on Pin 4 on ESP32 in inverted mode
led = Led()
print('Onboard LED is ON: {}'.format(led.on))
# Onboard LED is ON: False

# turn onboard LED on
led.state = True

# alternative way to turn onboard LED on
led.turn_on()

# turn onboard LED off
led.state = False

# alternative way to turn onboard LED off
led.turn_off()

# flash LED for 5 times, with 100ms delay between on and off states
# this is blocking other actions until flashing operation finished
led.flash(amount=5, delay_ms=100)
```

##### Advanced

Other (LED) pins can be used by specifiying them at the beginning

```python
from helpers.led_helper import Led

# LED at pin 12 will be active if pin is HIGH
led = Led(led_pin=12, inverted=False)
print('LED is ON: {}'.format(led.on))
```

```python
from helpers.led_helper import Led

# Onboard LED is availabe on Pin 4 on ESP32
led = Led()
print('LED is ON: {}'.format(led.on))

# let LED blink in a seperate thread with 100ms between on and off
led.blink(delay_ms=100)
print('LED is blinking: {}'.format(led.blinking))
# LED is blinking: True

# stop the LED blinking
led.blinking = False

# set different blinking delay
print('Current blinking delay: {}ms'.format(led.blink_delay))
# Current blinking delay: 100ms
led.blink_delay = 50

# start blinking again (with 50ms delay)
led.blinking = True
```

#### Neopixel

This example demonstrates how to interact with the Neopixel LED.

##### Basics

The one Neopixel LED is availabe on Pin 27 on ESP32 Pico D4 board.

```python
from helpers.led_helper import Neopixel

# Neopixel is by default attached to Pin 27 on ESP32
pixel = Neopixel()
print('Neopixel is active: {}'.format(pixel.active))

# turn Neopixel red with 50/255 intensity
pixel.red(50)
# pixel.green(50)
# pixel.blue(50)

pixel.active = False
# turn Neopixel off

# get the current Neopixel color
print('Neopixel color (RGB): {}'.format(pixel.color))
# Neopixel color (RGB): [50, 0, 0]

# get all available neopixel colors
pixel.colors
# >>> {'red': [30, 0, 0], 'green': [0, 30, 0], ...}

# turn Neopixel yellow
pixel.color = 'yellow'

# get current intensity of Neopixel
print('Neopixel intensity: {}/255'.format(pixel.intensity))
# Neopixel intensity: 30/255

# reduce Neopixel intensity to 10/255
pixel.intensity = 10

# turn Neopixel off, but remember last active color
pixel.clear()
```

##### Advanced

Other Neopixel pin can be used by specifiying them at the beginning

```python
from helpers.led_helper import Neopixel

# Neopixel at pin 37 will be active if pin is HIGH
pixel = Neopixel(neopixel_pin=37, neopixels=3)
print('Neopixel is active: {}'.format(pixel.active))
```

```python
from helpers.led_helper import Neopixel

# Neopixel is by default attached to Pin 27 on ESP32
pixel = Neopixel()

# set custom RGB color
pixel.set(rgb=[10, 20, 30])

# let Neopixel fade the currently set color in a seperate thread with 100ms
# between intensity changes, 50ms is default and quite smooth
pixel.fade(delay_ms=100)

# stop the Neopixel fading
pixel.fading = False

# set different fading delay
print('Current fading delay: {}ms'.format(pixel.fade_delay))
# Current fading delay: 100ms
pixel.fade_delay = 50

# start fading again (with 50ms delay)
pixel.fading = True

# stop the Neopixel fading
pixel.fading = False

# define a custom color and set the Neopixel to it
pixel.colors = {'DarlingColor': [26, 3, 18]}
pixel.color = 'DarlingColor'
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

### Time Helper

```python
from helpers.time_helper import TimeHelper

# set the timezone offset to +2, default is +1
th = TimeHelper(tz=2)

# sync the RTC with the NTP server (valid network connection required)
th.sync_time()

# get current timestamp in ISO8601 format
th.current_timestamp_iso8601
# >>> '21:23:55 2021-10-04'

# get current hour from RTC
th.hour
# >>> 21
```

### WiFi Helper

```python
from helpers.wifi_helper import WifiHelper

# connect to the network 'MyNetwork' and it's password 'realPassword1'
result = WifiHelper.connect(ssid='MyNetwork', password='realPassword1', timedout=3)
print('Connection result is: {}'.format(result))

# create an accesspoint named 'MyAP' with a password 'wpa_wpa2_valid_pw'
result = WifiHelper.create_ap(ssid='MyAP', password='wpa_wpa2_valid_pw', channel=10)
print('AP creation result is: {}'.format(result))

wh = WifiHelper()
found_networks = wh.get_wifi_networks_sorted(scan_if_empty=True)
print('Found these networks: {}'.format(found_networks))

# after a scan the networks are available as list of NamedTuple
strongest_network = wh.networks[0].ssid
print('SSID of strongest network: {}'.format(strongest_network))

# convert dBm (RRSI) to quality index in percent
quality = WifiHelper.dbm_to_quality(dBm=wh.networks[0].RSSI)
print('Quality of strongest network {}: {}%'.format(strongest_network, quality))
```
