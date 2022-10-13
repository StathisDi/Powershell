<#
Author : Dimitrios Stathis
Copyright 2021


This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
#>
Param($top, $work = "work", [switch] $gui)

if ($null -eq $top) {
  Write-Host "Top/TB level name of the module is needed"
  return
}

$name = $work + "." + $top
Write-Host $name
if ($gui) {
  vsim $name -voptargs=+acc -debugDB
}
else {
  vsim $name -voptargs=+acc -c -debugDB
}

# vsim -c -do "add waves" -do "run $runtime" .... 
# -fsmdebug
# -accessobjdebug (ebables loging of variables)
# -std_input <filename> Specifies the file to use for the VHDL TextIO STD_INPUT file.
# 


# Procedure
# Recommended Procedure for Database Creation
# The recommended procedure gives you complete control of the optimization # process.
# 
# Create a library for your work.
# vlib <library_name>
# 
# Compile your design into the library.
# vcom and/or vlog
# 
# Optimize your design and collect combinatorial and sequential logic data.
# vopt +acc <filename> -o <optimized_filename> -debugdb
# 
# The +acc argument maintains visibility into your design for debugging, # while the -debugdb argument saves combinatorial and sequential logic # events to the working library. All +acc options execute, even when you # include a -debugdb option.
# 
# Load your design (elaboration).
# vsim -debugdb <optimized_filename>
# 
# The -debugdb argument instructs the simulator to look for combinatorial # and sequential logic event data in the working library, then creates the # debug database (vsim.dbg) from this information.
# 
# The default filename for the .dbg file is vsim.dbg. If you want to # create a different name, use the following command syntax:
# 
# vsim -debugdb=<custom_name>.dbg -wlf <custom_name>.wlf # <optimized_filename>
# 
# The <custom_name> must be the same for the .dbg file and the .wlf file.
# 
# Log simulation data.
#    log -r /* or add wave -r /*
# 
# It is advisable to log the entire design to provide historic values of # the events of interest, plus their drivers. However, to reduce overhead, # you can log only the regions of interest.
# 
# You can use the log command to save the simulation data to the .wlf # file. Or, use the add wave command to log the simulation data to the .# wlf file and display simulation results as waveforms in the Wave window.
# 
# Run the simulation.
# Initiate a causality trace from the command line or from the GUI.
# Abbreviated Procedure for Database Creation
# You can abbreviate the database creation procedure with the steps that # follow. However, this abbreviated procedure does not give you the # control over the optimization process provided by the recommended # procedure above.
# 
# Create a library for your work.
#    vlib <library_name>
# 
# Compile your design.
#    vcom and/or vlog
# 
# Load your design
#    vsim -voptargs=”+acc” -debugdb <design_name>
# 
# The -voptargs=”+acc” argument for the vsim command maintains visibility # into your design for debugging.
# 
# The -debugdb argument performs a pre-simulation analysis of the # sequential and combinatorial elements in your design and generates the # required debug information for schematic analysis.
# 
# Log your design
#    log -r /* or add wave -r /*
# 
# Run the simulation
# Initiate a causality trace from the command line or from the GUI.