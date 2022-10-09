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
