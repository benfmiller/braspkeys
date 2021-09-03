"""
Sends keys to computer through raspberry pi. If file is given, reads from file and sends to computer.
"""
import json
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("input_file", help="path to the input file")
args = ap.parse_args()

with open("key_code_dict.json", "r") as infile:
    codes = json.load(infile)


def print_pressed_keys():
    global codes
    print(codes)


def write_event(self, mod_code, scan_code):
    with open("/dev/hidg0", "rb+") as output_file:
        data_event = mod_code + chr(0) + scan_code + (chr(0) * 5)
        print("sup")
        print(data_event.encode())
        return

        # TODO
        self.output_file.write(data_event.encode())
        self.output_file.flush()


def keyboard_input_loop():
    ...


def read_input(file_name):
    with open(file_name, "r") as input_file:
        ...


def main():
    input_file = args.input_file
    if input_file is None:
        keyboard_input_loop()
    else:
        read_input()
    print_pressed_keys()


if __name__ == "__main__":
    main()
