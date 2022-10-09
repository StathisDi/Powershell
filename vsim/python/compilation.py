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
import platform
import subprocess


def read_arg():
    parser = argparse.ArgumentParser(
        description="Python script to parse a configuration file and compile/simulate RTL using vsim"
    )
    parser.add_argument("json_file", help="Path to the configuration file.")
    parser.add_argument(
        "-s",
        action="store_true",
        help="Run simulation after compilation",
        default=False,
    )

    args = parser.parse_args()
    return args


class files:
    def __init__(self, src_path, lib, lang, order, check_syn, hier, mixed):
        self.src_path = src_path
        print(self.src_path)
        self.lib = lib
        self.lang = lang
        if (
            self.lang != "2008"
            and self.lang != "2002"
            and self.lang != "93"
            and self.lang != "87"
            and self.lang != "verilog"
            and self.lang != "vlog01compat"
            and self.lang != "vlog95compat"
            and self.lang != "sv"
            and self.lang != "sv05compat"
            and self.lang != "sv09compat"
            and self.lang != "sv12compat"
        ):
            print(
                "Language defined in config file is not valid.\nValid options are:\n\tVHDL 2008\n\tVHDL 2002\n\tVHDL 93\n\tVHDL 87\n\tverilog\n\tvlog01compat\n\tvlog95compat\n\tsv\n\tsv05compat\n\tsv09compat\n\tsv12compat"
            )
            exit()
        self.order = order
        self.check_syn = check_syn
        self.hier = hier
        self.n_files = len(hier)
        self.mixed = mixed

    def __str__(self):
        return f"files({self.src_path}, {self.lib}, {self.lang}, {self.order}, {self.check_syn}, {self.hier}, {self.n_files}, {self.mixed})"

    def get_ty(self):
        return "file"


class list_files:
    def __init__(self, src_path, lib, lang, order, check_syn, mixed):
        self.src_path = src_path
        self.lib = lib
        self.lang = lang
        self.order = order
        self.check_syn = check_syn
        self.mixed = mixed

    def __str__(self):
        return f"list files({self.src_path}, {self.lib}, {self.lang}, {self.order},{self.check_syn}, {self.mixed})"

    def get_ty(self):
        return "list"


class simulation:
    def __init__(
        self,
        opt,
        command_line,
        use_script,
        sim_script=None,
        top_entity=None,
        run_time=None,
    ):
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
                    print(
                        "!!!Warning!!! Run time and top entity should be defined inside the simulation script.\nValues defined in the configuration file will be ignored!"
                    )
        else:
            if self.top_entity == None:
                print("The top entity name is not defined!")
                exit()

    def __str__(self):
        return f"Simulation settings( optimizations = {self.opt}, command line = {self.command_line}, use script = {self.use_script}, sim script path = {self.sim_script}, top entity = {self.top_entity}, run time = {self.run_time})"


class configuration:
    def __init__(self, config_path):
        # Get the configuration path and open the file
        self.file_path = config_path
        with open(self.file_path, "r") as self.config_file:
            self.config_data = json.load(self.config_file)

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


# Function to run powershell command
def pwsh_run(cmd):
    return subprocess.run(["pwsh.exe", "-Command", cmd], stdout=sys.stdout)


# Function to compile files for windows
def compile_windows(files, list_files, path, prj_path, libs):
    # clean all libraries in the project folder
    for x in libs:
        command = (
            path + "compile.ps1" + " -prj_path " + prj_path + " -work " + x + " -clean"
        )
        pwsh_run(command)
    size = len(files) + len(list_files)
    ordered_list = [None] * size
    for f in files:
        ordered_list[f.order - 1] = f
    for fi in list_files:
        ordered_list[fi.order - 1] = fi
    for x in ordered_list:
        if x.get_ty() == "file":
            flags = ""
            if x.check_syn == "True":
                flags = " -syn"

            if x.mixed == "True":
                flags += " -mix"

            files = x.hier
            for f in files:
                command = (
                    path + "compile.ps1"
                    " -src_path "
                    + x.src_path
                    + "/"
                    + f
                    + " -prj_path "
                    + prj_path
                    + " -lang "
                    + x.lang
                    + " -work "
                    + x.lib
                    + flags
                )
                pwsh_run(command)

        elif x.get_ty() == "list":
            # @TODO fix the list compilation, need to spilt the verilog from vhdl, verilog we have to read the file
            print(x.get_ty(), x)
        else:
            print("ERROR: not valid type")
            exit(-1)


def simulation_windows(sim_conf):
    # @TODO need to fix simulation function windows
    print("Simulation function not supported yet")
    exit()


# @TODO Function to compile files for linux
def compile_linux(files, list_files, path, prj_path, libs):
    print("Compilation for linux not supported yet")
    exit()


def simulation_linux(sim_conf):
    # @TODO need to fix simulation function linux
    print("Simulation function not supported yet")
    exit()


if __name__ == "__main__":
    args = read_arg()
    # print(args.json_file)
    # print(args.s)
    conf = configuration(args.json_file)
    conf.print_me()
    OS = platform.system()
    print(OS)
    if OS == "Windows":
        compile_windows(conf.fi, conf.fi_list, conf.path_pwsh, conf.prj_dir, conf.libs)
    elif OS == "Linux":
        print("Helo Linux")
        compile_linux(conf.fi, conf.fi_list, conf.path_pwsh, conf.prj_dir, conf.libs)
    else:
        print("Not supported OS!")
        exit()

    if args.s:
        if conf.simulation:
            if OS == "Windows":
                simulation_windows(conf.sim_conf)
            elif OS == "Linux":
                print("Helo Linux")
                simulation_linux(conf.sim_conf)
            else:
                print("Not supported OS!")
                exit()
        else:
            print("Simulation settings not defined in the configuration file!")
            exit()
