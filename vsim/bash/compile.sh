#!/bin/bash




############################################################
# Help                                                     #
############################################################
Help()
{
  # Display Help
  echo "This script can be used to compile one or multiple HDL files."
  echo "It requres as an input the path to a file"
  echo "It requires either src_path or clean argument"
  echo "The \"-src_path\" should be a path to a directory or file."
  echo "This script can be used to compile one or multiple HDLfiles."
  echo "It requres as an input the path to a file or to adirectory with all the HDL Files"
  echo "It requires either src_path or clean argument"
  echo "-src_path : path to file"
  echo "-lang     : Specify a string that is the HDL langauge tobe used (and its version)"
  echo "            Accepted options:"
  echo "                VHDL: "
  echo "                      \"2008\""
  echo "                      \"2002\""
  echo "                      \"93\""
  echo "                      \"87\""
  echo "                Verilog: "
  echo "                      \"verilog\""
  echo "                      \"vlog01compat\""
  echo "                      \"vlog95compat\""
  echo "                System Verilog: "
  echo "                      \"sv\""
  echo "                      \"sv05compat\""
  echo "                      \"sv09compat\""
  echo "                      \"sv12compat\""
  echo "-work     : Specify a string that is the name of worklibrary (default is \"work\")"
  echo "-clean    : Completly removes the work library, if itused together with a valid src_path it rebuilds the work library"
  echo "-f        : File is an ordered list of the HDL files"
  echo "-syn      : Enables flag -check_synthesis"
  echo "-UVM      : Specifies the UVM home directory. If left empty together with an .sv file, the compilation is done as simplesv."
  echo "-mix      : Use this command while compilling VHDL itwill compile using the mixedsvvh argument"
  echo "-help     : Prints this message"
}

############################################################
############################################################
# Main program                                             #
############################################################
############################################################
############################################################
# Process the input options. Add options as needed.        #
############################################################
if [ $# -eq 0 ]; then
  Help
  exit -1
fi
flag=0

# Get the options
#for i in $@
while [[ $# -gt 0 ]];
do
  case $1 in
    -e|--extension)
      EXTENSION="${2}"
      shift # past argument=value
      echo $EXTENSION
    ;;
    -s*|--searchpath=*)
      SEARCHPATH="${1#*}"
      shift # past argument=value
      echo $SEARCHPATH
    ;;
    --default)
      DEFAULT=YES
      shift # past argument with no value
    ;;
    -*|--*)
      echo "Unknown option $1"
      exit 1
    ;;
    *)
      POSITIONAL_ARGS+=("$1") # save positional arg
      shift # past argument
    ;;
  esac
done

if [ $flag -eq 1 ]; then
  echo $flag
fi
echo "Flag was $flag"





#set TOP_NAME parallel_fir
#set RUN_TIME "5us"
#
#set REPORT_DIR  ./syn/rpt;      # synthesis reports: timing, area, etc.
#set OUT_DIR ./syn/db;           # output files: netlist, sdf sdc etc.
#set SOURCE_DIR ./rtl;           # rtl code that should be synthesised
#set SYN_DIR ./syn;              # synthesis directory, synthesis scripts constraints etc.
#set TB_DIR ./tb;                # testbench directory
#
#set hierarchy_files [split [read [open ${SOURCE_DIR}/${TOP_NAME}_hierarchy.txt r]] "\n"]
## close ${SOURCE_DIR}/${TOP_NAME}_hierarchy.txt
#
#foreach filename [lrange ${hierarchy_files} 0 end-1] {
#    # puts "${filename}"
#    if {[string equal [file extension $filename] ".vhd"]} {
#        vcom -2008 -work work ${SOURCE_DIR}/${filename}
#        } else {
#        vlog -v2001 -work work ${SOURCE_DIR}/${filename}
#    }
#}
#vcom -2008 -work work ${TB_DIR}/${TOP_NAME}_tb.vhd
#
#vsim -voptargs=+acc work.${TOP_NAME}_tb
#add wave sim:/${TOP_NAME}_tb/*
#wave zoom full
#
#run ${RUN_TIME}
