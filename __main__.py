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

# a = []
for line in fileinput.input():
    a += line
    if len(line) > 4:
        if line[0:3] == "#!$":
            time.sleep(int(line[3:]))
            continue
    if len(line) == 6:
        if line[0:5] == "!!$!!":
            break
    # if "\\n" in line or "\\t" in line:
    #     print("hey")
    #     line.replace(r"\n", "\n")  # chr(13))
    #     line.replace(r"\t", "\t")  # chr(9))
    # print(line, end="")
    # keyboard.write(line)
# print(a)
