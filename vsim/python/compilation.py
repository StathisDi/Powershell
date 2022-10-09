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
from simulation_class import simulation
from list_files_class import list_files
from files_class import files
from configuration_class import configuration


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


# Function to run powershell command
def pwsh_run(cmd):
    print(cmd)
    # return subprocess.run(["pwsh.exe", "-Command", cmd], stdout=sys.stdout)


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
            if x.get_lang() == "VHDL":
                command = (
                    path + "compile.ps1"
                    " -src_path "
                    + x.src_path
                    + " -prj_path "
                    + prj_path
                    + " -lang "
                    + x.lang
                    + " -f -work "
                    + x.lib
                    + flags
                )
                pwsh_run(command)
            else:
                print("Not VHDL")
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
