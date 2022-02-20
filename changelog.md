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

## [Unreleased]
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

## Released
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
[Unreleased]: https://github.com/brainelectronics/micropython-modules/compare/0.2.0...develop

[0.2.0]: https://github.com/brainelectronics/micropython-modules/tree/0.2.0
[0.1.0]: https://github.com/brainelectronics/micropython-modules/tree/0.1.0
