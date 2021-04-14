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
Param($location)
function writeLog {
  param ([string] $LOG, [string] $STR)
  Write-Host $LOG
  if (Test-Path $LOG -PathType Leaf) {
    # File already exist
    $date = (Get-Date -UFormat "%A %Y/%b/%d - %T : ")
    $text = $date + $STR
    $text | Out-File -FilePath $LOG -Append 
  }
  else {
    $date = (Get-Date -UFormat "%A %Y/%b/%d - %T : ")
    $text = $date + $STR
    $text | Out-File -FilePath $LOG
  }
  
}

$log_file = "$HOME\Documents\wallpaper_log"

if (!$location) {
  Write-Host "Location of the wallpaper folder is required!"
  return
}
else {
  if ((-not (Test-Path $location))) {
    Write-Host "A Valid location to the wallpaper folder is required!"
    return -1
  }
  if ((-not (Test-Path $log_file))) {
    mkdir $log_file
  }
  $log_file = "$HOME\Documents\wallpaper_log\log.txt"
  $random = Get-Random $(Get-ChildItem -Path $location).Count
  $image = Get-ChildItem -name -Path $location | Select-Object -index $random
  try {
    Set-ItemProperty -path 'HKCU:\Control Panel\Desktop\' -name wallpaper -value $location\$image -ErrorAction Stop
    writeLog $log_file $image
    Write-Host $image
  }
  catch {
    writeLog $log_file "ERROR"
    return -1
  }
  rundll32.exe user32.dll, UpdatePerUserSystemParameters
}
