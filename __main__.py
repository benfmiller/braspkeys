#!/usr/bin/env python3
import keyboard.keyboard as keyboard
import json
import time
import sys
import fileinput

# with open("key_code_dict.json", "r") as file:
#     key_codes = json.load(file)


# def write_report(report):
#     with open("/dev/hidg0", "rb+") as fd:
#         fd.write(report.encode())

for line in fileinput.input():
    # print(line, end="")
    keyboard.write(line)
