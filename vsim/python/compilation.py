#!python3.7

#
# Author : Dimitrios Stathis
# Copyright 2022
# 
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# Use the python to parse the configuration json, and then call the appropriate
# bash or powershell script to execute

import json
import sys
import argparse


def read_arg():
    parser = argparse.ArgumentParser(description='Python script to parse a configuration file and compile/simulate RTL using vsim')
    parser.add_argument('json_file', help='Path to the configuration file.')

    args = parser.parse_args()
    return(args)

class files():
    def __init__(self, src_path, lib, lang, order):
      self.src_path = src_path
      self.lib = lib
      self.lang = lang
      self.order = order
      self.n_files = len(order)

class configuration:
    def __init__(self, text):
        self.file_path = text
        with open(self.file_path, 'r') as self.config_file:
            self.config_data = json.load(self.config_file)
        if 'compilation_path' in self.config_data:
            self.source_dir = self.config_data.get('compilation_path')
        else:
            print("No \'compilation_path\' has been specified in the configuration file")
            exit()

        if 'FILES' in self.config_data:
            self.files_length = len(self.config_data['FILES'])
            for f in self.config_data['FILES']:
              print(f)
              fi = files(f.get('PARENT_PATH'),f.get('LIBRARY'),f.get('LANGUAGE'),f.get('ORDER'))
        else:
            print("No \'FILES\' has been specified in the configuration file")
            exit()

    def print_me(self):
        print(self.config_data)


if __name__ == '__main__':
    args = read_arg()
    print(args)
    t1 = configuration(args.json_file)
    t1.print_me()
    print(t1.source_dir)
