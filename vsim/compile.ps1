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
Param($src_path, $VHDL = 2008, [switch] $help, $work = "work", [switch] $clean, $f, $sim, [switch] $syn, $UVM, [switch] $mix)


$work_path = $PWD.ToString()
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
    Write-Host "It requres as an input the path to a file or to a directory with all the HDL Files"
    Write-Host "It requires either src_path or clean argument"
    Write-Host "-src_path : path to file or directory"
    Write-Host "-VHDL     : Specify a string that is the version of VHDL to be used"
    Write-Host "-work     : Specify a string that is the name of work library (default is `"work`")"
    Write-Host "-clean    : Completly removes the work library, if it used together with a valid src_path it rebuilds the work library"
    Write-Host "-f        : Specify file with an ordered list of the HDL files, possible values are VHDL or Verilog"
    write-Host "-syn      : Enables flag -check_synthesis"
    Write-Host "-UVM      : Specifies the UVM home directory. If left empty together with an .sv file, the compilation is done as simple sv."
    Write-Host "-mix      : Use this command while compilling VHDL it will compile using the mixedsvvh argument"
    Write-Host "-help     : Prints this message"
    return
  }
}

$custom_flag = ""

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
  Write-Host "-src_path : path to file or directory"
  Write-Host "-VHDL     : Specify a string that is the version of VHDL to be used"
  Write-Host "-work     : Specify a string that is the name of work library (default is `"work`")"
  Write-Host "-clean    : Completly removes the work library, if it used together with a valid src_path it rebuilds the work library"
  Write-Host "-f        : Specify file with an ordered list of the HDL files, possible values are VHDL or Verilog"
  write-Host "-syn      : Enables flag -check_synthesis"
  Write-Host "-UVM      : Specifies the UVM home directory. If left empty together with an .sv file, the compilation is done as simple sv."
  Write-Host "-mix      : Use this command while compilling VHDL it will compile using the mixedsvvh argument"
  Write-Host "-help     : Prints this message"
  return -1
}

if ((-not (($f -eq "Verilog") -or ($f -eq "VHDL"))) -and (-not ($null -eq $f))) {
  Write-Host "-f should only be Verilog or VHDL"
  return
}

if (-not (($VHDL -eq 2008) -or ($VHDL -eq 2002) -or ($VHDL -eq 93) -or ($VHDL -eq 87) -or ($VHDL -eq "ams99") -or ($VHDL -eq "ams07"))) {
  Write-Host "Not a valid VHDL version"
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

$list = Get-ChildItem $src_path -Recurse
$flag = $true
ForEach ($n in $list) {
  $vhdlf = [IO.Path]::GetExtension($n) -eq '.vhd' -or [IO.Path]::GetExtension($n) -eq '.vhdl'
  if ($vhdlf) {
    if ($syn) {
      vcom -$VHDL -check_synthesis $custom_flag $n 
    }
    else {
      vcom -$VHDL $custom_flag $n 
    }
    Write-Host $n
    $flag = $false
  }
  $verilog = [IO.Path]::GetExtension($n) -eq '.v' -or [IO.Path]::GetExtension($n) -eq '.sv'
  if ($verilog) {
    if ($UVM_FLAG) {
      vlog +incdir+$UVM/src $UVM/src/uvm_pkg.sv $UVM/src/uvm_macros.svh $n
    }
    else {
      vlog $n
    }
    Write-Host $n
    $flag = $false
  }
  if ((-not($vhdlf -or $verilog)) -and ([IO.Path]::GetExtension($n) -eq '.f')) {
    if ($null -eq $f) {
      Write-Host "No VHDL or Verilog file found and -f not set"
    }
    else {
      if ($f -eq "VHDL") {
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
          vlog -F $n
        }
        return 0
      }
    }
    $flag = $false
  }
}

if ($flag) {
  Write-Host "No list, vhdl or verilog files found"
  return
}