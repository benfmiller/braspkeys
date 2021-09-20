"""
Sends keys to computer through raspberry pi. If file given, reads from file and sends to computer.
"""
import argparse
import json
import re

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
    "input_file", nargs="?", help="path to the input file", type=str,
)
# TODO add wait time between keys
args = ap.parse_args()
input_file: str = args.input_file
verbose: bool = args.verbose
dry_run: bool = args.dry_run
code_print: bool = args.code_print

# reading codes
# -------------------------------------------------------------------

with open("key_code_dict.json", "r") as infile:
    codes: dict = json.load(infile)

for name, value in codes.items():
    codes[name] = int(value, 16)

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
    "ctrl": "0x01",
    "shift": "0x02",
    "alt": "0x04",
    "MOD_LMETA": "0x08",
    "MOD_RCTRL": "0x10",
    "MOD_RSHIFT": "0x20",
    "MOD_RALT": "0x40",
    "MOD_RMETA": "0x80",
}

# -------------------------------------------------------------------


def process_line(line: str):
    """
    Takes an unparsed line and writes the events
    """
    # TODO
    events_list = parse_events(line)
    for event in events_list:
        if verbose or dry_run:
            print(event[2], end="")
        if event[1] != 0:
            write_event(0, event[1])
        else:
            write_event(event[0], 0)
            write_event(event[0], event[1])
            write_event(event[0], 0)
        write_event(0, 0)
    # codes[event.lower()]
    # (codes["shift"], codes[shift_key_codes[event]], event)


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
    if re.search("$<*>", line):
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
                        chord_list += [completed_codes, index, end_index]
                        break
    return chord_list


def parse_events(line: str) -> list:
    """Takes a line and parses the events """
    # TODO parse for special chars

    chord_list = calc_chord_list(line)
    events_list = list(line)
    offset = 0
    for chord in chord_list:
        chord[1] -= offset
        chord[2] -= offset
        events_list = events_list[: chord[1]] + events_list[chord[2] + 1 :]
        events_list.insert(chord[1], chord)
        offset += chord[2] - chord[1] - 1

    new_events_list = []
    for event in events_list:
        if event == str:
            if event.isalpha() and event.isupper():
                new_events_list.append(("shift", event))
            elif event in shift_key_codes:
                new_events_list.append(new_events_list.append(("shift", event)))
            else:
                new_events_list.append((event))
        else:
            new_events_list.append((chord))
    # each element tup of letters to enter
    return new_events_list


def write_event(mod_code: int, scan_code: int):
    """Does the actual event writing"""
    data_event = (chr(mod_code) + chr(0) + chr(scan_code) + (chr(0) * 5)).encode()
    if code_print:
        print(data_event)
    if not dry_run:
        with open("/dev/hidg0", "rb+") as output_file:
            output_file.write(data_event)
            output_file.flush()


def keyboard_input_loop():
    """loops input if no file name input was given"""
    print("keyboard input")
    while True:
        line = input() + "\n"
        process_line(line)


def read_input(file_name):
    """Reads input from file"""
    print("reading from file")
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
    try:
        main()
    except KeyboardInterrupt as e:
        print()
