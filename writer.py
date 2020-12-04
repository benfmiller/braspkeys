#!/usr/bin/env python3

import time

NULL_CHAR = chr(0)
CTRL_KEY = chr(1)


def write_report(report):
    with open("/dev/hidg0", "rb+") as fd:
        fd.write(report.encode())