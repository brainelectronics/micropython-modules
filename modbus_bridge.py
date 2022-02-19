#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Modbus Bridge

Create bridge between RTU and TCP modbus requests
"""

# system packages
import gc
import network

# pip installed packages
# import picoweb
# https://github.com/pfalcon/picoweb/blob/b74428ebdde97ed1795338c13a3bdf05d71366a0/picoweb/
from uModbus.serial import Serial as ModbusRTUMaster
from uModbus.tcp import TCP as ModbusTCPMaster
# https://github.com/brainelectronics/micropython-modbus/
from primitives.message import Message
# https://github.com/peterhinch/micropython-async/blob/a87bda1b716090da27fd288cc8b19b20525ea20c/v3/primitives/

# custom packages
from helpers.generic_helper import GenericHelper
from helpers.path_helper import PathHelper
from modbus import ModbusRTU
from modbus import ModbusTCP

# not natively supported on micropython, see lib/typing.py
from typing import Dict, List, Tuple, Union


class ModbusBridgeError(Exception):
    """Base class for exceptions in this module."""
    pass


class ModbusBridge(object):
    """docstring for ModbusBridge"""
    def __init__(self, register_file: str, logger=None, quiet: bool = False):
        # setup and configure logger if none is provided
        if logger is None:
            logger = GenericHelper.create_logger(logger_name=self.__class__.__name__)
            GenericHelper.set_level(logger, 'debug')
        self.logger = logger
        self.logger.disabled = quiet

        self._register_file = ''
        self._register_definitions = dict()
        self._connection_settings_host = dict()
        self._connection_settings_client = dict()
        self._client_unit = 0
        self._host_unit = 0
        self._client = None
        self._host = None

        # set register file and load its definitions
        self.register_file = register_file
        self.register_definitions = self._load_register_file()

        # load connection definitions from register definitions
        self._load_connection_settings()

        # run garbage collector at the end to clean up
        gc.collect()

    @property
    def register_file(self) -> str:
        """
        Get Modbus register file path

        :returns:   Path to Modbus register file
        :rtype:     str
        """
        return self._register_file

    @register_file.setter
    def register_file(self, path: str) -> None:
        """
        Set Modbus register file path

        :param      path:  The path to the Modbus register file
        :type       path:  str
        """
        if PathHelper.exists(path=path):
            self._register_file = path
        else:
            raise ModbusBridgeError('Given register file {} does not exist'.
                                    format(path))

    @property
    def register_definitions(self) -> dict:
        """
        Get Modbus register definitions

        As this implements a bridge, host and client registers are the same

        :returns:   Modbus register definitions
        :rtype:     dict
        """
        return self._register_definitions

    @register_definitions.setter
    def register_definitions(self, val: dict) -> None:
        """
        Set Modbus register definitions.

        As this implements a bridge, host and client registers shall be same

        :param      val:  The Modbus register definitions
        :type       val:  dict
        """
        if val:
            self._register_definitions = val

    @property
    def connection_settings_host(self) -> dict:
        """
        Get Modbus connection settings of/to host

        :returns:   Modbus connection settings
        :rtype:     dict
        """
        return self._connection_settings_host

    @connection_settings_host.setter
    def connection_settings_host(self, val: dict) -> None:
        """
        Set Modbus connection settings of/to host

        :param      val:  The Modbus connection settings
        :type       val:  dict
        """
        if val:
            self._connection_settings_host = val

            if val.get('unit', ''):
                unit = val['unit']
                self.logger.debug('Update host connection unit to: {}'.
                                  format(unit))
                self.host_unit = unit

    @property
    def connection_settings_client(self) -> dict:
        """
        Get Modbus connection settings of/to client

        :returns:   Modbus connection settings
        :rtype:     dict
        """
        return self._connection_settings_client

    @connection_settings_client.setter
    def connection_settings_client(self, val: dict) -> None:
        """
        Set Modbus connection settings of/to client

        :param      val:  The Modbus connection settings
        :type       val:  dict
        """
        if val:
            self._connection_settings_client = val

            if val.get('unit', ''):
                unit = val['unit']
                self.logger.debug('Update client connection unit to: {}'.
                                  format(unit))
                self.client_unit = unit

    @property
    def client(self) -> Union[None, None]:
        """
        Get Modbus client instance

        :returns:   Modbus client instance
        :rtype:     Union[None, None]
        """
        return self._client

    @client.setter
    def client(self, value: Union[None, None]) -> None:
        """
        Set Modbus client instance

        :param      value:  The Modbus client
        :type       value:  Union[None, None]
        """
        self._client = value

    @property
    def host(self) -> Union[None, None]:
        """
        Get Modbus host instance

        :returns:   Modbus host instance
        :rtype:     Union[None, None]
        """
        return self._host

    @host.setter
    def host(self, value: Union[None, None]) -> None:
        """
        Set Modbus host instance

        :param      value:  The Modbus host
        :type       value:  Union[None, None]
        """
        self._host = value

    @property
    def client_unit(self) -> int:
        """
        Get Modbus client unit

        :returns:   Modbus client unit
        :rtype:     int
        """
        return self._client_unit

    @client_unit.setter
    def client_unit(self, val: int) -> None:
        """
        Set Modbus client unit

        :param      value:  The Modbus client unit
        :type       value:  int
        """
        if isinstance(val, int):
            self._client_unit = val
        else:
            raise ModbusBridgeError('Client unit shall be int, not {}'.
                                    format(type(val)))

    @property
    def host_unit(self) -> int:
        """
        Get Modbus host unit

        :returns:   Modbus host unit
        :rtype:     int
        """
        return self._host_unit

    @host_unit.setter
    def host_unit(self, val: int) -> None:
        """
        Set Modbus host unit

        :param      value:  The Modbus host unit
        :type       value:  int
        """
        if isinstance(val, int):
            self._host_unit = val
        else:
            raise ModbusBridgeError('Host unit shall be int, not {}'.
                                    format(type(val)))

    def _load_register_file(self) -> Dict[dict]:
        """
        Load JSON register file.

        :returns:   Defined Modbus registers
        :rtype:     Dict[dict]
        """
        registers = dict()

        path = self.register_file

        if PathHelper.exists(path=path):
            registers = GenericHelper.load_json(path=path)
        else:
            self.logger.warning('No register file {} found'.format(path))

        return registers

    def _load_connection_settings(self) -> None:
        """Load Modbus connection settings from Modbus registers."""
        config_keyword = 'CONNECTION'

        # type "rtu", "tcp"
        # unit: 10,
        # address: "/dev/tty.wchusbserial1420", "192.168.178.80"
        # mode: "slave", "master"
        # baudrate: 9600, optional, only required on type RTU
        required_keys = ["type", "unit", "address", "mode"]

        all_regs = self.register_definitions

        if self.register_definitions:
            if all_regs.get(config_keyword, ''):
                connection_config = all_regs[config_keyword]

                if all(k.lower() in connection_config for k in required_keys):
                    connection_type = connection_config['type'].lower()
                    if connection_type == 'rtu':
                        if 'baudrate' not in all_regs[config_keyword]:
                            # baudrate is required for RTU connections
                            raise ModbusBridgeError('Missing "baudrate" key in connection config')
                    elif connection_type == 'tcp':
                        pass
                    else:
                        raise ModbusBridgeError('Unknown connection type: {}'.
                                                format(connection_type))

                    connection_unit = connection_config['unit']
                    if not isinstance(connection_unit, int):
                        raise ModbusBridgeError('Unknown connection unit: {}'.
                                                format(connection_unit))

                    connection_mode = connection_config['mode'].lower()
                    if connection_mode == 'slave':
                        self.connection_settings_client = connection_config
                        self.client_unit = connection_unit
                        self.logger.debug('Client connection settings: {}'.
                                          format(connection_config))
                    elif connection_mode == 'master':
                        self.connection_settings_host = connection_config
                        self.host_unit = connection_unit
                        self.logger.debug('Host connection settings: {}'.
                                          format(connection_config))
                    else:
                        raise ModbusBridgeError('Unknown connection mode: {}'.
                                                format(connection_mode))
                else:
                    missing_keys = set(connection_config.keys()) - set(required_keys)
                    self.logger.warning('Missing connection keys: {}'.
                                        format(missing_keys))
            else:
                self.logger.warning('Key "{}" not found in modbus config'.
                                    format(config_keyword))
        else:
            self.logger.warning('No register definitions loaded so far')

    def _get_network_ip(self) -> str:
        """
        Get the IP address of either Station or Accesspint.

        :returns:   The network IP.
        :rtype:     str
        """
        result = False
        local_ip = '0.0.0.0'

        # check for network connection, either as Client or AccessPoint
        station = network.WLAN(network.STA_IF)
        accesspoint = network.WLAN(network.AP_IF)

        if station.active():
            if station.isconnected():
                local_ip = station.ifconfig()[0]
                result = True
            else:
                self.logger.debug('Station is active but not connected')

        if accesspoint.active() and result is False:
            local_ip = accesspoint.ifconfig()[0]
            result = True

        if result is False:
            self.logger.warning('No valid local IP found, using default')

        return local_ip

    def setup_connection(self, pins: Tuple[int, int] = (1, 3)) -> None:
        """
        Setup Modbus connections between host and client.

        :param      pins:   Machine pins to RTU connection
        :type       pins:   Tuple[int, int]
        """
        _client = None
        _host = None

        _client_cfg = self.connection_settings_client
        _host_cfg = self.connection_settings_host

        if _client_cfg.get('type', '').lower() == 'rtu':
            # act as host, get Modbus data via RTU from a client device
            # bus_address = _host_cfg.get('unit', None)
            data_bits = _client_cfg.get('data_bits', 8)
            stop_bits = _client_cfg.get('stop_bits', 1)
            parity = _client_cfg.get('parity', None)
            baudrate = _client_cfg.get('baudrate', 9600)
            _host = ModbusRTUMaster(
                baudrate=baudrate,
                data_bits=data_bits,
                stop_bits=stop_bits,
                parity=parity,
                pins=pins,
                # ctrl_pin=MODBUS_PIN_TX_EN
            )
            self.logger.debug('Created RTU host to collect from {} at {} baud'.
                              format(pins, baudrate))
        elif _client_cfg.get('type', '').lower() == 'tcp':
            # act as host, get Modbus data via TCP from a client device
            # do not use 'get()' here, as there exists no valid fallback value
            slave_ip = _client_cfg['address']
            port = int(_client_cfg['unit'])
            _host = ModbusTCPMaster(
                slave_ip=slave_ip,
                slave_port=port
            )
            self.logger.debug('Created TCP host to collect from {}:{}'.
                              format(slave_ip, port))

        if _host_cfg.get('type', '').lower() == 'rtu':
            # act as client, provide Modbus data via RTU to a host device
            bus_address = _host_cfg.get('unit', None)
            data_bits = _host_cfg.get('data_bits', 8)
            stop_bits = _host_cfg.get('stop_bits', 1)
            parity = _host_cfg.get('parity', None)
            baudrate = _host_cfg.get('baudrate', 9600)
            _client = ModbusRTU(
                addr=bus_address,
                baudrate=baudrate,
                data_bits=data_bits,
                stop_bits=stop_bits,
                parity=parity,
                pins=pins,
                # ctrl_pin=MODBUS_PIN_TX_EN
            )
            self.logger.debug('Created RTU client to serve on {} at {} baud'.
                              format(bus_address, baudrate))
        elif _host_cfg.get('type', '').lower() == 'tcp':
            # act as client, provide Modbus data via TCP to a host device
            _client = ModbusTCP()

            is_bound = False
            local_ip = self._get_network_ip()

            try:
                is_bound = _client.get_bound_status()
            except Exception as e:
                raise ModbusBridgeError('No "get_bound_status" function: {}'.
                                        format(e))

            if is_bound is False:
                self.logger.debug('TCP client not yet bound to IP and port')

                # local_ip = _net.ifconfig()[0]
                self.logger.debug('Local IP of device: {}'.format(local_ip))

                self.logger.debug('Connection settings: {}'.
                                  format(_host_cfg))
                port = int(_host_cfg['unit'])

                self.logger.debug('Binding device to IP "{}" on port "{}"'.
                                  format(local_ip, port))
                _client.bind(local_ip=local_ip, local_port=port)
                self.logger.debug('Modbus TCP client binding done')

            self.logger.debug('Created TCP client to serve on {}:{}'.
                              format(local_ip, port))

            _client.setup_registers(registers=self.register_definitions,
                                    use_default_vals=True)

        self.host = _host
        self.client = _client

        self.logger.debug('Client started as {mode} on address {address}'.
                          format(mode=_client_cfg['type'],
                                 address=_client_cfg['unit']))
        self.logger.debug('Host started as {mode} on address {address}:{port}'.
                          format(mode=_host_cfg['type'],
                                 address=local_ip,
                                 port=_host_cfg['unit']))

    def read_all_registers(self) -> dict:
        """
        Read all modbus registers (from client).

        :returns:   Dictionary with read register data
        :rtype:     dict
        """
        read_content = dict()
        modbus_registers = self.register_definitions

        # Coils (setter+getter) [0, 1]
        self.logger.debug('Coils:')
        if 'COILS' in modbus_registers:
            coil_register_content = self.read_coil_registers()
            self.logger.debug('coil_register_content: {}'.
                              format(coil_register_content))

            read_content.update(coil_register_content)
        else:
            self.logger.debug('No COILS defined, skipping')

        # Hregs (setter+getter) [0, 65535]
        self.logger.debug('Hregs:')
        if 'HREGS' in modbus_registers:
            hreg_register_content = self.read_hregs_registers()
            self.logger.debug('hreg_register_content: {}'.
                              format(hreg_register_content))
            read_content.update(hreg_register_content)
        else:
            self.logger.debug('No HREGS defined, skipping')

        # Ists (only getter) [0, 1]
        self.logger.debug('Ists:')
        if 'ISTS' in modbus_registers:
            input_status_content = self.read_ists_registers()
            self.logger.debug('input_status_content: {}'.
                              format(input_status_content))
            read_content.update(input_status_content)
        else:
            self.logger.debug('No ISTS defined, skipping')

        # Iregs (only getter) [0, 65535]
        self.logger.debug('Iregs:')
        if 'IREGS' in modbus_registers:
            ireg_register_content = self.read_iregs_registers()
            self.logger.debug('ireg_register_content: {}'.
                              format(ireg_register_content))
            read_content.update(ireg_register_content)
        else:
            self.logger.debug('No IREGS defined, skipping')

        self.logger.debug('Complete read content: {}'.format(read_content))

    def write_all_registers(self, modbus_registers: dict) -> None:
        """
        Write all modbus registers (of/to client).

        :param      modbus_registers:  The modbus registers
        :type       modbus_registers:  dict
        """
        # Coils (setter+getter) [0, 1]
        self.logger.debug('Coils:')
        if 'COILS' in modbus_registers:
            self.write_coil_registers(
                modbus_registers=modbus_registers['COILS']
            )
        else:
            self.logger.debug('No COILS defined, skipping')

        # Hregs (setter+getter) [0, 65535]
        self.logger.debug('Hregs:')
        if 'HREGS' in modbus_registers:
            self.write_hregs_registers(
                modbus_registers=modbus_registers['HREGS']
            )
        else:
            self.logger.debug('No HREGS defined, skipping')

        # Ists (only getter) [0, 1]
        if 'ISTS' in modbus_registers:
            self.logger.debug('ISTS can only be read, skipping')

        # Iregs (only getter) [0, 65535]
        if 'IREGS' in modbus_registers:
            self.logger.debug('IREGS can only be read, skipping')

    def read_coil_registers(self) -> dict:
        """
        Read all coil registers.

        Coils (setter+getter) [0, 1], function 01 - read single register

        :returns:   Read register content as dict
        :rtype:     dict
        """
        register_content = dict()
        modbus_registers = self.register_definitions['COILS']
        slave_addr = self.client_unit

        for key, val in modbus_registers.items():
            self.logger.debug('\tkey: {}'.format(key))
            self.logger.debug('\t\tval: {}'.format(val))

            register_address = val['register']
            count = val['len']

            coil_status = self.host.read_coils(
                slave_addr=slave_addr,
                starting_addr=register_address,
                coil_qty=count)

            if len(coil_status) == 1:
                # only a single value
                register_content[key] = {
                    'register': register_address,
                    'val': coil_status[0]
                }
            else:
                # convert the tuple to list to be JSON conform
                register_content[key] = {
                    'register': register_address,
                    'val': list(coil_status)
                }

            self.logger.debug('\t{}\t{}'.format(register_address,
                                                coil_status))

        return register_content

    def write_coil_registers(self, modbus_registers: dict) -> None:
        """
        Write all coil registers.

        Coils (setter+getter) [0, 1], function 05 - write single register

        :param      modbus_registers:   The modbus registers
        :type       modbus_registers:   dict
        """
        slave_addr = self.client_unit

        for key, val in modbus_registers.items():
            self.logger.debug('\tkey: {}'.format(key))
            self.logger.debug('\t\tval: {}'.format(val))

            register_address = val['register']
            register_value = val['val']

            # @see lib/uModbus/functions.write_single_coil
            if register_value is True:
                register_value = 0xFF00
            else:
                register_value = 0x0000

            operation_status = self.host.write_single_coil(
                slave_addr=slave_addr,
                output_address=register_address,
                output_value=register_value)

            self.logger.debug('Result of setting COIL {} to {}: {}'.
                              format(register_address,
                                     register_value,
                                     operation_status))

    def read_hregs_registers(self) -> dict:
        """
        Read all holding registers.

        Hregs (setter+getter) [0, 65535], function 03 - read holding register

        :returns:   Read register content as dict
        :rtype:     dict
        """
        register_content = dict()
        modbus_registers = self.register_definitions['HREGS']
        slave_addr = self.client_unit
        signed = False

        for key, val in modbus_registers.items():
            self.logger.debug('\tkey: {}'.format(key))
            self.logger.debug('\t\tval: {}'.format(val))

            register_address = val['register']
            count = val['len']

            register_value = self.host.read_holding_registers(
                slave_addr=slave_addr,
                starting_addr=register_address,
                register_qty=count,
                signed=signed)

            if len(register_value) == 1:
                # only a single value
                register_content[key] = {
                    'register': register_address,
                    'val': register_value[0]
                }
            else:
                # convert the tuple to list to be JSON conform
                register_content[key] = {
                    'register': register_address,
                    'val': list(register_value)
                }

            self.logger.debug('\t{}\t{}'.format(register_address,
                                                register_value))

        return register_content

    def write_hregs_registers(self, modbus_registers: dict) -> None:
        """
        Write all holding registers.

        Hregs (setter+getter) [0, 65535], function 06 - write holding register

        :param      modbus_registers:   The modbus registers
        :type       modbus_registers:   dict
        """
        slave_addr = self.client_unit
        signed = False

        for key, val in modbus_registers.items():
            self.logger.debug('\tkey: {}'.format(key))
            self.logger.debug('\t\tval: {}'.format(val))

            register_address = val['register']
            register_value = val['val']

            operation_status = self.host.write_single_register(
                slave_addr=slave_addr,
                output_address=register_address,
                output_value=register_value,
                signed=signed)

            self.logger.debug('Result of setting HREGS {} to {}: {}'.
                              format(register_address,
                                     register_value,
                                     operation_status))

    def read_ists_registers(self) -> dict:
        """
        Read all discrete input registers.

        Ists (only getter) [0, 1], function 02 - read input status (discrete
        inputs/digital input)

        :returns:   Read register content as dict
        :rtype:     dict
        """
        register_content = dict()
        modbus_registers = self.register_definitions['ISTS']
        slave_addr = self.client_unit

        for key, val in modbus_registers.items():
            self.logger.debug('\tkey: {}'.format(key))
            self.logger.debug('\t\tval: {}'.format(val))

            register_address = val['register']
            count = val['len']

            input_status = self.host.read_discrete_inputs(
                slave_addr=slave_addr,
                starting_addr=register_address,
                input_qty=count)

            if len(input_status) == 1:
                # only a single value
                register_content[key] = {
                    'register': register_address,
                    'val': input_status[0]
                }
            else:
                # convert the tuple to list to be JSON conform
                register_content[key] = {
                    'register': register_address,
                    'val': list(input_status)
                }

            self.logger.debug('\t{}\t{}'.format(register_address,
                                                input_status))

        return register_content

    def read_iregs_registers(self) -> dict:
        """
        Read all input registers.

        Iregs (only getter) [0, 65535], function 04 - read input registers

        :returns:   Read register content as dict
        :rtype:     dict
        """
        register_content = dict()
        modbus_registers = self.register_definitions['IREGS']
        slave_addr = self.client_unit
        signed = False

        for key, val in modbus_registers.items():
            self.logger.debug('\tkey: {}'.format(key))
            self.logger.debug('\t\tval: {}'.format(val))

            register_address = val['register']
            count = val['len']

            register_value = self.host.read_input_registers(
                slave_addr=slave_addr,
                starting_addr=register_address,
                register_qty=count,
                signed=signed)

            if len(register_value) == 1:
                # only a single value
                register_content[key] = {
                    'register': register_address,
                    'val': register_value[0]
                }
            else:
                # convert the tuple to list to be JSON conform
                register_content[key] = {
                    'register': register_address,
                    'val': list(register_value)
                }

            self.logger.debug('\t{}\t{}'.format(register_address,
                                                register_value))

        return register_content
