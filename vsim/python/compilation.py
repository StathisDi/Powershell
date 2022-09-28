#!python3.7

# Use the python to parse the configuration json, and then call the appropriate
# bash or powershell script to execute

import json
import sys
import argparse


def read_arg():
    parser = argparse.ArgumentParser(description='Python script to parse a configuration file and compile/simulate RTL using vsim')
    parser.add_argument('json_file', help='Path to the configuration file.')
    parser.add_argument('-s', action='store_true', default='False', help='Run simulation after compilation')
    parser.add_argument('-c', action='store_true', default='False', help='Run simulation after compilation in command line only')

    args = parser.parse_args()
    return(args)


class configuration:
    def __init__(self, text):
        self.file_path = text
        with open(self.file_path, 'r') as self.config_file:
            self.config_data = json.load(self.config_file)

    def print_me(self):
        print(self.config_data)


if __name__ == '__main__':
    args = read_arg()
    print(args)
    t1 = configuration(args.json_file)
    t1.print_me()
    print(t1.config_data['GENERAL'][0]['compilation_path'])
