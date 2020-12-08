#!/bin/bash
#source subprocess.sh


# decode(inn) {
#   echo "$inn" | base64 -d ; echo
# }



if [[ $# -ge 6 ]]; then
	#echo $#
	classfile=$1
	input_filename=$2
	output_filename=$3
	tl=$4
	base_classfile=$5
	cli=""
	for (( i = 6; i <= $#; i++ )); do
		#echo $i
		if [[ i -lt $# ]]; then
			cli+=$i
			cli+=" "
		else
			cli+=$i
		fi
		
	done
	#echo $cli
else
	exit -1
fi


input_file=`cat $input_filename`
output_file=`cat $output_filename`


bash ./subprocess.sh "$classfile" "$input_file" "$output_file" "$tl"

# rc=$?
# echo $rc
# echo "temp_bash"

# if rc==0:
#     echo execute.stdout.decode() >> output_file
        
# elif rc==124:
#   	echo "TLE" >> output_file

# elif rc==136:
#     echo "Floating point exception (core dumped)" >> output_file

# elif rc==139:
#     echo "Segmentation fault (core dumped)" >> output_file

# elif rc==134:
#     echo "Aborted (core dumped)" >> output_file

# elif rc==1:
#     echo "Execution failed" >> output_file

# elif rc==255:
#     echo "Program Timed Out" >> output_file

# else:
#     echo "Runtime Error" >> output_file

echo $output_file