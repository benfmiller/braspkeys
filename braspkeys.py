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
    "input_file", nargs="?", help="path to the input file", type=str,
)
args = ap.parse_args()
input_file: str = args.input_file
verbose: bool = args.verbose

with open("key_code_dict.json", "r") as infile:
    codes: dict = json.load(infile)


def process_line(line: str):
    # print(line)
    events_list = list(line)
    for event in events_list:
        if verbose:
            print(event, end="")
        # write_event()
    # TODO


def write_event(self, mod_code: int, scan_code: int):
    with open("/dev/hidg0", "rb+") as output_file:
        data_event = mod_code + chr(0) + scan_code + (chr(0) * 5)
        print("sup")
        print(data_event.encode())
        return

        # TODO
        self.output_file.write(data_event.encode())
        self.output_file.flush()


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
