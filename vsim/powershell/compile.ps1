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
Param( [string[]] $src_path, [string[]] $lang = "VHDL 2008", [switch] $help, [string[]]$prj_path = ".", $work = "work", [switch] $clean, [switch] $f, [switch] $syn, [string[]] $UVM, [switch] $mix, [string[]] $misc_options = "")

#=======================================================================================================#
# Set up 
#=======================================================================================================#
$work_path = $prj_path
$work_path = $work_path + "\" + $work

if (($help) -or (!$src_path)) {
  if ($clean) {
    if (!(Test-Path $work_path)) {
      Write-Host "Work Library does not exist, Specify work library using the `"-work`" argument."
      Write-Host "For more details see `"-help`"."
      return -1
    }
    else {
      Write-Host "Work library already exists"
      if ($clean) {
        Write-Host "Removing work library"
        Remove-Item $work -Recurse -Force
        return
      }
    }
  }
  else {
    Write-Host "This script can be used to compile one or multiple HDL files."
    Write-Host "It requres as an input the path to a file"
    Write-Host "It requires either src_path or clean argument"
    Write-Host "The `""$src_path "`" should be a path to a directory or file."
    Write-Host "This script can be used to compile one or multiple HDL files."
    Write-Host "It requres as an input the path to a file or to a directory with all the HDL Files"
    Write-Host "It requires either src_path or clean argument"
    Write-Host "-src_path : path to file"
    Write-Host "-lang     : Specify a string that is the HDL langauge to be used (and its version)"
    Write-Host "            Accepted options:"
    Write-Host "                VHDL: "
    Write-Host "                      `"2008`""
    Write-Host "                      `"2002`""
    Write-Host "                      `"93`""
    Write-Host "                      `"87`""
    Write-Host "                Verilog: "
    Write-Host "                      `"verilog`""
    Write-Host "                System Verilog: "
    Write-Host "                      `"SV`""
    Write-Host "-work     : Specify a string that is the name of work library (default is `"work`")"
    Write-Host "-clean    : Completly removes the work library, if it used together with a valid src_path it rebuilds the work library"
    Write-Host "-f        : File is an ordered list of the HDL files"
    write-Host "-syn      : Enables flag -check_synthesis"
    Write-Host "-UVM      : Specifies the UVM home directory. If left empty together with an .sv file, the compilation is done as simple sv."
    Write-Host "-mix      : Use this command while compilling VHDL it will compile using the mixedsvvh argument"
    Write-Host "-help     : Prints this message"
    return
  }
}

$custom_flag = $misc_options

$UVM_FLAG = $false
if ($UVM) {
  $UVM_FLAG = $true
}

if ((-not (Test-Path $src_path))) {
  Write-Host "Path or file argument missing or wrong."
  Write-Host "The `""$src_path "`" should be a path to a directory or file."
  Write-Host "This script can be used to compile one or multiple HDL files."
  Write-Host "It requres as an input the path to a file or to a directory with all the HDL Files"
  Write-Host "It requires either src_path or clean argument"
  Write-Host "-src_path : path to file"
  Write-Host "-lang     : Specify a string that is the HDL langauge to be used (and its version)"
  Write-Host "            Accepted options:"
  Write-Host "                VHDL: "
  Write-Host "                      `"2008`""
  Write-Host "                      `"2002`""
  Write-Host "                      `"93`""
  Write-Host "                      `"87`""
  Write-Host "                Verilog: "
  Write-Host "                      `"verilog`""
  Write-Host "                System Verilog: "
  Write-Host "                      `"SV`""
  Write-Host "-work     : Specify a string that is the name of work library (default is `"work`")"
  Write-Host "-clean    : Completly removes the work library, if it used together with a valid src_path it rebuilds the work library"
  Write-Host "-f        : File is an ordered list of the HDL files"
  write-Host "-syn      : Enables flag -check_synthesis"
  Write-Host "-UVM      : Specifies the UVM home directory. If left empty together with an .sv file, the compilation is done as simple sv."
  Write-Host "-mix      : Use this command while compilling VHDL it will compile using the mixedsvvh argument"
  Write-Host "-help     : Prints this message"
  return -1
}

# Set the langauge flags
$vhdlf = $false
$SVf = $false
$verilogf = $false
if (($lang -eq "2008") -or ($lang -eq "2002") -or ($lang -eq "93") -or ($lang -eq "87") -or ($lang -eq "ams99") -or ($lang -eq "ams07")) {
  $vhdlf = $true
}
elseif ($lang -eq "verilog") {
  $verilogf = $true
}
elseif ($lang -eq "SV") {
  $SVf = $true
}
else {
  Write-Host "Not a valid langauge selection."
  Write-Host "            Accepted options:"
  Write-Host "                VHDL: "
  Write-Host "                      `"2008`""
  Write-Host "                      `"2002`""
  Write-Host "                      `"93`""
  Write-Host "                      `"87`""
  Write-Host "                Verilog: "
  Write-Host "                      `"verilog`""
  Write-Host "                System Verilog: "
  Write-Host "                      `"SV`""
  return
}

if (!(Test-Path $work_path)) {
  Write-Host "Work Library does not exist, creating work Library"
  vlib $work
  vmap work $work_path
}
else {
  Write-Host "Work library already exists"
  if ($clean) {
    Write-Host "Removing and re-creating work library"
    Remove-Item $work -Recurse -Force
    vlib $work
    vmap work $work_path
  }
}

#=======================================================================================================#
# Compile single files
#=======================================================================================================#


if ($vhdlf) {
  if ($syn) {
    Write-Host "vcom -$lang -check_synthesis $custom_flag $src_path" 
  }
  else {
    Write-Host "vcom -$lang $custom_flag $src_path"
  }
  Write-Host "Copilation of $src_path completed"

}

if ($verilogf -or $SVf) {
  if ($UVM_FLAG) {
    Write-Host "vlog +incdir+$UVM/src $UVM/src/uvm_pkg.sv $UVM/src/uvm_macros.svh $src_path"
  }
  else {
    Write-Host "vlog $src_path"
  }
  Write-Host "Copilation of $src_path completed"
}

#=======================================================================================================#
# Compile lists
#=======================================================================================================#

if ($f) {
  if ($vhdlf) {}
  if ($mix) {
    $custom_flag = "-mixedsvvh"
  }
  Write-Host "Reading list file (VHDL)"
  if ($syn) {
    vcom -F $n -$VHDL -check_synthesis $custom_flag
  }
  else {
    vcom -F $n -$VHDL $custom_flag
  }
                
}
else {
  if ($UVM_FLAG) {
    vlog +incdir+$UVM/src $UVM/src/uvm_pkg.sv $UVM/src/uvm_macros.svh -F $n
  }
  else {
    vlog -f $n
  }
  return 0
}