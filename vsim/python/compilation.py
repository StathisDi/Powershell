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
    parser.add_argument('-s', action='store_true', help='Run simulation after compilation', default=False)

    args = parser.parse_args()
    return(args)


class files():
    def __init__(self, src_path, lib, lang, order, check_syn, hier, mixed):
        self.src_path = src_path
        self.lib = lib
        self.lang = lang
        self.order = order
        self.check_syn = check_syn
        self.hier = hier
        self.n_files = len(hier)
        self.mixed = mixed

    def __str__(self):
        return f'files({self.src_path}, {self.lib}, {self.lang}, {self.order}, {self.check_syn}, {self.hier}, {self.n_files}, {self.mixed})'


class list_files():
    def __init__(self, src_path, lib, lang, order, check_syn, mixed):
        self.src_path = src_path
        self.lib = lib
        self.lang = lang
        self.order = order
        self.check_syn = check_syn
        self.mixed = mixed

    def __str__(self):
        return f'list files({self.src_path}, {self.lib}, {self.lang}, {self.order},{self.check_syn}, {self.mixed})'


class simulation():
    def __init__(self, opt, command_line, use_script, sim_script=None, top_entity=None, run_time=None):
        self.opt = opt
        self.command_line = command_line
        self.use_script = use_script
        self.sim_script = sim_script
        self.top_entity = top_entity
        self.run_time = run_time
        if self.use_script == True:
            if self.sim_script == None:
                print("No path for simulation script!")
                exit()
            else:
                if self.run_time != None or self.top_entity != None:
                    print("!!!Warning!!! Run time and top entity should be defined inside the simulation script.\nValues defined in the configuration file will be ignored!")
        else:
            if self.top_entity == None:
                print("The top entity name is not defined!")
                exit()

    def __str__(self):
        return f'Simulation settings( optimizations = {self.opt}, command line = {self.command_line}, use script = {self.use_script}, sim script path = {self.sim_script}, top entity = {self.top_entity}, run time = {self.run_time})'


class configuration:
    def __init__(self, config_path):
        # Get the configuration path and open the file
        self.file_path = config_path
        with open(self.file_path, 'r') as self.config_file:
            self.config_data = json.load(self.config_file)

        # Parse the compilation/project path
        if 'compilation_path' in self.config_data:
            self.source_dir = self.config_data.get('compilation_path')
        else:
            print("No \'compilation_path\' has been defined in the configuration file")
            exit()

        # Parse the file section (get instruction for RTL files and libraries)
        self.files_length = 0
        if 'FILES' in self.config_data:
            self.files_length = len(self.config_data['FILES'])
            self.fi = []
            for f in self.config_data['FILES']:
                self.fi.append(files(f.get('PARENT_PATH'), f.get('LIBRARY'), f.get('LANGUAGE'), f.get('ORDER'), f.get('check_for_synthesis'), f.get('HIERARCHY'), f.get('MIXED')))
        else:
            print("No \'FILES\' has been defined in the configuration file")
            exit()

        # Parse the list_files section (get instruction for hierarchy files )
        self.files_list_length = 0
        if 'LIST_FILES' in self.config_data:
            self.files_list_length = len(self.config_data['LIST_FILES'])
            self.fi_list = []
            for f in self.config_data['LIST_FILES']:
                self.fi_list.append(list_files(f.get('PATH'), f.get('LIBRARY'), f.get('LANGUAGE'), f.get('ORDER'), f.get('check_for_synthesis'), f.get('MIXED')))
        else:
            print("No \'LIST_FILES\' has been defined in the configuration file")

        # Parse the Simulation section (get instructions for the simulation after the compilation)
        self.simulation = False
        if 'SIMULATION' in self.config_data:
            sim = self.config_data.get('SIMULATION')
            self.simulation = True
            self.sim_conf = simulation(sim[0].get('opt'), sim[0].get('command_line'), sim[0].get('use_script'), sim[0].get('sim_script'), sim[0].get('top_entity'), sim[0].get('run_time'))
        else:
            print('Json file does not include configuration for simulation')

    def print_me(self):
        print("Configuration:")
        print("Working path: ", self.source_dir)
        print("\nCompilation of RTL files: ")
        for x in self.fi:
            print("   ", x)
        print("\n\nCompilation of List files:")
        for x in self.fi_list:
            print("   ", x)
        if self.simulation:
            print("\n\nSimulation:")
            print("   ", self.sim_conf)


if __name__ == '__main__':
    args = read_arg()
    print(args.json_file)
    print(args.s)
    t1 = configuration(args.json_file)
    t1.print_me()
