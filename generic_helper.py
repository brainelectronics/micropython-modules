#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""General Helper functions for Micropython boards like BE32-01 and others"""

import gc
import json
import ulogging as logging
import os
import random

# not natively supported on micropython, see typing.py
from typing import Optional, Union


class GenericHelper(object):
    """docstring for GenericHelper"""
    def __init__(self):
        pass

    @staticmethod
    def create_logger(logger_name: Optional[str] = None):
        """
        Create a logger.

        :param      logger_name:  The logger name
        :type       logger_name:  str, optional

        :returns:   Configured logger
        :rtype:     logging.Logger
        """
        logging.basicConfig(level=logging.INFO)

        if logger_name:
            logger = logging.getLogger(logger_name)
        else:
            logger = logging.getLogger(__name__)

        return logger

    @staticmethod
    def set_level(logger: logging.Logger, level: str) -> None:
        """
        Set the level of a logger.

        :param      logger:  The logger to set the level
        :type       logger:  logging.Logger
        :param      level:   The new level
        :type       level:   str
        """
        if level.lower() == 'debug':
            logger.setLevel(level=logging.DEBUG)
        elif level.lower() == 'info':
            logger.setLevel(level=logging.DEBUG)
        elif level.lower() == 'warning':
            logger.setLevel(level=logging.WARNING)
        elif level.lower() == 'error':
            logger.setLevel(level=logging.ERROR)
        elif level.lower() == 'critical':
            logger.setLevel(level=logging.CRITICAL)
        else:
            pass

    @staticmethod
    def get_random_value(lower: int = 0, upper: int = 255) -> int:
        """
        Get a random value within the given range

        :param      lower:  The lower boundary
        :type       lower:  int, optional
        :param      upper:  The upper boundary, inclusive, default 255
        :type       upper:  int, optional

        :returns:   The random value.
        :rtype:     int
        """
        return random.randint(lower, upper)

    @staticmethod
    def df(path: str = '//', unit: Optional[str] = None) -> Union[int, str]:
        """
        Get free disk space

        :param      path:    The path to obtain informations
        :type       path:    str, optional
        :param      unit:    The unit of the returned size, None, 'kB' or 'MB'
        :type       unit:    str, optional

        :returns:   Available disk space in byte or as string in kB or MB
        :rtype:     int or str
        """
        info = os.statvfs(path)

        if unit is None:
            result = info[0] * info[3]
        elif unit.lower() == 'kb':
            result = ('{0:.3f} kB'.format((info[0] * info[3]) / 1024))
        elif unit.lower() == 'mb':
            result = ('{0:.3f} MB'.format((info[0] * info[3]) / 1048576))

        return result

    @staticmethod
    def get_free_memory() -> dict:
        """
        Get free memory (RAM)

        :param      update:  Flag to collect latest informations
        :type       update:  bool, optional

        :returns:   Informations about system RAM
        :rtype:     dict
        """
        gc.collect()
        free = gc.mem_free()
        allocated = gc.mem_alloc()
        total = free + allocated
        percentage = '{0:.2f}%'.format((free / total) * 100)

        memory_stats = {'free': free,
                        'total': total,
                        'percentage': percentage}

        return memory_stats

    @staticmethod
    def free(full: bool = False) -> Union[int, str]:
        """
        Get detailed informations about free RAM

        :param      full:    Flag to return report with total, free, percentage
        :type       full:    bool, optional

        :returns:   Informations, percentage by default
        :rtype:     int or str
        """
        memory_stats = GenericHelper.get_free_memory()

        if not full:
            return memory_stats['percentage']
        else:
            return ('Total: {0:.1f} kB, Free: {1:.2f} kB ({2})'.
                    format(memory_stats['total'] / 1023,
                           memory_stats['free'] / 1024,
                           memory_stats['percentage']))

    @staticmethod
    def str_to_dict(data: str) -> dict:
        """
        Convert string to dictionary

        :param      data:  The data
        :type       data:  str

        :returns:   Dictionary of string
        :rtype:     dict
        """
        return json.loads(data.replace("'", "\""))

    @staticmethod
    def save_json(data: dict, path: str, mode: str = 'w') -> None:
        """
        Save data as JSON file.

        :param      data:  The data
        :type       data:  dict
        :param      path:  The path to the JSON file
        :type       path:  str
        :param      mode:  The mode of file operation
        :type       mode:  str, optional
        """
        with open(path, mode) as file:
            json.dump(data, file)

    @staticmethod
    def load_json(path: str, mode: str = 'r') -> dict:
        """
        Load data from JSON file.

        :param      path:  The path to the JSON file
        :type       path:  str
        :param      mode:  The mode of file operation
        :type       mode:  str, optional

        :returns:   Loaded data
        :rtype:     dict
        """
        read_data = dict()
        with open(path, mode) as file:
            read_data = json.load(file)

        return read_data

    @staticmethod
    def save_file(data: str, path: str, mode: str = 'wb') -> None:
        """
        Save data to a file.

        :param      data:  The data
        :type       data:  str
        :param      path:  The path to the file
        :type       path:  str
        :param      mode:  The mode of file operation
        :type       mode:  str, optional
        """
        # save to file as binary by default
        with open(path, mode) as file:
            file.write(data)

    @staticmethod
    def load_file(path: str, mode: str = 'rb') -> str:
        """
        Load data from a file.

        :param      path:  The path to the file
        :type       path:  str
        :param      mode:  The mode of file operation
        :type       mode:  str, optional

        :returns:   Read file content
        :rtype:     str
        """
        # read file in binary by default
        read_data = ""
        with open(path, mode) as file:
            read_data = file.read()

        return read_data
