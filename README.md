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

```python
from helpers.led_helper import LedHelper

# Onboard LED is availabe on Pin 4 on ESP32
lh = LedHelper()
print('Onboard LED is ON: {}'.format(lh.onboard_led))
# Onboard LED is ON: False

# turn onboard LED on
lh.onboard_led = True

# alternative way to turn onboard LED on
lh.onboard_led_on()

# turn onboard LED off
lh.onboard_led = False

# alternative way to turn onboard LED off
lh.onboard_led_off()

# flash LED for 5 times, with 100ms delay between on and off
lh.flash_led(amount=5, delay_ms=100)
```

##### Advanced

```python
from helpers.led_helper import LedHelper

# Onboard LED is availabe on Pin 4 on ESP32
lh = LedHelper()
print('Onboard LED is ON: {}'.format(lh.onboard_led))

# let LED blink in a seperate thread with 100ms between on and off
lh.blink_led(delay_ms=100)
print('Onboard LED is blinking: {}'.format(lh.blinking))
# Onboard LED is blinking: True

# stop the LED blinking
lh.blinking = False

# set different blinking delay
print('Current blinking delay: {}ms'.format(lh.blink_delay))
# Current blinking delay: 100ms
lh.blink_delay = 50

# start blinking again (with 50ms delay)
lh.blinking = True
```

#### Neopixel

This example demonstrates how to interact with the Neopixel LED.

##### Basics

```python
from helpers.led_helper import LedHelper

# Neopixel is by default attached to Pin 27 on ESP32
lh = LedHelper()
print('Neopixel is ON: {}'.format(lh.neopixel_active))

# turn Neopixel red with 50/255 intensity
lh.neopixel_red(50)
# lh.neopixel_green(50)
# lh.neopixel_blue(50)

lh.neopixel_active = False
# turn Neopixel off

# get the current Neopixel color
print('Neopixel color (RGB): {}'.format(lh.neopixel_color))
# Neopixel color (RGB): [50, 0, 0]

# get all available neopixel colors
lh.neopixel_colors
# >>> {'red': [30, 0, 0], 'green': [0, 30, 0], ...}

# turn Neopixel yellow
lh.neopixel_color = 'yellow'

# get current intensity of Neopixel
print('Neopixel intensity: {}/255'.format(lh.neopixel_intensity))
# Neopixel intensity: 30/255

# reduce Neopixel intensity
lh.neopixel_intensity = 10

# turn Neopixel off, but remember last active color
lh.neopixel_clear()
```

##### Advanced

```python
from helpers.led_helper import LedHelper

# Neopixel is by default attached to Pin 27 on ESP32
lh = LedHelper()

# let Neopixel fade the currently set color in a seperate thread with 100ms
# between intensity changes, 50ms is default and quite smooth
lh.neopixel_fade(delay_ms=100)

# stop the Neopixel fading
lh.fading = False

# set different fading delay
print('Current fading delay: {}ms'.format(lh.fade_delay))
# Current fading delay: 100ms
lh.fade_delay = 50

# start fading again (with 50ms delay)
lh.fading = True

# stop the Neopixel fading
lh.fading = False

# define a custom color and set the Neopixel to it
lh.neopixel_colors = {'DarlingColor': [26, 3, 18]}
lh.neopixel_color = 'DarlingColor'
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
