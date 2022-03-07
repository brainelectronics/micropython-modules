# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

<!--
## [x.y.z] - yyyy-mm-dd
### Added
### Changed
### Removed
### Fixed
-->

## Released
## [1.2.0] - 2022-03-06
### Added
- [`version.py`](be_helpers/version.py) provides info as semver tuple with
  `__version_info__`
- Raw and human encoded system info data is provided by function
  `get_system_infos_raw` and `get_system_infos_human` of
  [`generic_helper.py`](be_helpers/generic_helper.py)

### Changed
- `gc.collect()` is no longer called on `client_data` property access of
  [`modbus_bridge.py`](be_helpers/modbus_bridge.py)

### Fixed
- Adopted import paths of Generic helper, Led, Neopixel, Path helper, Time
  helper and WiFi helper examples in [`README`](README.md).

## [1.1.2] - 2022-02-26
### Fixed
- Adopted import path of `modbus_bridge` in Modbus Bridge example in
  [`README`](README.md).
- Adopted import paths of `umodbus` files in
  [`modbus_bridge.py`](be_helpers/modbus_bridge.py)
- Provide installation instructions for `micropython-modbus` library in
  [`README`](README.md)
- Call `setup_registers` for either TCP or RTU client, not only in TCP client
  mode in [`modbus_bridge.py`](be_helpers/modbus_bridge.py)

## [1.1.1] - 2022-02-25
### Fixed
- Adopted import paths of `typing` module in all modules from
 `from typing import *` to `from .typing import *`
- Do not import any modules in [`__init__.py`](be_helpers/__init__.py) other
  than [`version.py`](be_helpers/version.py) to avoid issues and gain speed

## [1.1.0] - 2022-02-25
### Added
- [`message.py`](be_helpers/message.py) and [`queue.py`](be_helpers/queue.py)
  taken from [peterhinch's micropython async repo][ref-peterhinch-async]

## [1.0.0] - 2022-02-24
### Added
- [`setup.py`](setup.py) and [`sdist_upip.py`](sdist_upip.py) taken from
  [pfalcon's picoweb repo][ref-pfalcon-picoweb-sdist-upip] and PEP8 improved
- [`MIT License`](LICENSE)
- [`version.py`](be_helpers/version.py) storing current library version

### Changed
- Moved all helper files into folder named [`be_helpers`](be_helpers)
- Update [`README`](README.md) usage description of MicroPython lib deploy to
  [PyPi][ref-pypi]
- Usage examples in [`README`](README.md) updated with new import path
- Use `upip_utarfile` instead of external `micropython-utarfile` in
  [`update_helper.py`](be_helpers/update_helper.py)

### Removed
- Dependency to `micropython-utarfile` by using built-in `upip_utarfile`

## [0.2.0] - 2022-02-20
### Added
- Modbus data between RTU and TCP can be synchronized continously. Access to
  client is secured by thread lock ressource.

### Changed
- Reduce modbus logging output of get and set functions from `INFO` to `DEBUG`
- Returned dict of `read_all_registers` clusters registers by type instead of
  register names
- Tuple of failed and successfully updated registers dict is returned on
  register write functions instead of dictionary of failed registers only
- Setting and getting register data is done in try-catch block to avoid errors
  on unavailable registers or invalid response data
- Log client register data as JSON instead of dict to improve later logging
  data usage
- Default logging level of `ModbusBridge` increased from `DEBUG` to `WARNING`

### Fixed
- Update host and client unit on setting new connections settings
- Set logging level `INFO` not `DEBUG` if desired logger level is `info`
- Return dictionary of read content in `read_all_registers`

## [0.1.0] - 2022-02-19
### Added
- This changelog file
- [`.gitignore`](.gitignore) file
- [`README`](README.md) file with usage examples
- [`PathHelper`](path_helper.py) module added to provide `os.path.exists()`
  function
- [`ModbusBridge`](modbus_bridge.py) module to connect RTU with TCP and vice
  versa

### Changed
- `LED` and `Neopixel` helper module converted into classes of
  [`led_helper`](led_helper.py)
- [`TimeHelper`](time_helper.py) module converted into class
- [`WifiHelper`](wifi_helper.py) module converted into class

<!-- Links -->
[Unreleased]: https://github.com/brainelectronics/micropython-modules/compare/1.2.0...develop

[1.2.0]: https://github.com/brainelectronics/micropython-modules/tree/1.2.0
[1.1.2]: https://github.com/brainelectronics/micropython-modules/tree/1.1.2
[1.1.1]: https://github.com/brainelectronics/micropython-modules/tree/1.1.1
[1.1.0]: https://github.com/brainelectronics/micropython-modules/tree/1.1.0
[1.0.0]: https://github.com/brainelectronics/micropython-modules/tree/1.0.0
[0.2.0]: https://github.com/brainelectronics/micropython-modules/tree/0.2.0
[0.1.0]: https://github.com/brainelectronics/micropython-modules/tree/0.1.0

[ref-pypi]: https://pypi.org/
[ref-pfalcon-picoweb-sdist-upip]: https://github.com/pfalcon/picoweb/blob/b74428ebdde97ed1795338c13a3bdf05d71366a0/sdist_upip.py
[ref-peterhinch-async]: https://github.com/peterhinch/micropython-async/tree/a87bda1b716090da27fd288cc8b19b20525ea20c/v3/primitives

