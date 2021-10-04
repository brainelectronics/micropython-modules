#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
try to sync and set the internal clock (RTC) with NTP server time
"""

import machine
import ntptime
import time


# There's currently no timezone support in MicroPython
# RTC is set in UTC time
def set_time() -> None:
    """
    Set RTC time to time received from NTP server.

    No network check is performed
    """
    tm = time.localtime()
    print("Local time before synchronization: {}".format(tm))
    # Local time before synchronization: (2000, 1, 1, 0, 9, 44, 5, 1)

    # sync time with NTP server
    try:
        ntptime.settime()
        print('Synced with NTP server')
    except Exception as e:
        print('Failed to sync with NTP server due to {}'.format(e))

    tm = time.localtime()
    print("Local time after synchronization: {}".format(tm))
    # Local time after synchronization: (2021, 7, 15, 15, 12, 25, 1, 196)

    rtc = machine.RTC()
    # year, month, day, hour, minute, second, microsecond, tzinfo
    rtc.init((tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], 0))
