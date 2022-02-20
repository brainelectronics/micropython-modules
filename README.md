# MicroPython modules

Custom brainelectronics MicroPython helpers, modules and wrappers

---------------

## About

This is a collection of MicroPython modules required for the BE32-01 and other
brainelectronics projects.

## Available generators

For the individual usage of a helper, module or wrapper read the brief
description and usage instructions of each module.

<!-- TOC -->
 - [Generic Helper](#generic-helper)
 - [LED Helper](#led-helper)
     - [Onboard LED](#onboard-led)
     - [Neopixel](#neopixel)
 - [Modbus TCP-RTU bridge](#modbus-bridge)
 - [Path Helper](#path-helper)
 - [Time Helper](#time-helper)
 - [WiFi Helper](#wifi-helper)

## Setup

Copy the module(s) to the MicroPython board and import them as shown below
using [Remote MicroPython shell][ref-remote-upy-shell]

```bash
mkdir /pyboard/helpers
cp helpers/* /pyboard/helpers
```

Install required dependencies (requires network connection, see may use the
[`WifiHelper`][ref-wifi-helper])

```python
import upip
upip.install('micropython-ulogging')
# upip.install('micropython-utarfile')
```

### Generic Helper

Generic helper class with different usecases and functions.

```python
from helpers.generic_helper import GenericHelper

# get a random value between zero and 100 (inclusive)
GenericHelper.get_random_value(0, 100)
# >>> 72

# get amount of free disk space in kilobytes
GenericHelper.df(path='/', unit='kb')
# >>> '1984.000 kB'

# get dict of free RAM with total, free and percentage used
GenericHelper.get_free_memory()
# >>> {'percentage': '99.76%', 'total': 4098240, 'free': 4088400}

# get detailed info (full == True) RAM informations
GenericHelper.free(full=True)
# >>> 'Total: 4006.1 kB, Free: 3992.56 kB (99.76%)'

# interpret a string as dictionary
some_string = "{'klaus': 123}"
d = GenericHelper.str_to_dict(data=some_string)
type(d)
# >>> <class 'dict'>

# save a dictionary as JSON file
GenericHelper.save_json(path='/test.json', data=d)

# load a JSON file as dictionary
read_back_dict = GenericHelper.load_json(path='/test.json')
read_back_dict
# >>> {'klaus': 123}

read_back_dict == d
# >>> True

# save a string to file in non binary mode
GenericHelper.save_file(path='/test.txt', data=some_string, mode='w')

# load the content of a file in non binary mode
read_back_str = GenericHelper.load_file(path='/test.txt', mode='r')
read_back_str
# >>> "{'klaus': 123}"

read_back_str == some_string
# >>> True
```

### LED Helper

Handle the onbaord LED on a BE32-01, ESP32 or ESP8266 as well as Neopixel LEDs.

#### Onboard LED

This example demonstrates how to interact with the onboard LED on the BE32-01

##### Basics

The onboard LED is availabe on Pin 4 on the BE32-01 board in inverted mode.

```python
from helpers.led_helper import Led

# Onboard LED is availabe on Pin 4 on BE32-01 in inverted mode
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

# Onboard LED is availabe on Pin 4 on BE32-01
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

This example demonstrates how to interact with the Neopixel LED on the BE32-01.

##### Basics

The one Neopixel LED is availabe on Pin 27 on the BE32-01 board.

```python
from helpers.led_helper import Neopixel

# Neopixel is by default attached to Pin 27 on BE32-01
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

# Neopixel is by default attached to Pin 27 on BE32-01
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

### Modbus Bridge

This requires [brainelectronics MicroPython Modbus][ref-be-upy-modbus]. Forked
and extended from [SFERALABS Exo Sense Py][ref-sferalabs-exo-sense].

```python
import time
import machine

from helpers.modbus_bridge import ModbusBridge

register_file = 'registers/modbusRegisters-MyEVSE.json'
rtu_pins = (25, 26)     # (TX, RX)
tcp_port = 180          # TCP port for Modbus connection
run_time = 60           # run this example for this amount of seconds

# default level is 'warning', may use custom logger to get initial log data
mb_bridge = ModbusBridge(register_file=register_file)

# define and apply Modbus TCP host settings
host_settings = {
    'type': 'tcp',
    'unit': tcp_port,
    'address': -1,
    'baudrate': -1,
    'mode': 'master'
}
mb_bridge.connection_settings_host = host_settings

# setup Modbus connections to host and client
mb_bridge.setup_connection(pins=rtu_pins)   # (TX, RX)

print('Modbus instances:')
print('\t Act as Host: {} on {}'.format(mb_bridge.host, mb_bridge.host_unit))
print('\t Act as Client: {} on {}'.format(mb_bridge.client, mb_bridge.client_unit))

# readout the client registers once manually
# mb_bridge.read_all_registers()

# start collecting latest RTU client data in thread and TCP data provision
mb_bridge.collecting_client_data = True
mb_bridge.provisioning_host_data = True

print('Run client and host for {} seconds'.format(run_time))
print('Collect latest client data every {} seconds'.format(mb_bridge.collection_interval))
print('Synchronize Host-Client every {} seconds'.format(mb_bridge.synchronisation_interval))

start_time = time.time()
while time.time() < (start_time + run_time):
    try:
        machine.idle()
    except KeyboardInterrupt:
        print('KeyboardInterrupt, stop collection + provisioning after {}'.
              format(time.time() - start_time))
        break
    except Exception as e:
        print('Exception: {}'.format(e))

# stop collecting latest client data in thread and data provision via TCP
mb_bridge.collecting_client_data = False
mb_bridge.provisioning_host_data = False

# wait for 5 more seconds to safely finish the may still running threads
time.sleep(5)
```

### Path Helper

MicroPython does not have an `os.path.exists()` function. This small module
adds this function.

```python
from helpers.path_helper import PathHelper

path = 'registers/modbusRegisters.json'
result = PathHelper.exists(path=path)
print('File at path "{}" does exist: {}'.format(path, result))
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

# connect to the network 'MyNet' and it's password 'realPassword1'
result = WifiHelper.connect(ssid='MyNet', password='realPassword1', timedout=3)
print('Connection result is: {}'.format(result))

# create an accesspoint named 'MyAP' with a password 'wpa_wpa2_valid_pw'
result = WifiHelper.create_ap(ssid='MyAP', password='wpa_wpa2_valid_pw', channel=10)
print('AP creation result is: {}'.format(result))

wh = WifiHelper()
found_networks = wh.get_wifi_networks_sorted(scan_if_empty=True)
print('Found these networks: {}'.format(found_networks))

# after a scan the networks are available as list of NamedTuple
strongest_net = wh.networks[0].ssid
print('SSID of strongest network: {}'.format(strongest_net))

# convert dBm (RRSI) to quality index in percent
quality = WifiHelper.dbm_to_quality(dBm=wh.networks[0].RSSI)
print('Quality of strongest network {}: {}%'.format(strongest_net, quality))
```

<!-- Links -->
[ref-remote-upy-shell]: https://github.com/dhylands/rshell
[ref-wifi-helper]: wifi_helper.py
[ref-be-upy-modbus]: https://github.com/brainelectronics/micropython-modbus
[ref-sferalabs-exo-sense]: https://github.com/sfera-labs/exo-sense-py-modbus
