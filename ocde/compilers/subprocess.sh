#! /bin/bash


timeout $4 java $1 $2 &> $3   # Time limit on the execution time
rc=$?
#echo $rc
#echo "subprocess"

if [[ $rc -ne 0 ]]
then
    cat $3
    exit 1
elif [[ $rc -eq 0 ]]
then
    #echo "" >> $3 
    cat $3
    exit 0
fi       




#./$2+'.out'