#!/usr/bin/env python3
"""
Sends keys to computer through raspberry pi. If file given, reads from file and sends to computer.
"""
import argparse
import os
import time

# Parsing Args
# -------------------------------------------------------------------
ap = argparse.ArgumentParser()
ap.add_argument(
    "-v",
    "--verbose",
    help="if given, prints to console as well as to output device",
    action="store_true",
)
ap.add_argument(
    "-d",
    "--dry-run",
    help="if given, only prints to console and doesn't output to computer",
    action="store_true",
)
ap.add_argument(
    "-c",
    "--code-print",
    help="if given, prints byte string that is written to computer",
    action="store_true",
)
ap.add_argument(
    "input_file",
    nargs="?",
    help="path to the input file",
    type=str,
)
ap.add_argument(
    "-w",
    "--wait-time",
    help="time in between keypresses in milliseconds",
    type=int,
    default=0,
)
args = ap.parse_args()
input_file: str = args.input_file
verbose: bool = args.verbose
dry_run: bool = args.dry_run
code_print: bool = args.code_print
wait_time: int = args.wait_time

# reading codes
# -------------------------------------------------------------------

shift_key_codes = {
    "~": "`",
    "!": "1",
    "@": "2",
    "#": "3",
    "$": "4",
    "%": "5",
    "^": "6",
    "&": "7",
    "*": "8",
    "(": "9",
    ")": "0",
    "_": "-",
    "+": "=",
    "{": "[",
    "}": "]",
    "|": "\\",
    ":": ";",
    '"': "'",
    "<": ",",
    ">": ".",
    "?": "/",
}

modifier_codes = {
    "ctrl": 0x01,
    "shift": 0x02,
    "alt": 0x04,
    "MOD_LMETA": 0x08,
    "MOD_RCTRL": 0x10,
    "MOD_RSHIFT": 0x20,
    "MOD_RALT": 0x40,
    "MOD_RMETA": 0x80,
}

codes = {
    "NONE": "0x00",
    "ERR_OVF": "0x01",
    "a": "0x04",
    "b": "0x05",
    "c": "0x06",
    "d": "0x07",
    "e": "0x08",
    "f": "0x09",
    "g": "0x0a",
    "h": "0x0b",
    "i": "0x0c",
    "j": "0x0d",
    "k": "0x0e",
    "l": "0x0f",
    "m": "0x10",
    "n": "0x11",
    "o": "0x12",
    "p": "0x13",
    "q": "0x14",
    "r": "0x15",
    "s": "0x16",
    "t": "0x17",
    "u": "0x18",
    "v": "0x19",
    "w": "0x1a",
    "x": "0x1b",
    "y": "0x1c",
    "z": "0x1d",
    "1": "0x1e",
    "2": "0x1f",
    "3": "0x20",
    "4": "0x21",
    "5": "0x22",
    "6": "0x23",
    "7": "0x24",
    "8": "0x25",
    "9": "0x26",
    "0": "0x27",
    "\n": "0x28",
    "KEY_ESC": "0x29",
    "\b": "0x2a",
    "\t": "0x2b",
    " ": "0x2c",
    "-": "0x2d",
    "=": "0x2e",
    "[": "0x2f",
    "]": "0x30",
    "\\": "0x31",
    "~": "0x32",
    ";": "0x33",
    "'": "0x34",
    "GRAVE": "0x35",
    ",": "0x36",
    ".": "0x37",
    "SLASH": "0x38",
    "CAPSLOCK": "0x39",
    "F1": "0x3a",
    "F2": "0x3b",
    "F3": "0x3c",
    "F4": "0x3d",
    "F5": "0x3e",
    "F6": "0x3f",
    "F7": "0x40",
    "F8": "0x41",
    "F9": "0x42",
    "F10": "0x43",
    "F11": "0x44",
    "F12": "0x45",
    "SYSRQ": "0x46",
    "SCROLLLOCK": "0x47",
    "PAUSE": "0x48",
    "INSERT": "0x49",
    "HOME": "0x4a",
    "PAGEUP": "0x4b",
    "DELETE": "0x4c",
    "END": "0x4d",
    "PAGEDOWN": "0x4e",
    "RIGHT": "0x4f",
    "LEFT": "0x50",
    "DOWN": "0x51",
    "UP": "0x52",
    "NUMLOCK": "0x53",
    "KPSLASH": "0x54",
    "KPASTERISK": "0x55",
    "KPMINUS": "0x56",
    "KPPLUS": "0x57",
    "KPENTER": "0x58",
    "KP1": "0x59",
    "KP2": "0x5a",
    "KP3": "0x5b",
    "KP4": "0x5c",
    "KP5": "0x5d",
    "KP6": "0x5e",
    "KP7": "0x5f",
    "KP8": "0x60",
    "KP9": "0x61",
    "KP0": "0x62",
    "KPDOT": "0x63",
    "102ND": "0x64",
    "COMPOSE": "0x65",
    "POWER": "0x66",
    "KPEQUAL": "0x67",
    "F13": "0x68",
    "F14": "0x69",
    "F15": "0x6a",
    "F16": "0x6b",
    "F17": "0x6c",
    "F18": "0x6d",
    "F19": "0x6e",
    "F20": "0x6f",
    "F21": "0x70",
    "F22": "0x71",
    "F23": "0x72",
    "F24": "0x73",
    "OPEN": "0x74",
    "HELP": "0x75",
    "PROPS": "0x76",
    "FRONT": "0x77",
    "STOP": "0x78",
    "AGAIN": "0x79",
    "UNDO": "0x7a",
    "CUT": "0x7b",
    "COPY": "0x7c",
    "PASTE": "0x7d",
    "FIND": "0x7e",
    "MUTE": "0x7f",
    "VOLUMEUP": "0x80",
    "VOLUMEDOWN": "0x81",
    "KPCOMMA": "0x85",
    "RO": "0x87",
    "KATAKANAHIRAGANA": "0x88",
    "YEN": "0x89",
    "HENKAN": "0x8a",
    "MUHENKAN": "0x8b",
    "KPJPCOMMA": "0x8c",
    "HANGEUL": "0x90",
    "HANJA": "0x91",
    "KATAKANA": "0x92",
    "HIRAGANA": "0x93",
    "ZENKAKUHANKAKU": "0x94",
    "KPLEFTPAREN": "0xb6",
    "KPRIGHTPAREN": "0xb7",
    "LEFTCTRL": "0xe0",
    "LEFTSHIFT": "0xe1",
    "LEFTALT": "0xe2",
    "LEFTWINDOWS": "0xe3",
    "RIGHTCTRL": "0xe4",
    "RIGHTSHIFT": "0xe5",
    "RIGHTALT": "0xe6",
    "RIGHTMETA": "0xe7",
    "MEDIA_PLAYPAUSE": "0xe8",
    "MEDIA_STOPCD": "0xe9",
    "MEDIA_PREVIOUSSONG": "0xea",
    "MEDIA_NEXTSONG": "0xeb",
    "MEDIA_EJECTCD": "0xec",
    "MEDIA_VOLUMEUP": "0xed",
    "MEDIA_VOLUMEDOWN": "0xee",
    "MEDIA_MUTE": "0xef",
    "MEDIA_WWW": "0xf0",
    "MEDIA_BACK": "0xf1",
    "MEDIA_FORWARD": "0xf2",
    "MEDIA_STOP": "0xf3",
    "MEDIA_FIND": "0xf4",
    "MEDIA_SCROLLUP": "0xf5",
    "MEDIA_SCROLLDOWN": "0xf6",
    "MEDIA_EDIT": "0xf7",
    "MEDIA_SLEEP": "0xf8",
    "MEDIA_COFFEE": "0xf9",
    "MEDIA_REFRESH": "0xfa",
    "MEDIA_CALC": "0xfb",
}

for name, value in codes.items():
    codes[name] = int(value, 16)

# -------------------------------------------------------------------


def process_line(line: str):
    """
    Takes an unparsed line and writes the events
    """
    events_list = parse_events(line)
    for event in events_list:
        write_chord(event, 0, 0)
        write_event(0, 0)


def write_chord(to_write: list, mod, scan):
    """Shifts already processed at this point"""
    if verbose or dry_run:
        print(to_write[0], end="")
    if to_write[0] in modifier_codes:
        mod += modifier_codes[to_write[0]]
    else:
        scan += codes[to_write[0]]

    if len(to_write) == 1:
        write_event(mod, scan)
    else:
        write_event(mod, scan)
        write_chord(to_write[1:], mod, scan)
        write_event(mod, scan)


def process_special_event(events_list: str) -> tuple:
    """Gets word list from parse events and turns into list"""
    in_key_dicts = [
        x in shift_key_codes or x in modifier_codes or x in codes for x in events_list
    ]
    final_keys = []
    if False not in in_key_dicts:
        for word in events_list:
            if word in shift_key_codes:
                final_keys += ["shift", shift_key_codes[word]]
            else:
                final_keys += [word]
    else:
        final_keys = ["$", "<"]
        final_keys += list(" ".join(events_list))
        final_keys += [">"]
    return final_keys


def calc_chord_list(line: str) -> list:
    """Parses line for possible chords and calcs them"""
    chord_list = []
    if "$<" in line and ">" in line and line.index(">") > line.index("$<"):
        dollar_indexes = [i for i, ltr in enumerate(line) if ltr == "$"]
        end_angle_indexes = [i for i, ltr in enumerate(line) if ltr == ">"]
        for index in dollar_indexes:
            if index - 1 >= 0 and line[index - 1] == "\\":
                continue
            if index + 1 < len(line) and line[index + 1] == "<":
                for end_index in end_angle_indexes:
                    if end_index > index and "$<" not in line[index + 2 : end_index]:
                        temp_words = line[index + 2 : end_index].split()
                        completed_codes = process_special_event(temp_words)
                        chord_list += [[completed_codes, index, end_index]]
                        break
    return chord_list


def parse_events(line: str) -> list:
    """Takes a line and parses the events """
    chord_list = calc_chord_list(line)
    events_list = list(line)
    offset = 0
    for chord in chord_list:
        if chord[0][0] == "$":
            continue
        chord[1] -= offset
        chord[2] -= offset
        events_list = events_list[: chord[1]] + events_list[chord[2] + 1 :]
        events_list.insert(chord[1], chord[0])
        offset += chord[2] - chord[1]

    new_events_list = []
    for event in events_list:
        if isinstance(event, str):
            if event.isalpha() and event.isupper():
                new_events_list.append(("shift", event.lower()))
            elif event in shift_key_codes:
                new_events_list.append(("shift", shift_key_codes[event]))
            else:
                new_events_list.append((event))
        else:
            new_events_list.append((event))
    # each element tup of letters to enter
    return new_events_list


def write_event(mod_code: int, scan_code: int):
    """Does the actual event writing"""
    data_event = (chr(mod_code) + chr(0) + chr(scan_code) + (chr(0) * 5)).encode()
    time.sleep(wait_time / 1000)
    if code_print:
        print("\t\t", end="")
        print(data_event)
    if not dry_run:
        with open("/dev/hidg0", "rb+") as output_file:
            output_file.write(data_event)
            output_file.flush()


def keyboard_input_loop():
    """loops input if no file name input was given"""
    print("keyboard input")
    print("--------------")
    while True:
        line = input() + "\n"
        process_line(line)


def read_input(file_name):
    """Reads input from file"""
    print("reading from file")
    print("-----------------")
    with open(file_name, "r") as file:
        lines = file.readlines()
        [process_line(line) for line in lines]


def main():
    """Calls read input if file given or keyboard_input_loop if no file name"""
    if input_file is None:
        keyboard_input_loop()
    else:
        read_input(input_file)


if __name__ == "__main__":
    if not dry_run and os.geteuid() != 0:
        raise SystemError(
            "You need to have root privileges to run this script.\n\
            Please try again, this time using 'sudo'. Exiting."
        )
    try:
        main()
    except KeyboardInterrupt as e:
        print()
