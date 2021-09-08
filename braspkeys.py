"""
Sends keys to computer through raspberry pi. If file is given, reads from file and sends to computer.
"""
import json
import argparse

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

with open("key_code_dict.json", "r") as infile:
    codes: dict = json.load(infile)

for name, value in codes.items():
    codes[name] = int(value, 16)


def process_line(line: str):
    # TODO
    events_list = list(line)
    for event in events_list:
        if verbose or dry_run:
            print(event, end="")
        if not dry_run:
            if event.isalpha() and event.isupper():
                write_event(codes["shift"], 0)
                write_event(codes["shift"], codes[event.lower()])
                write_event(codes["shift"], 0)
            write_event(0, 0)


def write_event(mod_code: int, scan_code: int):
    data_event = (chr(mod_code) + chr(0) + chr(scan_code) + (chr(0) * 5)).encode()
    print(data_event)
    if not dry_run:
        with open("/dev/hidg0", "rb+") as output_file:
            pass
            # TODO
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
