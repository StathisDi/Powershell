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

    def get_lang(self):
        if (
            self.lang == "2008"
            or self.lang == "2002"
            or self.lang == "93"
            or self.lang == "97"
        ):
            return "VHDL"
        elif (
            self.lang == "verilog"
            or self.lang == "vlog01compat"
            or self.lang == "vlog95compat"
        ):
            return "verilog"
        else:
            return "sv"
