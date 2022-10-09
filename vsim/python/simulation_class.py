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

# Class that is used by the compilation and configuration class


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
