#!/usr/bin/env python3

import json
import time
import sys

with open("key_code_dict.json", "r") as file:
    key_codes = json.load(file)

NULL_CHAR = chr(0)
CTRL_KEY = chr(1)


def write_report(report):
    with open("/dev/hidg0", "rb+") as fd:
        fd.write(report.encode())
