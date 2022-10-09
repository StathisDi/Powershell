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

# Configuration class that is used in the compilation.py

import json
from simulation_class import simulation
from list_files_class import list_files
from files_class import files


class configuration:
    def __init__(self, config_path):
        # Get the configuration path and open the file
        self.file_path = config_path
        with open(self.file_path, "r") as config_file:
            self.config_data = json.load(config_file)
            config_file.close

        # Parse the compilation/project path
        if "compilation_path" in self.config_data:
            self.prj_dir = self.config_data.get("compilation_path")
        else:
            print("No 'compilation_path' has been defined in the configuration file")
            exit()

        # Parse the compilation/project path
        if "path_pwsh" in self.config_data:
            self.path_pwsh = self.config_data.get("path_pwsh")
        else:
            print("No 'path_pwsh' has been defined in the configuration file")
            exit()

        # Parse the compilation/project path
        if "path_bash" in self.config_data:
            self.path_bash = self.config_data.get("path_bash")
        else:
            print("No 'path_bash' has been defined in the configuration file")
            exit()
        # Create list of libraries
        self.libs = []

        # Parse the file section (get instruction for RTL files and libraries)
        self.files_length = 0
        if "FILES" in self.config_data:
            self.files_length = len(self.config_data["FILES"])
            self.fi = []
            for f in self.config_data["FILES"]:
                self.fi.append(
                    files(
                        f.get("PARENT_PATH"),
                        f.get("LIBRARY"),
                        f.get("LANGUAGE"),
                        f.get("ORDER"),
                        f.get("check_for_synthesis"),
                        f.get("HIERARCHY"),
                        f.get("MIXED"),
                    )
                )
                self.add_lib(f.get("LIBRARY"))
        else:
            print("No 'FILES' has been defined in the configuration file")
            exit()

        # Parse the list_files section (get instruction for hierarchy files )
        self.files_list_length = 0
        if "LIST_FILES" in self.config_data:
            self.files_list_length = len(self.config_data["LIST_FILES"])
            self.fi_list = []
            for f in self.config_data["LIST_FILES"]:
                self.fi_list.append(
                    list_files(
                        f.get("PATH"),
                        f.get("LIBRARY"),
                        f.get("LANGUAGE"),
                        f.get("ORDER"),
                        f.get("check_for_synthesis"),
                        f.get("MIXED"),
                    )
                )
                self.add_lib(f.get("LIBRARY"))
        else:
            print("No 'LIST_FILES' has been defined in the configuration file")

        # Parse the Simulation section (get instructions for the simulation after the compilation)
        self.simulation = False
        if "SIMULATION" in self.config_data:
            sim = self.config_data.get("SIMULATION")
            self.simulation = True
            self.sim_conf = simulation(
                sim[0].get("opt"),
                sim[0].get("command_line"),
                sim[0].get("use_script"),
                sim[0].get("sim_script"),
                sim[0].get("top_entity"),
                sim[0].get("run_time"),
            )
        else:
            print("Json file does not include configuration for simulation")

    # Add libraries to the list
    def add_lib(self, lib):
        if lib not in self.libs:
            self.libs.append(lib)

    def print_me(self):
        print("Configuration:")
        print("Working path: ", self.prj_dir)
        print("\nCompilation of RTL files: ")
        for x in self.fi:
            print("   ", x)
        print("\n\nCompilation of List files:")
        for x in self.fi_list:
            print("   ", x)
        if self.simulation:
            print("\n\nSimulation:")
            print("   ", self.sim_conf)
