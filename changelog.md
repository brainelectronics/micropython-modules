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
[Unreleased]: https://github.com/brainelectronics/micropython-modules/compare/0.1.0...develop


[0.1.0]: https://github.com/brainelectronics/micropython-modules/tree/0.1.0
