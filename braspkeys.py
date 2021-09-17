"""
Sends keys to computer through raspberry pi. If file is given, reads from file and sends to computer.
"""
import json
import argparse

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


def parse_events(line: str) -> list:
    # TODO parse for special chars
    if "$" in line:
        # TODO
        ...
    events_list = list(line)
    new_events_list = []
    for event in events_list:
        if event.isalpha() and event.isupper():
            new_events_list.append((codes["shift"], codes[event.lower()], event))
        elif event in shift_key_codes:
            new_events_list.append(
                (codes["shift"], codes[shift_key_codes[event]], event)
            )
        else:
            new_events_list.append((0, codes[event], event))
    # each element (mod, scan, printable)
    return new_events_list


def write_event(mod_code: int, scan_code: int):
    data_event = (chr(mod_code) + chr(0) + chr(scan_code) + (chr(0) * 5)).encode()
    if code_print:
        print(data_event)
    if not dry_run:
        with open("/dev/hidg0", "rb+") as output_file:
            output_file.write(data_event)
            output_file.flush()


def keyboard_input_loop():
    print("keyboard input")
    while True:
        line = input() + "\n"
        process_line(line)


def read_input(file_name):
    print("reading from file")
    with open(file_name, "r") as input_file:
        lines = input_file.readlines()
        [process_line(line) for line in lines]


def main(input_file):
    input_file = args.input_file
    if input_file is None:
        keyboard_input_loop()
    else:
        read_input(input_file)


if __name__ == "__main__":
    try:
        main(input_file)
    except KeyboardInterrupt as e:
        print()
