"""
Sends keys to computer through raspberry pi. If file is given, reads from file and sends to computer.
"""
import json
import argparse

ap = argparse.ArgumentParser()
ap.add_argument(
    "input_file",
    nargs="?",
    help="path to the input file",
    type=str,
)
args = ap.parse_args()
input_file: str = args.input_file

with open("key_code_dict.json", "r") as infile:
    codes: dict = json.load(infile)


def process_line(line: str):
    print(line)
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
        line = input()
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
    main(input_file)
